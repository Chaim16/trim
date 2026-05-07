from utils.database import engine, Base
from repository.models import WeightRecord, Food, FoodRecord, ExerciseRecord


def init_database():
    """初始化数据库，创建表结构"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表结构创建成功")


if __name__ == "__main__":
    init_database()