from utils.database import get_db_session
from repository.models import Food


def init_food_data():
    """初始化食物数据"""
    # 常见食物数据
    food_data = [
        {"name": "米饭", "calorie_per_100g": 116},
        {"name": "鸡胸肉", "calorie_per_100g": 165},
        {"name": "鸡蛋", "calorie_per_100g": 155},
        {"name": "牛奶", "calorie_per_100g": 42},
        {"name": "苹果", "calorie_per_100g": 52},
        {"name": "香蕉", "calorie_per_100g": 89},
        {"name": "西兰花", "calorie_per_100g": 34},
        {"name": "胡萝卜", "calorie_per_100g": 41},
        {"name": "土豆", "calorie_per_100g": 77},
        {"name": "牛肉", "calorie_per_100g": 250}
    ]
    
    with get_db_session() as db:
        # 检查是否已有食物数据
        existing_foods = db.query(Food).count()
        if existing_foods > 0:
            print("食物数据已存在，跳过初始化")
            return
        
        # 添加食物数据
        for food_info in food_data:
            food = Food(
                name=food_info["name"],
                calorie_per_100g=food_info["calorie_per_100g"]
            )
            db.add(food)
        
        db.commit()
        print("食物数据初始化成功")


if __name__ == "__main__":
    init_food_data()