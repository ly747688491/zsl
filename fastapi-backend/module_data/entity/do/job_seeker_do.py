from sqlalchemy import Integer, Column, String, Float

from config.database import Base


class JobSeekerInfo(Base):
    """
    Employee Info Model
    """
    __tablename__ = "job_seekers"

    enrollee_id = Column(Integer, primary_key=True, comment="求职者ID")
    city = Column(String(100), nullable=True, comment="所在城市")
    city_development_index = Column(Float, nullable=True, comment="城市发展指数")
    gender = Column(String(20), nullable=True, comment="性别")
    relevent_experience = Column(String(100), nullable=True, comment="相关经验")
    enrolled_university = Column(String(100), nullable=True, comment="所在大学")
    education_level = Column(String(100), nullable=True, comment="教育水平")
    major_discipline = Column(String(100), nullable=True, comment="主修学科")
    experience = Column(String(100), nullable=True, comment="经验")
    company_size = Column(String(100), nullable=True, comment="公司规模")
    company_type = Column(String(100), nullable=True, comment="公司类型")
    last_new_job = Column(String(100), nullable=True, comment="最新工作")
    training_hours = Column(Integer, nullable=True, comment="培训小时数")
