from datetime import date
from repository.food_repository import FoodRepository, FoodRecordRepository
from repository.models import FoodRecord
from utils.database import get_db_session
from utils.logger import get_logger


class FoodService:
    """食物服务"""
    
    def __init__(self):
        self.logger = get_logger("food_service")
    
    def get_foods(self):
        """获取食物列表"""
        self.logger.info("开始获取食物列表")
        try:
            with get_db_session() as db:
                repo = FoodRepository(db)
                foods = repo.get_all()
                data = [
                    {
                        "id": food.id,
                        "name": food.name,
                        "calorie_per_100g": float(food.calorie_per_100g)
                    }
                    for food in foods
                ]
                self.logger.info(f"获取食物列表成功，共 {len(data)} 条记录")
                return data
        except Exception as e:
            self.logger.error(f"获取食物列表失败: {e}")
            raise


class FoodRecordService:
    """饮食记录服务"""
    
    def __init__(self):
        self.logger = get_logger("food_record_service")
    
    def get_food_records(self, date_str: str):
        """获取饮食记录"""
        self.logger.info(f"开始获取饮食记录: 日期={date_str}")
        try:
            with get_db_session() as db:
                repo = FoodRecordRepository(db)
                food_repo = FoodRepository(db)
                record_date = date.fromisoformat(date_str)
                records = repo.get_by_date(record_date)
                
                data = []
                for record in records:
                    if record.food_name:
                        food_name = record.food_name
                    elif record.food_id:
                        food = food_repo.get_by_id(record.food_id)
                        food_name = food.name if food else "未知食物"
                    else:
                        food_name = "未知食物"
                    
                    data.append({
                        "id": record.id,
                        "food_name": food_name,
                    })
                
                self.logger.info(f"获取饮食记录成功，共 {len(data)} 条记录")
                return data
        except Exception as e:
            self.logger.error(f"获取饮食记录失败: 日期={date_str}, 错误={e}")
            raise
    
    def add_food_record(self, date_str: str, food_id: int = None, food_name: str = None):
        """新增饮食记录"""
        self.logger.info(f"开始新增饮食记录: 日期={date_str}, 食物ID={food_id}, 食物名称={food_name}")
        try:
            with get_db_session() as db:
                food_repo = FoodRepository(db)
                record_repo = FoodRecordRepository(db)
                
                if food_id:
                    food = food_repo.get_by_id(food_id)
                    if not food:
                        self.logger.warning(f"食物不存在: ID={food_id}")
                        return False
                
                record_date = date.fromisoformat(date_str)
                new_record = FoodRecord(
                    date=record_date,
                    food_id=food_id,
                    food_name=food_name
                )
                
                record_repo.create(new_record)
                self.logger.info(f"新增饮食记录成功")
                return True
        except Exception as e:
            self.logger.error(f"新增饮食记录失败: {e}")
            raise
    
    def delete_food_record(self, id: int):
        """删除饮食记录"""
        self.logger.info(f"开始删除饮食记录: ID={id}")
        try:
            with get_db_session() as db:
                repo = FoodRecordRepository(db)
                success = repo.delete(id)
                if success:
                    self.logger.info(f"删除饮食记录成功: ID={id}")
                else:
                    self.logger.warning(f"饮食记录不存在: ID={id}")
                return success
        except Exception as e:
            self.logger.error(f"删除饮食记录失败: ID={id}, 错误={e}")
            raise