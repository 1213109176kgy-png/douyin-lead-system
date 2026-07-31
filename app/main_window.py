from __future__ import annotations

from datetime import datetime
from pathlib import Path
import tempfile

from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget,
    QDialog, QInputDialog, QMainWindow, QMessageBox, QProgressBar, QPushButton, QSpinBox, QSplitter,
    QStackedWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QTextEdit, QVBoxLayout, QWidget,
)
from PySide6.QtCore import QUrl

from .api_client import LocalApiClient
from .ai_client import DEFAULT_ANALYSIS_PROMPT, DEFAULT_REWRITE_PROMPT, OpenAICompatibleClient
from .collector import Collector, CollectorCallbacks
from .database import Database
from .douyin_login import DouyinLoginDialog
from .exporter import export_leads
from .paths import AppPaths
from .scoring import DEFAULT_NEGATIVES, DEFAULT_RULES
from .secure_store import SettingsStore
from .server_manager import ServerManager
from .video_ai import analyze_video, download_media, find_media_url, rewrite_video, shorten, transcribe_local


class AcquisitionWorker(QThread):
    progress = Signal(int, int, int)
    message = Signal(str)
    failed = Signal(str)
    completed = Signal()

    def __init__(self, db, manager, settings, task_id):
        super().__init__(); self.db=db; self.manager=manager; self.settings=settings; self.task_id=task_id; self.collector=None

    def run(self):
        try:
            order = self.settings.get_secret("order_number")
            ok, message = self.manager.start(order)
            self.message.emit(message)
            if not ok: raise RuntimeError(message)
            delay = float(self.settings.load().get("request_delay", 1.2))
            client = LocalApiClient(self.manager.base_url, "", delay, self.settings.get_secret("douyin_cookie"))
            callbacks = CollectorCallbacks(progress=lambda a,b,c: self.progress.emit(a,b,c), log=lambda text: self.message.emit(str(text)))
            self.collector = Collector(self.db, client, callbacks)
            self.collector.run(self.task_id)
            self.completed.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

    def pause(self):
        if self.collector: self.collector.pause()
    def resume(self):
        if self.collector: self.collector.resume()
    def cancel(self):
        if self.collector: self.collector.cancel()


class VideoAIWorker(QThread):
    message = Signal(str)
    failed = Signal(str)
    completed = Signal(str)

    def __init__(self, window, aweme_id, mode="analysis", requirements=""):
        super().__init__(); self.window=window; self.aweme_id=aweme_id; self.mode=mode; self.requirements=requirements

    def run(self):
        try:
            video=self.window.db.get_video(self.aweme_id); settings=self.window.settings
            client=OpenAICompatibleClient(settings.load().get("ai_base_url",""),settings.get_secret("ai_api_key"),settings.load().get("ai_model",""),int(settings.load().get("ai_timeout",90)),float(settings.load().get("ai_temperature",0.7)))
            if self.mode=="rewrite":
                if not video["analysis"]: raise RuntimeError("请先完成视频拆解")
                self.message.emit("正在整理拆解内容…")
                if self.isInterruptionRequested(): raise RuntimeError("用户已取消")
                self.message.emit("AI 正在生成仿写文案…")
                result=rewrite_video(client,settings.load().get("rewrite_prompt",DEFAULT_REWRITE_PROMPT),video,self.requirements)
                self.window.db.update_video_ai(self.aweme_id,rewrite=result); self.completed.emit(result); return
            order=settings.get_secret("order_number"); ok,msg=self.window.server.start(order)
            if not ok: raise RuntimeError(msg)
            api=LocalApiClient(self.window.server.base_url,"",1.0,settings.get_secret("douyin_cookie"))
            self.message.emit("正在解析原视频地址…"); detail=api.video_detail(self.aweme_id); media_url=find_media_url(detail)
            if self.isInterruptionRequested(): raise RuntimeError("用户已取消")
            if not media_url: raise RuntimeError("未能从接口解析视频播放地址")
            with tempfile.TemporaryDirectory(prefix="douyin-lead-") as temp:
                media=Path(temp)/f"{self.aweme_id}.mp4"; self.message.emit("正在下载原视频…"); download_media(media_url,media,settings.get_secret("douyin_cookie"))
                if self.isInterruptionRequested(): raise RuntimeError("用户已取消")
                transcript=transcribe_local(media,self.window.paths.data/"models",self.message.emit)
            if self.isInterruptionRequested(): raise RuntimeError("用户已取消")
            if not transcript: raise RuntimeError("未识别到有效口播内容")
            self.message.emit("正在调用 AI 拆解…")
            result=analyze_video(client,settings.load().get("analysis_prompt",DEFAULT_ANALYSIS_PROMPT),video,transcript)
            self.window.db.update_video_ai(self.aweme_id,transcript=transcript,analysis=result,media_url=media_url,archived=1,analyzed_at=datetime.now().isoformat(timespec="seconds")); self.completed.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class AIProgressDialog(QDialog):
    def __init__(self, title, worker, parent=None):
        super().__init__(parent); self.worker=worker; self.seconds=0; self.setWindowTitle(title); self.setModal(False); self.setFixedWidth(520)
        layout=QVBoxLayout(self); self.step=QLabel("准备开始…"); self.step.setWordWrap(True); self.elapsed=QLabel("已用时 0 秒"); self.progress=QProgressBar(); self.progress.setRange(0,0); cancel=QPushButton("取消")
        cancel.clicked.connect(self.cancel); layout.addWidget(self.step); layout.addWidget(self.progress); layout.addWidget(self.elapsed); layout.addWidget(cancel)
        self.timer=QTimer(self); self.timer.timeout.connect(self.tick); self.timer.start(1000)

    def tick(self): self.seconds+=1; self.elapsed.setText(f"已用时 {self.seconds} 秒")
    def update_step(self,text): self.step.setText(text)
    def cancel(self): self.worker.requestInterruption(); self.step.setText("正在取消，请等待当前步骤结束…")


