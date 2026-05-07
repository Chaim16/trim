from datetime import date
from repository.exercise_repository import ExerciseRepository
from repository.models import ExerciseRecord
from utils.database import get_db_session
from utils.logger import get_logger


class ExerciseService:
    """运动记录服务"""
    
    def __init__(self):
        self.logger = get_logger("exercise_service")
    
    def get_exercise_records(self, date_str: str):
        """获取运动记录"""
        self.logger.info(f"开始获取运动记录: 日期={date_str}")
        try:
            with get_db_session() as db:
                repo = ExerciseRepository(db)
                record_date = date.fromisoformat(date_str)
                records = repo.get_by_date(record_date)
                
                data = [
                    {
                        "id": record.id,
                        "exercise_name": record.exercise_name,
                        "duration": float(record.duration),
                        "calorie": float(record.calorie)
                    }
                    for record in records
                ]
                self.logger.info(f"获取运动记录成功，共 {len(data)} 条记录")
                return data
        except Exception as e:
            self.logger.error(f"获取运动记录失败: 日期={date_str}, 错误={e}")
            raise
    
    def add_exercise_record(self, date_str: str, exercise_name: str, duration: float, calorie: float):
        """新增运动记录"""
        self.logger.info(f"开始新增运动记录: 日期={date_str}, 运动名称={exercise_name}, 时长={duration}分钟, 消耗热量={calorie}kcal")
        try:
            with get_db_session() as db:
                repo = ExerciseRepository(db)
                record_date = date.fromisoformat(date_str)
                new_record = ExerciseRecord(
                    date=record_date,
                    exercise_name=exercise_name,
                    duration=duration,
                    calorie=calorie
                )
                repo.create(new_record)
                self.logger.info("新增运动记录成功")
                return True
        except Exception as e:
            self.logger.error(f"新增运动记录失败: {e}")
            raise
    
    def delete_exercise_record(self, id: int):
        """删除运动记录"""
        self.logger.info(f"开始删除运动记录: ID={id}")
        try:
            with get_db_session() as db:
                repo = ExerciseRepository(db)
                success = repo.delete(id)
                if success:
                    self.logger.info(f"删除运动记录成功: ID={id}")
                else:
                    self.logger.warning(f"运动记录不存在: ID={id}")
                return success
        except Exception as e:
            self.logger.error(f"删除运动记录失败: ID={id}, 错误={e}")
            raise