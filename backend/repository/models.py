import time
from sqlalchemy import Column, Integer, inspect, String, Numeric, Date
from utils.database import Base


class BaseModel(Base):
    """基础模型"""

    __abstract__ = True
    id = Column(Integer(), primary_key=True, autoincrement=True)
    create_time = Column(Integer(), default=int(time.time()), comment="创建时间")
    update_time = Column(Integer(), default=int(time.time()), onupdate=int(time.time()),
                         comment="更新时间")

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class WeightRecord(BaseModel):
    """体重记录"""

    __tablename__ = "weight_record"

    date = Column(Date(), nullable=False, comment="日期")
    weight = Column(Numeric(5, 2), nullable=False, comment="体重")
    note = Column(String(255), nullable=True, comment="备注")


class Food(BaseModel):
    """食物列表"""

    __tablename__ = "food"

    name = Column(String(64), nullable=False, comment="食物名称")
    calorie_per_100g = Column(Numeric(6, 2), nullable=False, comment="每100克热量")


class FoodRecord(BaseModel):
    """饮食记录"""

    __tablename__ = "food_record"

    date = Column(Date(), nullable=False, comment="日期")
    food_id = Column(Integer(), nullable=True, comment="食物ID")
    food_name = Column(String(64), nullable=True, comment="食物名称")


class ExerciseRecord(BaseModel):
    """运动记录"""

    __tablename__ = "exercise_record"

    date = Column(Date(), nullable=False, comment="日期")
    exercise_name = Column(String(64), nullable=False, comment="运动名称")
    duration = Column(Numeric(4, 1), nullable=False, comment="运动时长")
    calorie = Column(Numeric(6, 2), nullable=False, comment="消耗热量")