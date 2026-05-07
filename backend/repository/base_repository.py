from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta


class BaseRepository:
    """基础仓库类"""
    
    def __init__(self, db: Session, model: DeclarativeMeta):
        self.db = db
        self.model = model
    
    def get_all(self):
        """获取所有记录"""
        return self.db.query(self.model).all()
    
    def get_by_id(self, id: int):
        """根据ID获取记录"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, instance):
        """创建记录"""
        self.db.add(instance)
        self.db.commit()
        return instance
    
    def delete(self, id: int):
        """删除记录"""
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False
    
    def update(self, id: int, data: dict):
        """更新记录"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.db.commit()
            return instance
        return None