import os
import uuid
from datetime import datetime
from typing import Optional, List
from typing import TypeVar, Dict, AnyStr
from urllib.parse import urlparse

from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)


def get_form_dict(form: Optional[SchemaType] = None, start: Optional[datetime] = None, end: Optional[datetime] = None,
                  time_range: Optional[str] = None, **kwargs) -> Dict:
    form_dict = form.dict(exclude_none=True) if form else {}
    if (start is not None) and (end is not None) and (time_range is not None):
        form_dict[time_range] = (start, end)
    form_dict.update(kwargs)
    return form_dict


def create_dir(file_name: str) -> str:
    """ 创建文件夹 """

    base_path = get_current_directory()

    path = base_path + os.sep + file_name + os.sep  # 拼接日志文件夹的路径

    os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建

    return path


def get_current_directory() -> AnyStr:
    """
    获取当前目录，F:/Github File/FastAPIProject
    :return:
    """
    current_path = os.path.dirname(__file__)  # 获取当前文件夹
    # 获取当前文件夹的上一层文件 F:/Github File/FastAPIProject
    return os.path.abspath(os.path.join(current_path, ".."))


def get_uuid() -> str:
    """生成uuid"""
    return str(uuid.uuid4())


def string_to_bool(string: str) -> bool:
    """字符串转bool变量"""
    return string.lower() != "False"


def get_array_by_str(ids_str: str):
    ids_list = ids_str.split(",")
    return [int(x) for x in ids_list]


def is_http(string: str) -> Optional[str]:
    """是否是http"""
    return string if is_url(string, allowed_schemes=["http", "https"]) else None


def is_url(string: str, allowed_schemes: Optional[List[str]] = None) -> bool:
    """判断是否是URL"""
    try:
        result = urlparse(string)
        if allowed_schemes:
            return all([result.scheme, result.netloc, result.scheme in allowed_schemes])
        else:
            return all([result.scheme, result.netloc])
    except ValueError:
        return False
