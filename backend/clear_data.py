#!/usr/bin/env python3
"""
清空数据库所有数据
"""

from repository.models import WeightRecord, Food, FoodRecord, ExerciseRecord
from utils.database import get_db_session


def clear_all_data():
    """清空所有数据库表中的数据"""
    try:
        with get_db_session() as db:
            # 删除所有表中的数据
            db.query(ExerciseRecord).delete()
            db.query(FoodRecord).delete()
            db.query(WeightRecord).delete()
            # 保留食物数据，因为是初始化数据
            # db.query(Food).delete()
            
            # 提交事务
            db.commit()
        print("✅ 数据清空成功！")
    except Exception as e:
        print(f"❌ 数据清空失败: {e}")


if __name__ == "__main__":
    clear_all_data()
