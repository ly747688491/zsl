from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from module_data.annotation.pydantic_annotation import as_query, as_form


class JobInfoModel(BaseModel):
    """
    岗位信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = None
    position_name: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    work_experience: Optional[str] = None
    education_requirement: Optional[str] = None
    position_tag: Optional[str] = None
    company_name: Optional[str] = None
    company_type: Optional[str] = None
    company_size: Optional[str] = None
    province: Optional[str] = None


@as_query
@as_form
class JobInfoPageQueryModel(JobInfoModel):
    """
    字典类型管理分页查询模型
    """
    page_num: int = 1
    page_size: int = 10