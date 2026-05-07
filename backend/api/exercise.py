from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel
from utils.response import set_result
from service.exercise_service import ExerciseService
from utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["运动记录"])
exercise_service = ExerciseService()
logger = get_logger("exercise_api")


class ExerciseRecordCreate(BaseModel):
    """运动记录创建模型"""
    date: str
    exercise_name: str
    duration: float
    calorie: float


@router.get("/exercise_record", summary="获取运动记录")
async def get_exercise_record(date: str = Query(..., description="查询日期")):
    """获取运动记录"""
    logger.info(f"开始获取运动记录: 日期={date}")
    try:
        data = exercise_service.get_exercise_records(date)
        logger.info(f"获取运动记录成功，共 {len(data)} 条记录")
        return set_result(data=data, message="操作成功")
    except Exception as e:
        logger.error(f"获取运动记录失败: 日期={date}, 错误={e}")
        return set_result(code=1, message=f"获取数据失败: {str(e)}")


@router.post("/exercise_record", summary="新增运动记录")
async def add_exercise_record(record: ExerciseRecordCreate = Body(...)):
    """新增运动记录"""
    logger.info(f"开始新增运动记录: 日期={record.date}, 运动名称={record.exercise_name}, 时长={record.duration}分钟, 消耗热量={record.calorie}kcal")
    try:
        success = exercise_service.add_exercise_record(record.date, record.exercise_name, record.duration, record.calorie)
        if success:
            logger.info("新增运动记录成功")
            return set_result(message="运动记录新增成功")
        else:
            logger.warning("新增运动记录失败")
            return set_result(code=1, message="新增运动记录失败")
    except Exception as e:
        logger.error(f"新增运动记录失败: {e}")
        return set_result(code=1, message=f"新增数据失败: {str(e)}")


@router.delete("/exercise_record/{id}", summary="删除运动记录")
async def delete_exercise_record(id: int = Path(..., description="运动记录ID")):
    """删除运动记录"""
    logger.info(f"开始删除运动记录: ID={id}")
    try:
        success = exercise_service.delete_exercise_record(id)
        if success:
            logger.info(f"删除运动记录成功: ID={id}")
            return set_result(message="删除成功")
        else:
            logger.warning(f"运动记录不存在: ID={id}")
            return set_result(code=1, message="运动记录不存在")
    except Exception as e:
        logger.error(f"删除运动记录失败: ID={id}, 错误={e}")
        return set_result(code=1, message=f"删除数据失败: {str(e)}")