from fastapi import APIRouter, Path, Body
from pydantic import BaseModel
from utils.response import set_result
from service.weight_service import WeightService
from utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["体重记录"])
weight_service = WeightService()
logger = get_logger("weight_api")


class WeightRecordCreate(BaseModel):
    """体重记录创建模型"""
    date: str
    weight: float
    note: str = None


@router.get("/weight_record", summary="获取体重记录列表")
async def get_weight_record():
    """获取体重记录列表"""
    logger.info("开始获取体重记录列表")
    try:
        data = weight_service.get_weight_records()
        logger.info(f"获取体重记录列表成功，共 {len(data)} 条记录")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取体重记录列表失败: {e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")


@router.post("/weight_record", summary="新增体重记录")
async def add_weight_record(record: WeightRecordCreate = Body(...)):
    """新增体重记录"""
    logger.info(f"开始新增体重记录: 日期={record.date}, 体重={record.weight}, 备注={record.note}")
    try:
        success = weight_service.add_weight_record(record.date, record.weight, record.note)
        if success:
            logger.info("新增体重记录成功")
            return set_result(message="体重记录新增成功")
        else:
            logger.warning("新增体重记录失败")
            return set_result(code=1, message="新增体重记录失败")
    except Exception as e:
        logger.error(f"新增体重记录失败: {e}")
        return set_result(code=1, message=f"新增数据失败: {str(e)}")


@router.delete("/weight_record/{id}", summary="删除体重记录")
async def delete_weight_record(id: int = Path(..., description="体重记录ID")):
    """删除体重记录"""
    logger.info(f"开始删除体重记录: ID={id}")
    try:
        success = weight_service.delete_weight_record(id)
        if success:
            logger.info(f"删除体重记录成功: ID={id}")
            return set_result(message="删除成功")
        else:
            logger.warning(f"体重记录不存在: ID={id}")
            return set_result(code=1, message="体重记录不存在")
    except Exception as e:
        logger.error(f"删除体重记录失败: ID={id}, 错误={e}")
        return set_result(code=1, message=f"删除数据失败: {str(e)}")