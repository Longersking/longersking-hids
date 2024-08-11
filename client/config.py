import os

# ws服务端URL
SERVER_URL = "ws://121.43.138.234:8003/ws"

# 定义关键文件和目录及其对应的风险提示信息
CRITICAL_PATHS = {
    '/bin': '可能被替换基本工具为恶意木马，例如 netstat, ps 等。',
    '/sbin': '可能被替换基本工具为恶意木马，例如 sshd, lsof, ss 等。',
    '/usr/bin': '可能被替换基本工具为恶意木马，例如 sshd, lsof, ss 等。',
    '/usr/sbin': '可能被替换基本工具为恶意木马，例如 sshd, lsof, ss 等。',
    '/etc/init.d': '修改开机启动任务，添加恶意脚本开机启动。',
    '/etc/cront.d': '修改计划任务，添加恶意脚本定时执行。',
    '/etc/crontab': '修改计划任务，添加恶意脚本定时执行。',
    '~/.ssh': '注入公钥，可能存在未授权的SSH访问。',
    '/etc/sysconfig': '修改iptables配置等，开放网络限制。',
    '/etc/ssh': '修改SSH配置，可能降低安全性。',
    '/var/log/auth.log': "用户登录日志",
    '/var/log/secure': "用户登录日志",
    '/etc/network/interfaces': "网卡接口文件",
    '/etc/nginx/nginx.conf': "web服务器Nginx配置文件",
    '/etc/apache2/apache2.conf': "Apache配置文件",
    '/etc/ssh/sshd_config': "SSH配置文件"
}

# 需要监控改动的文件路径
MONITORED_PATHS = [
    "/home/www/hids-new/client",
    # 添加更多路径
]

# HTTP 端口
HTTP_Ports = [80.8080,8003]
# HTTPS 端口
HTTPS_Ports = [443]
def get_config() -> dict:
    """
    get config from os type
    params:
        none
    return:
        config dict
    """
    if os.name == 'nt':
        return {
            "paths_to_monitor": ["W:\Temp"],
            "process_to_monitor": ["tcp", "udp", "ssh", "telnet"]
        }
    elif os.name == 'posix':
        return {
            "paths_to_monitor": ["/etc/passwd", "/etc/shadow", "/root/.bash_history", "/etc/init.d"],
            "process_to_monitor": ["tcp", "udp", "ssh", "telnet"]
        }
