# 抖音获客系统

一个面向 Windows 单机使用的抖音公开评论线索整理工具。它可以按行业、产品或服务关键词检索公开视频，分析公开评论中的咨询与购买意向，并将线索保存在本机、筛选管理及导出为 Excel。

## 产品介绍视频

▶️ **[点击前往哔哩哔哩观看完整产品介绍](https://www.bilibili.com/video/BV1tcGA6pEAN/)**

视频 BV 号：`BV1tcGA6pEAN`

## Windows 绿色版下载

不想配置 Python 环境的用户，可以前往 [GitHub Releases](https://github.com/1213109176kgy-png/douyin-lead-system/releases) 下载最新的 Windows 绿色免安装版，解压后运行 `DouyinLeadSystem.exe`。

## 主要功能

- 按关键词创建获客任务，设置目标客户数、视频数和评论数
- 自动整理公开视频与公开评论中的意向线索
- 客户池按任务、意向等级和跟进状态筛选
- 视频库查看互动数据、来源线索数及原视频
- 本地 Whisper 语音转文字，结合 OpenAI 兼容接口拆解和仿写视频
- 爆款素材库保存拆解结果、标签、备注和仿写内容
- 自定义意向关键词、分值及启停状态
- 按任务、等级、状态导出 Excel
- Cookie、API Key 与授权信息使用 Windows DPAPI 加密后仅保存在本机

## 项目结构

- `app/`：Windows 桌面客户端、数据管理、评分、导出和 AI 工作流
- `server/APIServer_v5.3.1/`：本地多平台接口服务
- `tests/`：自动化测试
- `scripts/`：本地联调与界面验证脚本

## 开发环境

- Windows 10/11
- Python 3.10+
- PySide6
- faster-whisper

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
python -m app.main
```

## 配置

在“系统设置”中配置：

1. 第三方本地接口的订单授权号
2. 抖音网页登录状态
3. DeepSeek 或其他 OpenAI 兼容 API 地址、API Key 与模型名
4. 视频拆解、仿写提示词

所有业务数据默认保存在程序目录的 `data/` 中，该目录已被 Git 忽略。

## 隐私与合规

- 仅处理用户主动指定范围内的公开内容。
- 请遵守平台服务条款、robots 约束、当地隐私和数据保护法律。
- 不要用于骚扰、群发营销、绕过访问控制或收集非公开个人信息。
- 使用者应自行确认其采集、保存、联系及导出行为具有合法依据。

## 测试

```powershell
pytest -q
```

当前测试覆盖数据库去重、任务筛选、素材库、规则、导出、接口冷启动重试和视频 AI 基础流程。

## 许可证

本项目采用 [MIT License](LICENSE)。

## 联系作者

如果你在部署或使用过程中遇到问题，可以扫描下方二维码添加作者微信：

<p align="left">
  <img src="assets/微信二维码.jpg" alt="作者微信二维码" width="360">
</p>
