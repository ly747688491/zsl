from sqlalchemy.orm import Session

from module_data.entity.do.job_seeker_do import JobSeekerInfo


class JobSeekerDao:

    @classmethod
    def get_all_job(cls, db: Session):
        """
        获取所有职位信息
        :param db:
        :return:
        """
        return db.query(JobSeekerInfo).all()
