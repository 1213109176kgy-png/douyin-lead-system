class BaseConfig(object):
    # MoreAPI 版本号
    VERSIONS = "5.3.1"
    # DEBUG模式
    DEBUG = False
    # 控制应用程序是否在文件更改时自动重新加载
    AUTO_RELOAD = False
    # 未捕获和处理异常时的错误响应格式
    FALLBACK_ERROR_FORMAT = "json"
    # 关闭OAS
    OAS = False
    # 开启keep-alive
    KEEP_ALIVE = True
    # 保持 TCP 连接打开的时间 （秒）
    KEEP_ALIVE_TIMEOUT = 120
    # 请求缓冲区大小
    REQUEST_BUFFER_SIZE = 65536
    # 请求的大小（字节），默认值为 100 MB
    REQUEST_MAX_SIZE = 100000000
    # 请求标头的大小 （字节），默认为 8192 字节
    REQUEST_MAX_HEADER_SIZE = 8192
    # 请求到达需要多长时间 （秒）
    REQUEST_TIMEOUT = 600
    # 响应处理需要多长时间 （秒）
    RESPONSE_TIMEOUT = 600
    # sanic项目后台刷新时间
    SYSTEM_REFRESH_TIMEOUT = 60
    # 是否启用日志记录
    ENABLE_LOGGING = True
    # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = "INFO"
    # 是否记录到文件  建议False不记录
    LOG_TO_FILE = False
    # 日志文件保留天数
    LOG_RETENTION_DAYS = 3
    # 日志文件大小限制（MB）
    LOG_FILE_SIZE_LIMIT = 2
    # 程序API基础路径
    API_BASIC_PATH = "api"
    # 是否开启API接口文档
    API_DOC = True
    # 接口文档路径
    API_DOC_PATH = "docs"
    # API网络请求超时时间
    API_RE_REQUEST_TIMEOUT = 15
    # 在API接口响应头中返回平台响应头
    RECEIVE_HEADERS = True
    # MoreAPI订单号 必填 不然无法启动
    MOREAPI_ORDER_NUM = ""

    # API请求密码 留空表示不限制
    API_PWD = ""
    # API请求密码字段(在请求体或请求URL参数中加入pwd=xxx或pwd:xxx)
    PWD_NAME = "pwd"

    # 小红书签名服务地址,(算法源码位于：application/src/xhs/client/args/，可自行搭建服务)
    XHS_X_S_ORIGIN = "http://127.0.0.1:5008/"

    # 小红书接口默认使用匿名cookie
    XHS_NOTE_DETAIL_USE_ANYACCOUNT = True

    # 国内代理（为空则不使用代理）  http://用户名:密码@ip或服务地址:端口号  |  socks5://用户名:密码@ip或服务地址:端口号  |  http://ip:port  ..
    CHINESE_PROXY_URL = ""

    # 海外代理（为空则不使用代理）  http://用户名:密码@ip或服务地址:端口号  |  socks5://用户名:密码@ip或服务地址:端口号  |  http://ip:port  ..
    OVERSEAS_PROXY_URL = ""

    # GOOGLE API官方秘钥
    GOOGLE_API_KEY = ""

    # REDIS代理获取地址,使用redis获取代理IP需设置`CHINESE_PROXY_URL`的值为：redis
    REDIS_URL = ""


