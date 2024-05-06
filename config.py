# config.py
import os

# 根目录（项目的基础目录）
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库相关路径
SQL_DB_PATH = os.path.join(ROOT_DIR, "data_storage", "sql_database.db")
# 其他路径配置
LOG_DIR = os.path.join(ROOT_DIR, "logs")