def title(text):
    label = QLabel(text); label.setObjectName("pageTitle"); return label


def table(headers):
    widget = QTableWidget(0, len(headers)); widget.setHorizontalHeaderLabels(headers)
    widget.setEditTriggers(QAbstractItemView.NoEditTriggers); widget.setSelectionBehavior(QAbstractItemView.SelectRows)
    widget.setAlternatingRowColors(True); widget.setWordWrap(False)
    widget.verticalHeader().setVisible(False); widget.verticalHeader().setDefaultSectionSize(42)
    widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive); widget.horizontalHeader().setStretchLastSection(False)
    return widget


def icon_button(symbol, tooltip, slot):
    button=QPushButton(symbol); button.setToolTip(tooltip); button.setFixedSize(32,30); button.setStyleSheet("QPushButton{padding:0;font-size:16px;}")
    button.clicked.connect(slot); return button


class MainWindow(QMainWindow):
    def __init__(self, paths: AppPaths):
        super().__init__(); self.paths=paths.ensure(); self.db=Database(paths.database); self.settings=SettingsStore(paths.settings)
        self.server=ServerManager(paths.server, paths.logs / "apiserver.log"); self.worker=None; self.ai_worker=None; self.ai_progress=None
        self.setWindowTitle("抖音获客系统"); self.resize(1380, 860); self.setMinimumSize(1100, 700)
        self.nav = QListWidget(); self.nav.setFixedWidth(190)
        self.stack = QStackedWidget(); self.pages=[]
        for name, maker in [("工作台",self.dashboard_page),("获客任务",self.tasks_page),("客户池",self.leads_page),("视频库",self.videos_page),("爆款素材库",self.materials_page),("意向规则",self.rules_page),("任务记录",self.history_page),("数据导出",self.export_page),("系统设置",self.settings_page)]:
            self.nav.addItem(name); page=maker(); self.pages.append(page); self.stack.addWidget(page)
        root=QWidget(); layout=QHBoxLayout(root); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0); layout.addWidget(self.nav); layout.addWidget(self.stack,1); self.setCentralWidget(root)
        self.nav.currentRowChanged.connect(self.on_page_changed); self.nav.setCurrentRow(0); self.refresh_all()

    def page_shell(self, heading):
        page=QWidget(); layout=QVBoxLayout(page); layout.setContentsMargins(28,24,28,24); layout.setSpacing(16); layout.addWidget(title(heading)); return page,layout

    def dashboard_page(self):
        page,layout=self.page_shell("工作台"); grid=QGridLayout(); self.kpis={}
        for i,(key,label) in enumerate([("leads","累计客户"),("high","高意向客户"),("videos","已扫描视频"),("tasks","采集任务")]):
            card=QFrame(); card.setObjectName("card"); box=QVBoxLayout(card); box.addWidget(QLabel(label)); value=QLabel("0"); value.setObjectName("kpiValue"); box.addWidget(value); self.kpis[key]=value; grid.addWidget(card,0,i)
        layout.addLayout(grid); note=QLabel("数据仅保存在本机。建议先到“系统设置”填写订单授权号，再创建获客任务。"); note.setWordWrap(True); layout.addWidget(note); layout.addStretch(); return page

    def tasks_page(self):
        page,layout=self.page_shell("获客任务"); form_card=QFrame(); form_card.setObjectName("card"); form=QFormLayout(form_card)
        self.keyword=QLineEdit(); self.keyword.setPlaceholderText("例如：销售工牌、智能工牌")
        self.target=QSpinBox(); self.target.setRange(1,500); self.target.setValue(50)
        self.max_videos=QSpinBox(); self.max_videos.setRange(1,100); self.max_videos.setValue(30)
        self.comments_per_video=QSpinBox(); self.comments_per_video.setRange(10,500); self.comments_per_video.setValue(100)
        self.include_replies=QCheckBox("采集二级评论（会增加请求量）")
        for label,widget in [("行业/产品关键词",self.keyword),("目标客户数",self.target),("最多扫描视频",self.max_videos),("每个视频最多评论",self.comments_per_video),("更多范围",self.include_replies)]: form.addRow(label,widget)
        layout.addWidget(form_card)
        buttons=QHBoxLayout(); self.start_btn=QPushButton("开始获客"); self.pause_btn=QPushButton("暂停"); self.resume_btn=QPushButton("继续"); self.cancel_btn=QPushButton("停止")
        for b in (self.start_btn,self.pause_btn,self.resume_btn,self.cancel_btn): buttons.addWidget(b)
        buttons.addStretch(); layout.addLayout(buttons); self.task_progress=QProgressBar(); layout.addWidget(self.task_progress); self.task_status=QLabel("尚未开始"); layout.addWidget(self.task_status)
        self.start_btn.clicked.connect(self.start_task); self.pause_btn.clicked.connect(lambda: self.worker and self.worker.pause()); self.resume_btn.clicked.connect(lambda: self.worker and self.worker.resume()); self.cancel_btn.clicked.connect(lambda: self.worker and self.worker.cancel())
        self.task_table=table(["任务","关键词","目标","状态","采集进度","客户","更新时间","错误"]); layout.addWidget(self.task_table,1)
        self.task_table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch); self.task_table.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch); self.task_table.setColumnWidth(0,58); self.task_table.setColumnWidth(2,54); self.task_table.setColumnWidth(3,76); self.task_table.setColumnWidth(4,124); self.task_table.setColumnWidth(5,54); self.task_table.setColumnWidth(6,142); return page

    def leads_page(self):
        page,layout=self.page_shell("客户池"); filters=QHBoxLayout(); self.lead_task=QComboBox(); self.lead_keyword=QLineEdit(); self.lead_keyword.setPlaceholderText("搜索昵称、关键词"); self.lead_level=QComboBox(); self.lead_level.addItems(["全部等级","高","中","低"]); self.lead_status=QComboBox(); self.lead_status.addItems(["全部状态","待跟进","已联系","已成交","无效"]); refresh=QPushButton("刷新")
        for widget in (self.lead_task,self.lead_keyword,self.lead_level,self.lead_status,refresh): filters.addWidget(widget)
        filters.addStretch(); layout.addLayout(filters)
        self.lead_table=table(["意向","昵称","任务关键词","原评论","命中词","状态","操作"]); layout.addWidget(self.lead_table,1)
        self.lead_table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch); self.lead_table.setColumnWidth(0,70); self.lead_table.setColumnWidth(1,96); self.lead_table.setColumnWidth(2,90); self.lead_table.setColumnWidth(4,84); self.lead_table.setColumnWidth(5,68); self.lead_table.setColumnWidth(6,106)
        refresh.clicked.connect(self.refresh_leads); self.lead_task.currentIndexChanged.connect(self.refresh_leads); self.lead_level.currentIndexChanged.connect(self.refresh_leads); self.lead_status.currentIndexChanged.connect(self.refresh_leads); self.lead_keyword.returnPressed.connect(self.refresh_leads); return page

    def videos_page(self):
        page,layout=self.page_shell("视频库"); filters=QHBoxLayout(); self.video_task=QComboBox(); self.video_search=QLineEdit(); self.video_search.setPlaceholderText("搜索标题、作者、关键词"); self.video_analysis=QComboBox(); self.video_analysis.addItems(["全部状态","已拆解","未拆解"]); refresh=QPushButton("刷新")
        for widget in (self.video_task,self.video_search,self.video_analysis,refresh): filters.addWidget(widget)
        filters.addStretch(); layout.addLayout(filters)
        self.video_table=table(["标题","作者","关键词","数据表现","线索","拆解状态","操作"]); layout.addWidget(self.video_table,1)
        self.video_table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch); self.video_table.setColumnWidth(1,90); self.video_table.setColumnWidth(2,90); self.video_table.setColumnWidth(3,150); self.video_table.setColumnWidth(4,54); self.video_table.setColumnWidth(5,76); self.video_table.setColumnWidth(6,118)
        refresh.clicked.connect(self.refresh_videos); self.video_task.currentIndexChanged.connect(self.refresh_videos); self.video_analysis.currentIndexChanged.connect(self.refresh_videos); self.video_search.returnPressed.connect(self.refresh_videos); return page

    def materials_page(self):
        page,layout=self.page_shell("爆款素材库"); filters=QHBoxLayout(); self.material_task=QComboBox(); self.material_search=QLineEdit(); self.material_search.setPlaceholderText("搜索标题、关键词或标签"); self.material_rewrite=QComboBox(); self.material_rewrite.addItems(["全部状态","已仿写","未仿写"]); refresh=QPushButton("刷新")
        for widget in (self.material_task,self.material_search,self.material_rewrite,refresh): filters.addWidget(widget)
        filters.addStretch(); layout.addLayout(filters)
        self.material_table=table(["素材标题","关键词 / 标签","数据表现","仿写状态","操作"]); layout.addWidget(self.material_table,1)
        self.material_table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch); self.material_table.setColumnWidth(1,140); self.material_table.setColumnWidth(2,170); self.material_table.setColumnWidth(3,76); self.material_table.setColumnWidth(4,158)
        refresh.clicked.connect(self.refresh_materials); self.material_task.currentIndexChanged.connect(self.refresh_materials); self.material_rewrite.currentIndexChanged.connect(self.refresh_materials); self.material_search.returnPressed.connect(self.refresh_materials); return page

    def rules_page(self):
        page,layout=self.page_shell("意向规则"); info=QLabel("新建或修改规则后，下一次获客任务会立即使用启用中的规则。关键词请用“|”分隔。"); info.setWordWrap(True); layout.addWidget(info)
        buttons=QHBoxLayout(); add=QPushButton("添加规则"); buttons.addWidget(add)
        buttons.addStretch(); layout.addLayout(buttons)
        self.rule_table=table(["ID","分类","分值","关键词","状态","操作"]); layout.addWidget(self.rule_table,1)
        self.rule_table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch); self.rule_table.setColumnWidth(0,54); self.rule_table.setColumnWidth(1,120); self.rule_table.setColumnWidth(2,64); self.rule_table.setColumnWidth(4,72); self.rule_table.setColumnWidth(5,118)
        add.clicked.connect(self.add_rule); return page

    def history_page(self):
        page,layout=self.page_shell("任务记录"); filters=QHBoxLayout(); self.log_task=QComboBox(); self.log_status=QComboBox(); self.log_status.addItems(["全部结果","ok","error"]); refresh=QPushButton("刷新")
        for widget in (self.log_task,self.log_status,refresh): filters.addWidget(widget)
        filters.addStretch(); layout.addLayout(filters)
        self.log_table=table(["任务","阶段","状态","发现","消息","时间"]); layout.addWidget(self.log_table,1)
        self.log_table.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch); self.log_table.setColumnWidth(0,72); self.log_table.setColumnWidth(1,100); self.log_table.setColumnWidth(2,72); self.log_table.setColumnWidth(3,64); self.log_table.setColumnWidth(5,150)
        refresh.clicked.connect(self.refresh_logs); self.log_task.currentIndexChanged.connect(self.refresh_logs); self.log_status.currentIndexChanged.connect(self.refresh_logs); return page

    def export_page(self):
        page,layout=self.page_shell("数据导出"); card=QFrame(); card.setObjectName("card"); form=QFormLayout(card); self.export_task=QComboBox(); self.export_level=QComboBox(); self.export_level.addItems(["全部","高","中","低"]); self.export_status=QComboBox(); self.export_status.addItems(["全部","待跟进","已联系","已成交","无效"]); self.export_count=QLabel("预计导出 0 条"); self.export_button=QPushButton("导出 Excel")
        form.addRow("选择任务",self.export_task); form.addRow("意向等级",self.export_level); form.addRow("客户状态",self.export_status); form.addRow("结果预览",self.export_count); form.addRow("",self.export_button); layout.addWidget(card); layout.addStretch()
        self.export_task.currentIndexChanged.connect(self.refresh_export_count); self.export_level.currentIndexChanged.connect(self.refresh_export_count); self.export_status.currentIndexChanged.connect(self.refresh_export_count); self.export_button.clicked.connect(self.do_export); return page

    def settings_page(self):
        page,layout=self.page_shell("系统设置"); card=QFrame(); card.setObjectName("card"); form=QFormLayout(card)
        self.order_number=QLineEdit(); self.order_number.setEchoMode(QLineEdit.Password); self.order_number.setPlaceholderText("首次使用必须填写")
        self.delay=QDoubleSpinBox(); self.delay.setRange(0.8,30); self.delay.setSingleStep(0.2); self.delay.setValue(float(self.settings.load().get("request_delay",1.2)))
        saved=self.settings.load(); self.order_number.setPlaceholderText("已保存" if saved.get("order_number") else "首次使用必须填写")
        self.login_state=QLabel("已登录" if saved.get("douyin_cookie") else "未登录")
        login=QPushButton("一键登录抖音" if not saved.get("douyin_cookie") else "重新登录抖音")
        clear_login=QPushButton("清除登录状态")
        self.server_state=QLabel("未检测"); save=QPushButton("保存设置"); start=QPushButton("启动并检测本地服务"); stop=QPushButton("停止本地服务")
        login_row=QHBoxLayout(); login_row.addWidget(self.login_state); login_row.addWidget(login); login_row.addWidget(clear_login)
        form.addRow("订单授权号",self.order_number); form.addRow("抖音登录",login_row); form.addRow("请求间隔（秒）",self.delay); form.addRow("服务状态",self.server_state)
        row=QHBoxLayout(); row.addWidget(save); row.addWidget(start); row.addWidget(stop); form.addRow("",row); layout.addWidget(card); layout.addStretch()
        ai_card=QFrame(); ai_card.setObjectName("card"); ai_form=QFormLayout(ai_card)
        self.ai_base_url=QLineEdit(saved.get("ai_base_url","https://api.deepseek.com/v1")); self.ai_model=QLineEdit(saved.get("ai_model","deepseek-chat")); self.ai_key=QLineEdit(); self.ai_key.setEchoMode(QLineEdit.Password); self.ai_key.setPlaceholderText("已保存" if saved.get("ai_api_key") else "填写 API Key")
        self.ai_temperature=QDoubleSpinBox(); self.ai_temperature.setRange(0,2); self.ai_temperature.setSingleStep(.1); self.ai_temperature.setValue(float(saved.get("ai_temperature",.7)))
        self.analysis_prompt=QTextEdit(saved.get("analysis_prompt",DEFAULT_ANALYSIS_PROMPT)); self.analysis_prompt.setMinimumHeight(150)
        self.rewrite_prompt=QTextEdit(saved.get("rewrite_prompt",DEFAULT_REWRITE_PROMPT)); self.rewrite_prompt.setMinimumHeight(140)
        test_ai=QPushButton("测试 AI 连接"); reset_prompt=QPushButton("恢复默认提示词")
        ai_form.addRow("AI API 地址",self.ai_base_url); ai_form.addRow("API Key",self.ai_key); ai_form.addRow("模型名称",self.ai_model); ai_form.addRow("温度",self.ai_temperature); ai_form.addRow("视频拆解提示词",self.analysis_prompt); ai_form.addRow("仿写提示词",self.rewrite_prompt)
        ai_buttons=QHBoxLayout(); ai_buttons.addWidget(test_ai); ai_buttons.addWidget(reset_prompt); ai_form.addRow("",ai_buttons); layout.insertWidget(layout.count()-1,ai_card)
        login.clicked.connect(self.login_douyin); clear_login.clicked.connect(self.clear_douyin_login)
        test_ai.clicked.connect(self.test_ai); reset_prompt.clicked.connect(lambda: (self.analysis_prompt.setPlainText(DEFAULT_ANALYSIS_PROMPT),self.rewrite_prompt.setPlainText(DEFAULT_REWRITE_PROMPT)))
        save.clicked.connect(self.save_settings); start.clicked.connect(self.test_server); stop.clicked.connect(self.stop_server); return page

    def _append(self, widget, values):
        row=widget.rowCount(); widget.insertRow(row)
        for col,value in enumerate(values): widget.setItem(row,col,QTableWidgetItem(str(value or "")))

    def on_page_changed(self,index):
        self.stack.setCurrentIndex(index); self.refresh_all()

    def refresh_all(self):
        metrics=self.db.dashboard()
        for key,label in getattr(self,"kpis",{}).items(): label.setText(str(metrics[key]))
        self.refresh_task_filters()
        if hasattr(self,"task_table"): self.refresh_tasks()
        if hasattr(self,"lead_table"): self.refresh_leads()
        if hasattr(self,"video_table"): self.refresh_videos()
        if hasattr(self,"material_table"): self.refresh_materials()
        if hasattr(self,"rule_table"): self.refresh_rules()
        if hasattr(self,"log_table"): self.refresh_logs()
        if hasattr(self,"export_task"): self.refresh_export_tasks()

    def refresh_task_filters(self):
        tasks=self.db.list_tasks()
        for name in ("lead_task","video_task","material_task","log_task"):
            combo=getattr(self,name,None)
            if not combo: continue
            current=combo.currentData(); combo.blockSignals(True); combo.clear(); combo.addItem("全部任务",None)
            for task in tasks:
                combo.addItem(f"#{task['id']}  {shorten(task['keyword'],18)}",task["id"])
            index=combo.findData(current); combo.setCurrentIndex(index if index>=0 else 0); combo.blockSignals(False)

    def refresh_tasks(self):
        self.task_table.setRowCount(0)
        for r in self.db.list_tasks():
            progress=f"{r['videos_scanned']} 视频 · {r['comments_scanned']} 评论"
            self._append(self.task_table,[f"#{r['id']}",r["keyword"],r["target"],r["status"],progress,r["leads_found"],r["updated_at"],shorten(r["error"],30)])
            if r["error"]: self.task_table.item(self.task_table.rowCount()-1,7).setToolTip(r["error"])

    def refresh_leads(self):
        self.lead_table.setRowCount(0); keyword=self.lead_keyword.text().strip() if hasattr(self,"lead_keyword") else ""; level=self.lead_level.currentText() if hasattr(self,"lead_level") else ""; level="" if level.startswith("全部") else level
        task_id=self.lead_task.currentData() if hasattr(self,"lead_task") else None; status=self.lead_status.currentText() if hasattr(self,"lead_status") else ""; status="" if status.startswith("全部") else status
        for r in self.db.list_leads(keyword,level,task_id=task_id,status=status):
            evidence=self.db.lead_evidence(r["id"]); preview=shorten(evidence[0]["comment_text"],32) if evidence else ""; matched=shorten(evidence[0]["matched"],18) if evidence else ""
            row=self.lead_table.rowCount(); self.lead_table.insertRow(row)
            values=[f"{r['level']} · {r['score']}分",shorten(r["nickname"],12),r["keyword"],preview,matched,r["status"]]
            for col,value in enumerate(values): self.lead_table.setItem(row,col,QTableWidgetItem(str(value or "")))
            if evidence:
                self.lead_table.item(row,3).setToolTip(evidence[0]["comment_text"])
                self.lead_table.item(row,4).setToolTip(evidence[0]["matched"])
            self.lead_table.item(row,1).setToolTip(r["nickname"])
            actions=QWidget(); box=QHBoxLayout(actions); box.setContentsMargins(0,0,0,0); box.setSpacing(4)
            box.addWidget(icon_button("ⓘ","查看客户详情",lambda _=False,lead_id=r["id"]:self.show_lead_detail(lead_id)))
            box.addWidget(icon_button("↗","访问公开主页",lambda _=False,url=r["profile_url"]:QDesktopServices.openUrl(QUrl(url))))
            box.addWidget(icon_button("✎","修改客户状态",lambda _=False,lead_id=r["id"],status=r["status"]:self.change_lead_status(lead_id,status)))
            box.addStretch(); self.lead_table.setCellWidget(row,6,actions)

    def refresh_videos(self):
        self.video_table.setRowCount(0); task_id=self.video_task.currentData() if hasattr(self,"video_task") else None; keyword=self.video_search.text().strip() if hasattr(self,"video_search") else ""
        state=self.video_analysis.currentText() if hasattr(self,"video_analysis") else ""; analyzed={"已拆解":"yes","未拆解":"no"}.get(state,"")
        for r in self.db.list_videos(task_id=task_id,keyword=keyword,analyzed=analyzed):
            row=self.video_table.rowCount(); self.video_table.insertRow(row)
            performance=f"赞 {r['digg_count'] or 0} · 藏 {r['collect_count'] or 0} · 评 {r['comment_count'] or 0}"
            values=[shorten(r["title"],38),r["author_name"],r["keyword"],performance,r["qualified_count"],"已拆解" if r["analysis"] else "未拆解"]
            for col,value in enumerate(values): self.video_table.setItem(row,col,QTableWidgetItem(str(value or "")))
            actions=QWidget(); box=QHBoxLayout(actions); box.setContentsMargins(0,0,0,0); box.setSpacing(4)
            box.addWidget(icon_button("ⓘ","查看视频详情",lambda _=False,x=r["aweme_id"]:self.show_video_detail(x)))
            box.addWidget(icon_button("▶","查看原视频",lambda _=False,url=r["url"]:QDesktopServices.openUrl(QUrl(url))))
            box.addWidget(icon_button("✨","拆解与仿写",lambda _=False,x=r["aweme_id"]:self.start_video_workflow(x)))
            box.addStretch(); self.video_table.setCellWidget(row,6,actions)

    def refresh_materials(self):
        self.material_table.setRowCount(0); keyword=self.material_search.text().strip(); task_id=self.material_task.currentData() if hasattr(self,"material_task") else None
        state=self.material_rewrite.currentText() if hasattr(self,"material_rewrite") else ""; rewritten={"已仿写":"yes","未仿写":"no"}.get(state,"")
        for material in self.db.list_materials(keyword,task_id=task_id,rewritten=rewritten):
            row=self.material_table.rowCount(); self.material_table.insertRow(row)
            performance=f"赞 {material['digg_count']} / 藏 {material['collect_count']} / 评 {material['comment_count']}"
            keyword_tags=material["keyword"] + (f" · {material['material_tags']}" if material["material_tags"] else "")
            for col,value in enumerate([shorten(material["title"],42),shorten(keyword_tags,24),performance,"已仿写" if material["rewrite"] else "未仿写"]): self.material_table.setItem(row,col,QTableWidgetItem(str(value or "")))
            self.material_table.item(row,1).setToolTip(keyword_tags)
            actions=QWidget(); box=QHBoxLayout(actions); box.setContentsMargins(0,0,0,0); box.setSpacing(4)
            box.addWidget(icon_button("ⓘ","查看存档详情",lambda _=False,x=material["aweme_id"]:self.show_video_detail(x)))
            box.addWidget(icon_button("✨","继续仿写",lambda _=False,x=material["aweme_id"]:self.start_video_rewrite(x)))
            box.addWidget(icon_button("✎","编辑标签和备注",lambda _=False,x=material["aweme_id"]:self.edit_material(x)))
            box.addWidget(icon_button("⌫","移出素材库",lambda _=False,x=material["aweme_id"]:self.remove_material(x)))
            box.addStretch(); self.material_table.setCellWidget(row,4,actions)

    def edit_material(self,aweme_id):
        material=self.db.get_video(aweme_id); tags,ok=QInputDialog.getText(self,"素材标签","标签：",text=material["material_tags"])
        if not ok:return
        note,ok=QInputDialog.getMultiLineText(self,"素材备注","备注：",material["material_note"])
        if ok:self.db.update_video_ai(aweme_id,material_tags=tags,material_note=note);self.refresh_materials()

    def remove_material(self,aweme_id):
        if QMessageBox.question(self,"移出素材库","只移出素材库，已保存的拆解结果仍保留。确定继续吗？")==QMessageBox.Yes:
            self.db.update_video_ai(aweme_id,archived=0); self.refresh_materials()

    def show_text_dialog(self,title,text):
        dialog=QDialog(self); dialog.setWindowTitle(title); dialog.resize(820,620); layout=QVBoxLayout(dialog); editor=QTextEdit(); editor.setReadOnly(True); editor.setPlainText(text); close=QPushButton("关闭"); close.clicked.connect(dialog.accept); layout.addWidget(editor,1); layout.addWidget(close); dialog.exec()

    def show_markdown_dialog(self,title,markdown,aweme_id=None,allow_rewrite=False):
        dialog=QDialog(self); dialog.setWindowTitle(title); dialog.resize(900,700); layout=QVBoxLayout(dialog)
        viewer=QTextBrowser(); viewer.setOpenExternalLinks(True); viewer.setMarkdown(markdown or "暂无内容")
        buttons=QHBoxLayout(); copy=QPushButton("复制 Markdown"); copy.clicked.connect(lambda:QApplication.clipboard().setText(markdown or "")); buttons.addWidget(copy)
        if allow_rewrite and aweme_id:
            rewrite=QPushButton("继续仿写"); rewrite.clicked.connect(lambda:(dialog.accept(),self.start_video_rewrite(aweme_id))); buttons.addWidget(rewrite)
        buttons.addStretch(); close=QPushButton("关闭"); close.clicked.connect(dialog.accept); buttons.addWidget(close)
        layout.addWidget(viewer,1); layout.addLayout(buttons); dialog.exec()

    def show_lead_detail(self,lead_id):
        with self.db.connect() as c: lead=c.execute("SELECT * FROM leads WHERE id=?",(lead_id,)).fetchone()
        evidence=self.db.lead_evidence(lead_id)
        text=f"昵称：{lead['nickname']}\n完整公开用户 ID：{lead['user_id']}\n意向：{lead['level']}（{lead['score']}分）\n公开主页：{lead['profile_url']}\n\n"
        text+="\n\n".join(f"原评论：{e['comment_text']}\n来源视频：{e['video_title']}\n命中规则：{e['matched']}\n视频地址：{e['video_url']}" for e in evidence)
        self.show_text_dialog("客户详情",text)

    def change_lead_status(self,lead_id,current):
        statuses=["待跟进","跟进中","已联系","有意向","已成交","无效"]
        selected,ok=QInputDialog.getItem(self,"修改客户状态","选择新状态：",statuses,max(statuses.index(current) if current in statuses else 0,0),False)
        if ok:
            self.db.update_lead_status(lead_id,selected); self.refresh_leads(); self.refresh_export_count()

    def show_video_detail(self,aweme_id):
        video=self.db.get_video(aweme_id); text=f"# {video['title']}\n\n- **作者**：{video['author_name']}\n- **关键词**：{video['keyword']}\n- **点赞 / 收藏 / 评论**：{video['digg_count']} / {video['collect_count']} / {video['comment_count']}\n- **原视频**：[{video['url']}]({video['url']})\n\n## 口播稿\n\n{video['transcript'] or '尚未拆解'}\n\n## 拆解结果\n\n{video['analysis'] or '尚未拆解'}\n\n## 仿写结果\n\n{video['rewrite'] or '尚未仿写'}"
        self.show_markdown_dialog("视频详情",text,aweme_id,bool(video["analysis"]))

    def start_video_workflow(self,aweme_id):
        video=self.db.get_video(aweme_id)
        if video["analysis"]:
            self.show_markdown_dialog("视频拆解结果",video["analysis"],aweme_id,True)
        else:
            self.start_video_ai(aweme_id)

    def start_video_ai(self,aweme_id):
        if self.ai_worker and self.ai_worker.isRunning(): QMessageBox.warning(self,"处理中","已有视频任务正在运行"); return
        self.ai_worker=VideoAIWorker(self,aweme_id); self.ai_progress=AIProgressDialog("视频拆解进度",self.ai_worker,self); self.ai_worker.message.connect(self.ai_progress.update_step); self.ai_worker.message.connect(lambda text:self.statusBar().showMessage(text)); self.ai_worker.failed.connect(lambda text:self.finish_ai_failed("拆解失败",text)); self.ai_worker.completed.connect(lambda text:self.finish_analysis(aweme_id,text)); self.ai_progress.show(); self.ai_worker.start()

    def start_video_rewrite(self,aweme_id):
        requirements,ok=QInputDialog.getMultiLineText(self,"仿写要求","请输入本次特殊要求：","改写为当前行业的60秒口播，语言口语化，结尾引导咨询。")
        if not ok:return
        self.ai_worker=VideoAIWorker(self,aweme_id,"rewrite",requirements); self.ai_progress=AIProgressDialog("视频仿写进度",self.ai_worker,self); self.ai_worker.message.connect(self.ai_progress.update_step); self.ai_worker.failed.connect(lambda text:self.finish_ai_failed("仿写失败",text)); self.ai_worker.completed.connect(lambda text:self.finish_rewrite(aweme_id,text)); self.ai_progress.show(); self.ai_worker.start()

    def close_ai_progress(self):
        if self.ai_progress:self.ai_progress.timer.stop();self.ai_progress.close();self.ai_progress=None

    def finish_ai_failed(self,title,text):
        self.close_ai_progress()
        if text!="用户已取消":QMessageBox.warning(self,title,text)

    def finish_analysis(self,aweme_id,text):
        self.close_ai_progress(); self.refresh_videos(); self.refresh_materials(); self.show_markdown_dialog("拆解完成",text,aweme_id,True)

    def finish_rewrite(self,aweme_id,text):
        self.close_ai_progress(); self.refresh_videos(); self.refresh_materials(); self.show_markdown_dialog("仿写完成",text,aweme_id,False)

    def refresh_logs(self):
        self.log_table.setRowCount(0); task_id=self.log_task.currentData() if hasattr(self,"log_task") else None
        status=self.log_status.currentText() if hasattr(self,"log_status") else ""; status="" if status.startswith("全部") else status
        for r in self.db.list_logs(task_id,status):
            task_name=f"#{r['task_id']} {shorten(r['task_keyword'],10)}" if r["task_id"] else "系统"
            display_status={"ok":"成功","error":"失败"}.get(r["status"],r["status"])
            self._append(self.log_table,[task_name,r["stage"],display_status,r["found"],shorten(r["message"] or r["target"],60),r["created_at"]])

    def refresh_rules(self):
        self.rule_table.setRowCount(0)
        for rule in self.db.list_rules():
            row=self.rule_table.rowCount(); self.rule_table.insertRow(row)
            for col,value in enumerate([rule["id"],rule["category"],rule["weight"],rule["terms"],"启用" if rule["enabled"] else "停用"]): self.rule_table.setItem(row,col,QTableWidgetItem(str(value)))
            actions=QWidget(); box=QHBoxLayout(actions); box.setContentsMargins(0,0,0,0); box.setSpacing(4)
            box.addWidget(icon_button("✎","编辑规则",lambda _=False,rid=rule["id"]:self.edit_rule_by_id(rid)))
            box.addWidget(icon_button("⏯","启用或停用",lambda _=False,rid=rule["id"]:self.toggle_rule_by_id(rid)))
            box.addWidget(icon_button("⌫","删除规则",lambda _=False,rid=rule["id"]:self.delete_rule_by_id(rid)))
            box.addStretch(); self.rule_table.setCellWidget(row,5,actions)

    def selected_rule(self):
        row=self.rule_table.currentRow()
        if row<0: QMessageBox.warning(self,"意向规则","请先选择一条规则"); return None
        rule_id=int(self.rule_table.item(row,0).text())
        return next((r for r in self.db.list_rules() if r["id"]==rule_id),None)

    def rule_inputs(self,rule=None):
        category,ok=QInputDialog.getText(self,"规则分类","分类名称：",text=rule["category"] if rule else "")
        if not ok or not category.strip(): return None
        weight,ok=QInputDialog.getInt(self,"规则分值","命中分值：",rule["weight"] if rule else 3,1,20)
        if not ok:return None
        terms,ok=QInputDialog.getMultiLineText(self,"规则关键词","用 | 分隔多个关键词：",rule["terms"] if rule else "")
        return (category.strip(),weight,terms.strip()) if ok and terms.strip() else None

    def add_rule(self):
        values=self.rule_inputs()
        if values:self.db.save_rule(*values);self.refresh_rules()

    def edit_rule(self):
        rule=self.selected_rule()
        if not rule:return
        values=self.rule_inputs(rule)
        if values:self.db.save_rule(*values,bool(rule["enabled"]),rule["id"]);self.refresh_rules()

    def rule_by_id(self,rule_id):
        return next((rule for rule in self.db.list_rules() if rule["id"]==rule_id),None)

    def edit_rule_by_id(self,rule_id):
        rule=self.rule_by_id(rule_id); values=self.rule_inputs(rule) if rule else None
        if values:self.db.save_rule(*values,bool(rule["enabled"]),rule_id);self.refresh_rules()

    def toggle_rule_by_id(self,rule_id):
        rule=self.rule_by_id(rule_id)
        if rule:self.db.save_rule(rule["category"],rule["weight"],rule["terms"],not bool(rule["enabled"]),rule_id);self.refresh_rules()

    def delete_rule_by_id(self,rule_id):
        rule=self.rule_by_id(rule_id)
        if rule and QMessageBox.question(self,"删除规则",f"确定删除“{rule['category']}”吗？")==QMessageBox.Yes:self.db.delete_rule(rule_id);self.refresh_rules()

    def toggle_rule(self):
        rule=self.selected_rule()
        if rule:self.db.save_rule(rule["category"],rule["weight"],rule["terms"],not bool(rule["enabled"]),rule["id"]);self.refresh_rules()

    def delete_rule(self):
        rule=self.selected_rule()
        if rule and QMessageBox.question(self,"删除规则",f"确定删除“{rule['category']}”吗？")==QMessageBox.Yes:self.db.delete_rule(rule["id"]);self.refresh_rules()

    def refresh_export_tasks(self):
        current=self.export_task.currentData(); self.export_task.blockSignals(True); self.export_task.clear(); self.export_task.addItem("全部任务",None)
        for task in self.db.list_tasks():self.export_task.addItem(f"#{task['id']} {task['keyword']}（{task['status']}）",task["id"])
        index=self.export_task.findData(current); self.export_task.setCurrentIndex(max(index,0)); self.export_task.blockSignals(False); self.refresh_export_count()

    def export_filters(self):
        level="" if self.export_level.currentText()=="全部" else self.export_level.currentText(); status="" if self.export_status.currentText()=="全部" else self.export_status.currentText()
        return self.export_task.currentData(),level,status

    def refresh_export_count(self):
        if not hasattr(self,"export_count"):return
        task_id,level,status=self.export_filters(); self.export_count.setText(f"预计导出 {len(self.db.list_leads(level=level,task_id=task_id,status=status))} 条")

    def save_settings(self):
        if self.order_number.text().strip(): self.settings.set_secret("order_number",self.order_number.text().strip()); self.order_number.clear(); self.order_number.setPlaceholderText("已保存")
        if self.ai_key.text(): self.settings.set_secret("ai_api_key",self.ai_key.text()); self.ai_key.clear(); self.ai_key.setPlaceholderText("已保存")
        self.settings.update(request_delay=self.delay.value(),ai_base_url=self.ai_base_url.text().strip(),ai_model=self.ai_model.text().strip(),ai_temperature=self.ai_temperature.value(),ai_timeout=90,analysis_prompt=self.analysis_prompt.toPlainText(),rewrite_prompt=self.rewrite_prompt.toPlainText()); QMessageBox.information(self,"设置","设置已保存到本机。")

    def test_ai(self):
        if self.ai_key.text(): self.settings.set_secret("ai_api_key",self.ai_key.text()); self.ai_key.clear()
        try:
            result=OpenAICompatibleClient(self.ai_base_url.text().strip(),self.settings.get_secret("ai_api_key"),self.ai_model.text().strip(),30,0).chat("只回复：连接成功")
            QMessageBox.information(self,"AI 连接",result[:300])
        except Exception as exc: QMessageBox.warning(self,"AI 连接失败",str(exc))

    def login_douyin(self):
        dialog=DouyinLoginDialog(self)
        if dialog.exec() == QDialog.Accepted and dialog.cookie_value:
            self.settings.set_secret("douyin_cookie", dialog.cookie_value)
            self.login_state.setText("已登录")
            QMessageBox.information(self,"抖音登录","登录状态已加密保存到本机。")

    def clear_douyin_login(self):
        self.settings.clear_secret("douyin_cookie")
        self.login_state.setText("未登录")
        QMessageBox.information(self,"抖音登录","本机保存的抖音登录状态已清除。")

    def test_server(self):
        self.save_settings(); ok,message=self.server.start(self.settings.get_secret("order_number")); self.server_state.setText(message); (QMessageBox.information if ok else QMessageBox.warning)(self,"本地服务",message)

    def stop_server(self): self.server.stop(); self.server_state.setText("已停止")

    def start_task(self):
        keyword=self.keyword.text().strip()
        if not keyword: QMessageBox.warning(self,"缺少关键词","请输入行业、产品或服务关键词。"); return
        if not self.settings.get_secret("order_number"): QMessageBox.warning(self,"缺少授权","请先到系统设置填写并保存订单授权号。"); self.nav.setCurrentRow(8); return
        task_id=self.db.create_task(keyword,self.target.value(),self.max_videos.value(),self.comments_per_video.value(),self.include_replies.isChecked())
        self.worker=AcquisitionWorker(self.db,self.server,self.settings,task_id); self.worker.progress.connect(self.on_progress); self.worker.message.connect(self.task_status.setText); self.worker.failed.connect(self.on_failed); self.worker.completed.connect(self.on_completed); self.worker.start(); self.start_btn.setEnabled(False); self.task_status.setText("正在启动本地服务…")

    def on_progress(self,current,total,leads): self.task_progress.setMaximum(max(total,1)); self.task_progress.setValue(current); self.task_status.setText(f"已扫描 {current}/{total} 个视频，当前客户 {leads} 人"); self.refresh_all()
    def on_failed(self,message): self.start_btn.setEnabled(True); self.task_status.setText("失败："+message); QMessageBox.warning(self,"任务失败",message); self.refresh_all()
    def on_completed(self): self.start_btn.setEnabled(True); self.task_status.setText("任务完成"); self.refresh_all(); QMessageBox.information(self,"完成","获客任务已完成，可在客户池查看并导出。")

    def do_export(self):
        filename=f"抖音意向客户-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"; chosen,_=QFileDialog.getSaveFileName(self,"导出 Excel",str(self.paths.exports/filename),"Excel 工作簿 (*.xlsx)")
        if not chosen:return
        task_id,level,status=self.export_filters(); output=export_leads(self.db,Path(chosen),level=level,task_id=task_id,status=status); QMessageBox.information(self,"导出完成",str(output))

    def open_lead_profile(self,row,column):
        item=self.lead_table.item(row,8)
        if item and item.text(): QDesktopServices.openUrl(QUrl(item.text()))

    def closeEvent(self,event):
        if self.worker and self.worker.isRunning(): self.worker.cancel(); self.worker.wait(3000)
        self.server.stop(); event.accept()
