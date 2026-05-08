from repository.dashboard_repository import DashboardRepository
from utils.database import get_db_session
from utils.logger import get_logger
from utils.other import read_yaml_config


class DashboardService:
    """首页数据服务"""
    
    def __init__(self):
        self.logger = get_logger("dashboard_service")
    
    def get_dashboard_data(self):
        """获取首页统计数据"""
        self.logger.info("开始获取首页统计数据")
        try:
            with get_db_session() as db:
                repo = DashboardRepository(db)
                current_weight = repo.get_current_weight()
                today_exercise_calorie = repo.get_today_exercise_calorie()
                
                # 从配置文件中读取目标体重
                config = read_yaml_config()
                target_weight = config.get("user", {}).get("target_weight", 65)
                
                data = {
                    "current_weight": float(current_weight),
                    "target_weight": target_weight,
                    "today_exercise_calorie": today_exercise_calorie,
                }
                self.logger.info(f"获取首页统计数据成功: {data}")
                return data
        except Exception as e:
            self.logger.error(f"获取首页统计数据失败: {e}")
            raise
    
    def get_weight_trend(self):
        """获取体重趋势数据"""
        self.logger.info("开始获取体重趋势数据")
        try:
            with get_db_session() as db:
                repo = DashboardRepository(db)
                records = repo.get_weight_trend()
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