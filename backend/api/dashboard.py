from fastapi import APIRouter
from utils.response import set_result
from service.dashboard_service import DashboardService
from utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["数据概览"])
dashboard_service = DashboardService()
logger = get_logger("dashboard_api")


@router.get("/dashboard", summary="获取首页统计数据")
async def get_dashboard():
    """获取首页统计数据"""
    logger.info("开始获取首页统计数据")
    try:
        data = dashboard_service.get_dashboard_data()
        logger.info("获取首页统计数据成功")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取首页统计数据失败: {e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")


@router.get("/dashboard/weight_trend", summary="获取体重趋势数据")
async def get_weight_trend():
    """获取体重趋势数据"""
    logger.info("开始获取体重趋势数据")
    try:
        data = dashboard_service.get_weight_trend()
        logger.info("获取体重趋势数据成功")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取体重趋势数据失败: {e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")