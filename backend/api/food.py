from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel
from utils.response import set_result
from service.food_service import FoodService, FoodRecordService
from utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["饮食记录"])
food_service = FoodService()
food_record_service = FoodRecordService()
logger = get_logger("food_api")


class FoodRecordCreate(BaseModel):
    """饮食记录创建模型"""
    date: str
    food_id: int
    weight: float


@router.get("/food", summary="获取食物列表")
async def get_food():
    """获取食物列表"""
    logger.info("开始获取食物列表")
    try:
        data = food_service.get_foods()
        logger.info(f"获取食物列表成功，共 {len(data)} 条记录")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取食物列表失败: {e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")


@router.get("/food_record", summary="获取饮食记录")
async def get_food_record(date: str = Query(..., description="查询日期")):
    """获取饮食记录"""
    logger.info(f"开始获取饮食记录: 日期={date}")
    try:
        data = food_record_service.get_food_records(date)
        logger.info(f"获取饮食记录成功，共 {len(data)} 条记录")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取饮食记录失败: 日期={date}, 错误={e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")


@router.post("/food_record", summary="新增饮食记录")
async def add_food_record(record: FoodRecordCreate = Body(...)):
    """新增饮食记录"""
    logger.info(f"开始新增饮食记录: 日期={record.date}, 食物ID={record.food_id}, 重量={record.weight}")
    try:
        success = food_record_service.add_food_record(record.date, record.food_id, record.weight)
        if success:
            logger.info("新增饮食记录成功")
            return set_result(message="饮食记录添加成功")
        else:
            logger.warning(f"食物不存在: ID={record.food_id}")
            return set_result(code=1, message="食物不存在")
    except Exception as e:
        logger.error(f"新增饮食记录失败: {e}")
        return set_result(code=1, message=f"新增数据失败: {str(e)}")


@router.delete("/food_record/{id}", summary="删除饮食记录")
async def delete_food_record(id: int = Path(..., description="饮食记录ID")):
    """删除饮食记录"""
    logger.info(f"开始删除饮食记录: ID={id}")
    try:
        success = food_record_service.delete_food_record(id)
        if success:
            logger.info(f"删除饮食记录成功: ID={id}")
            return set_result(message="删除成功")
        else:
            logger.warning(f"饮食记录不存在: ID={id}")
            return set_result(code=1, message="饮食记录不存在")
    except Exception as e:
        logger.error(f"删除饮食记录失败: ID={id}, 错误={e}")
        return set_result(code=1, message=f"删除数据失败: {str(e)}")