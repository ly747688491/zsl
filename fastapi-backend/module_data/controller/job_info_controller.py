from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from fastapi import Request

from config.get_db import get_db
from module_data.entity.vo.job_info_vo import JobInfoPageQueryModel
from module_data.service.job_info_service import JobInfoService
from utils.system_utils import ResponseUtil
from utils.system_utils.page_utils import PageResponseModel

jobInfoController = APIRouter(prefix='/job')


@jobInfoController.get("/all", response_model=PageResponseModel)
async def get_type_num(request: Request,
                       job_info_page_query: JobInfoPageQueryModel = Depends(JobInfoPageQueryModel.as_query),
                       query_db: Session = Depends(get_db)):
    try:
        job_info_page_query_result = JobInfoService.query_job_info_list_services(query_db, job_info_page_query,
                                                                                 is_page=True)
        logger.info("查询成功")
        return ResponseUtil.success(model_content=job_info_page_query_result)
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=str(e))
