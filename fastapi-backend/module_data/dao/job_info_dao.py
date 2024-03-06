from sqlalchemy.orm import Session

from module_data.entity.do.job_info_do import JobInfo
from module_data.entity.vo.job_info_vo import JobInfoPageQueryModel
from utils.system_utils.page_utils import PageUtil


class JobInfoDao:

    @classmethod
    def get_all_job(cls, db: Session, query_object: JobInfoPageQueryModel, is_page: bool = False):
        """
        获取所有职位信息
        :param is_page: 是否分页
        :param query_object: 查询参数对象
        :param db: orm对象
        :return: 岗位信息列表对象
        """
        query = db.query(JobInfo)
        return PageUtil.paginate(query, query_object.page_num, query_object.page_size, is_page)
