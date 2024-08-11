from datetime import datetime
import logging
import os
from config import CRITICAL_PATHS, MONITORED_PATHS

class FIDShandler:
    def __init__(self, alarm_queue):
        self.rules = [
            self.detect_abnormal_login,
            self.detect_network_card_change,
            self.detect_config_change,
            self.critical_path_modification,
            self.critical_path_deletion,
        ]
        self.alarm_queue = alarm_queue

    def critical_path_modification(self, event):
        for path, risk in CRITICAL_PATHS.items():
            if event.event_type == 'modified' and event.src_path.startswith(path):
                return True, self.generate_message(risk, event, "modified")
            elif event.event_type == 'created' and event.src_path.startswith(path):
                return True, self.generate_message(risk, event, "created")
        return False, ""

    def critical_path_deletion(self, event):
        for path, risk in CRITICAL_PATHS.items():
            if event.event_type == 'deleted' and event.src_path.startswith(path):
                return True, self.generate_message(risk, event, "deleted")
        return False, ""

    def detect_abnormal_login(self, event):
        if event.src_path in ['/var/log/auth.log', '/var/log/secure']:
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'maximum authentication' in line:
                        return True, f"存在用户登录爆破的风险: {line.strip()}"
                    if 'Failed password' in line:
                        return True, f"失败的用户登录尝试: {line.strip()}"
                    if 'Accepted password' in line and 'root' in line:
                        return True, f"检测到Root用户登录: {line.strip()}"
        return False, ""

    def detect_network_card_change(self, event):
        if event.src_path in ['/etc/network/interfaces'] or 'ifcfg-' in event.src_path:
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if 'hwaddress' in line:
                        return True, f"检测到异常的Network和MAC地址更改: {line.strip()}"
        return False, ""

    def detect_config_change(self, event):
        if event.src_path in ['/etc/nginx/nginx.conf', '/etc/apache2/apache2.conf', '/etc/ssh/sshd_config']:
            with open(event.src_path, 'r') as f:
                content = f.read()
                if 'PermitRootLogin yes' in content:
                    return True, f"异常的系统核心文件修改（允许Root用户登录）: {event.src_path}"
                if 'listen 80' in content or 'listen 443' in content:
                    return True, f"Web server config changed: {event.src_path}"
        return False, ""

    def check_event(self, event):
        # 处理关键路径上的事件
        for rule in self.rules:
            match, message = rule(event)
            if match:
                logging.warning(message)
                self.send_file_log(event, message, 'alarms')
                return True, message

        # 处理一般监控路径上的事件
        for path in MONITORED_PATHS:
            if event.src_path.startswith(path):
                self.send_file_log(event, f"{event.src_path} 被 {event.event_type}，时间：{datetime.now()}", 'normal')
                return False, ""

    def send_file_log(self, event, message, type):
        file_info = self.get_file_info(event.src_path)
        alarm_data = {
            'type': type,
            "message": message,
            "file_info": file_info,
            "event_type": event.event_type,
            "event_path": event.src_path
        }
        self.alarm_queue.put(alarm_data)
        print(f"文件监控触发: {message}\n{file_info}")

    def generate_message(self, risk, event, action):
        return f"{risk} 文件被{action}: {event.src_path}"

    def get_file_info(self, file_path):
        info = {
            "path": file_path,
            "size": None,
            "owner": None,
            "content": None,
            "creation_time": None,
            "modification_time": None,
            "access_time": None
        }

        try:
            if os.path.isfile(file_path) and os.path.getsize(file_path) < 100 * 1024:  # 100KB
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    info["content"] = file.read()
            else:
                info["content"] = "文件过大或不存在，无法读取内容"
        except Exception as e:
            info["content"] = f"无法读取文件内容: {str(e)}"

        try:
            stat = os.stat(file_path)
            info["size"] = stat.st_size
            info["creation_time"] = self.format_time(stat.st_ctime)
            info["modification_time"] = self.format_time(stat.st_mtime)
            info["access_time"] = self.format_time(stat.st_atime)
            info["owner"] = self.get_file_owner(file_path)
        except Exception as e:
            info["error"] = f"无法获取文件详细信息: {str(e)}"

        return info

    def format_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_file_owner(self, file_path):
        try:
            stat = os.stat(file_path)
            uid = stat.st_uid
            return f"UID: {uid}"
        except Exception as e:
            return f"无法获取文件所有者: {str(e)}"
