from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class JobSeekerModel(BaseModel):
    """
    岗位信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    enrollee_id: Optional[int] = None
    city: Optional[str] = None
    city_development_index: Optional[float] = None
    gender: Optional[str] = None
    relevent_experience: Optional[str] = None
    enrolled_university: Optional[str] = None
    education_level: Optional[str] = None
    major_discipline: Optional[str] = None
    experience: Optional[str] = None
    company_size: Optional[str] = None
    company_type: Optional[str] = None
    last_new_job: Optional[str] = None
    training_hours: Optional[int] = None
