from sqlalchemy import Column, Integer, String

from config.database import Base


class JobInfo(Base):
    __tablename__ = 'job_info'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    position_name = Column(String(100), nullable=False, comment='职位名称')
    salary_range = Column(String(100), nullable=False, comment='薪资范围')
    location = Column(String(100), nullable=False, comment='工作地点')
    work_experience = Column(String(100), nullable=False, comment='工作经验')
    education_requirement = Column(String(100), nullable=False, comment='学历要求')
    position_tag = Column(String(100), nullable=False, comment='职位标签')
    company_name = Column(String(100), nullable=False, comment='公司名称')
    company_type = Column(String(100), nullable=False, comment='公司类型')
    company_size = Column(String(100), nullable=False, comment='公司规模')
    province = Column(String(100), nullable=False, comment='省份')
