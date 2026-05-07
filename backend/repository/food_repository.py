from sqlalchemy.orm import Session
from datetime import date
from repository.base_repository import BaseRepository
from repository.models import Food, FoodRecord


class FoodRepository(BaseRepository):
    """食物仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, Food)


class FoodRecordRepository(BaseRepository):
    """饮食记录仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, FoodRecord)
    
    def get_by_date(self, date: date):
        """根据日期获取饮食记录"""
        return self.db.query(self.model).filter(self.model.date == date).all()