from datetime import date
from repository.weight_repository import WeightRepository
from repository.models import WeightRecord
from utils.database import get_db_session
from utils.logger import get_logger


class WeightService:
    """体重记录服务"""
    
    def __init__(self):
        self.logger = get_logger("weight_service")
    
    def get_weight_records(self):
        """获取体重记录列表"""
        self.logger.info("开始获取体重记录列表")
        try:
            with get_db_session() as db:
                repo = WeightRepository(db)
                records = repo.get_all()
                data = [
                    {
                        "id": record.id,
                        "date": record.date.isoformat(),
                        "weight": float(record.weight),
                        "note": record.note
                    }
                    for record in records
                ]
                self.logger.info(f"获取体重记录列表成功，共 {len(data)} 条记录")
                return data
        except Exception as e:
            self.logger.error(f"获取体重记录列表失败: {e}")
            raise
    
    def add_weight_record(self, date_str: str, weight: float, note: str = None):
        """新增体重记录"""
        self.logger.info(f"开始新增体重记录: 日期={date_str}, 体重={weight}, 备注={note}")
        try:
            with get_db_session() as db:
                repo = WeightRepository(db)
                record_date = date.fromisoformat(date_str)
                new_record = WeightRecord(
                    date=record_date,
                    weight=weight,
                    note=note
                )
                repo.create(new_record)
                self.logger.info("新增体重记录成功")
                return True
        except Exception as e:
            self.logger.error(f"新增体重记录失败: {e}")
            raise
    
    def delete_weight_record(self, id: int):
        """删除体重记录"""
        self.logger.info(f"开始删除体重记录: ID={id}")
        try:
            with get_db_session() as db:
                repo = WeightRepository(db)
                success = repo.delete(id)
                if success:
                    self.logger.info(f"删除体重记录成功: ID={id}")
                else:
                    self.logger.warning(f"体重记录不存在: ID={id}")
                return success
        except Exception as e:
            self.logger.error(f"删除体重记录失败: ID={id}, 错误={e}")
            raise
    
    def get_latest_weight(self):
        """获取最新的体重记录"""
        self.logger.info("开始获取最新的体重记录")
        try:
            with get_db_session() as db:
                repo = WeightRepository(db)
                record = repo.get_latest()
                weight = record.weight if record else 0
                self.logger.info(f"获取最新的体重记录成功: {weight}")
                return weight
        except Exception as e:
            self.logger.error(f"获取最新的体重记录失败: {e}")
            raise
    
    def get_weight_trend(self):
        """获取体重趋势数据"""
        self.logger.info("开始获取体重趋势数据")
        try:
            with get_db_session() as db:
                repo = WeightRepository(db)
                records = repo.get_trend()
                data = [
                    {
                        "date": record.date.isoformat(),
                        "weight": float(record.weight)
                    }
                    for record in records
                ]
                self.logger.info(f"获取体重趋势数据成功，共 {len(data)} 条记录")
                return data
        except Exception as e:
            self.logger.error(f"获取体重趋势数据失败: {e}")
            raise