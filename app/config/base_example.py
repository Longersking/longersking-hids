# config.py
import os

# 主机系统配置

# 数据库配置
mysql_username = "root"
mysql_password = "123456"
mysql_host = "localhost"
mysql_port = "3306"
mysql_db = "hids_db"

# HOST
ip = "127.0.0.1"
port = 8003


# 路径

# 根目录（项目的基础目录）
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库数据路径
SQL_DB_PATH = os.path.join(ROOT_DIR, "database")

# 日志路径
# LOG_DIR = os.path.join(ROOT_DIR, "logs")

# 工具路径
UTIL_DIR = os.path.join(ROOT_DIR,"utils")
# 主机工具路径
HOST_HANDLER_DIR = os.path.join(UTIL_DIR,"host_handler")




if __name__ == '__main__':
    # print(UTIL_DIR)
    print(HOST_HANDLER_DIR)


