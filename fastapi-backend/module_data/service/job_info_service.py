from sqlalchemy.orm import Session
from fastapi import Request

from module_data.dao.job_info_dao import JobInfoDao
from module_data.entity.vo.job_info_vo import JobInfoPageQueryModel


class JobInfoService:

    @classmethod
    def query_job_info_list_services(cls, query_db: Session, query_object: JobInfoPageQueryModel,
                                     is_page: bool = False):
        return JobInfoDao.get_all_job(query_db, query_object, is_page)
