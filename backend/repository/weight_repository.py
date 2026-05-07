from sqlalchemy.orm import Session
from repository.base_repository import BaseRepository
from repository.models import WeightRecord


class WeightRepository(BaseRepository):
    """体重记录仓库"""
    
    def __init__(self, db: Session):
        super().__init__(db, WeightRecord)
    
    def get_all(self):
        """获取所有体重记录"""
        return self.db.query(self.model).order_by(self.model.date.desc()).all()
    
    def get_latest(self):
        """获取最新的体重记录"""
        return self.db.query(self.model).order_by(self.model.date.desc()).first()
    
    def get_trend(self):
        """获取体重趋势数据"""
        return self.db.query(self.model).order_by(self.model.date).all()