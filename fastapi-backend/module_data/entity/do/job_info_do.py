from sqlalchemy import Column, Integer, String

from config.database import Base


class JobInfo(Base):
    __tablename__ = 'job_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(100), nullable=False)
    salary_range = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    work_experience = Column(String(100), nullable=False)
    education_requirement = Column(String(100), nullable=False)
    position_tag = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    company_type = Column(String(100), nullable=False)
    company_size = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
