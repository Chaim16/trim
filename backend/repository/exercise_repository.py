from sqlalchemy.orm import Session
from datetime import date
from repository.base_repository import BaseRepository
from repository.models import ExerciseRecord


class ExerciseRepository(BaseRepository):
    """运动记录仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, ExerciseRecord)
    
    def get_by_date(self, date: date):
        """根据日期获取运动记录"""
        return self.db.query(self.model).filter(self.model.date == date).all()