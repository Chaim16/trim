from sqlalchemy.orm import Session
from datetime import date
from repository.base_repository import BaseRepository
from repository.models import WeightRecord, FoodRecord, ExerciseRecord


class DashboardRepository(BaseRepository):
    """首页数据仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, WeightRecord)  # 以 WeightRecord 为默认模型
    
    def get_current_weight(self):
        """获取当前体重"""
        latest_weight = self.db.query(WeightRecord).order_by(WeightRecord.date.desc()).first()
        return latest_weight.weight if latest_weight else 0
    
    def get_today_food_calorie(self):
        """获取今日饮食热量（已移除）"""
        return 0
    
    def get_today_exercise_calorie(self):
        """获取今日运动消耗"""
        today = date.today()
        today_exercise_calories = self.db.query(ExerciseRecord).filter(ExerciseRecord.date == today).all()
        return sum(float(record.calorie) for record in today_exercise_calories)
    
    def get_weight_trend(self):
        """获取体重趋势数据"""
        return self.db.query(WeightRecord).order_by(WeightRecord.date).all()