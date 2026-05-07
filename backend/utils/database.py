from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 使用SQLite数据库
DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'trim.db')}"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 设置为True可以看到SQL语句
    connect_args={"check_same_thread": False}  # SQLite需要这个参数
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


@contextmanager
def get_db_session():
    """获取数据库会话的上下文管理器"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()