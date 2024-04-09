import re
import numpy as np

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

from config.database import SQLALCHEMY_DATABASE_URL


def read_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    sql = r"select * from sheet1"  # 查询数据库中的表
    # 读取SQL数据库
    df = pd.read_sql_query(sql=sql, con=engine)  # 读取SQL数据库，并获得pandas数据帧。
    df = df.set_index("id")
    return df


def replace_unknown_city(row):
    """
    将数据中的未知城市替换为正确内容
    """
    if row["province"] == "未知城市":
        return row["location"].split("·")[0]
    else:
        return row["province"]


def replace_error_expercience(work_experience):
    """
    将数据中的《不限》替换为《经验不限》
    """
    return "经验不限" if work_experience == "不限" else work_experience


def process_position_tag(tag):
    """
    处理position_tag，将数据清洗为正确格式
    """
    pattern = r"\['[^']*'\]"
    match = re.search(pattern, tag)
    # 处理空数据
    if pd.isnull(tag):
        return "['None']"
    if ";" not in tag and "," in tag:
        return tag
    if match:
        return tag
    if tag == "[]":
        return tag
    if tag == "":
        return "[]"

    tag_list = re.split(";+", tag)
    tag_list = [f"'{t.strip()}'" for t in tag_list]

    return f"[{', '.join(tag_list)}]"


def clean_error_company(df: DataFrame):
    """
    清除掉company_type错误的数据
    """
    wrong_data = ["20-99人", "100-299人", "20人以下", "500-999人", "10000人以上"]
    df["company_type"] = df["company_type"].str.strip()  # 去除左右两边的空格
    df["company_type"] = df["company_type"].replace("", "未知")
    return df[~df["company_type"].isin(wrong_data)]

def clean_error_size(company_size):
    if company_size in ["20人以下", "10000人以上"]:
        return company_size
    elif "-" in company_size:
        company_size = company_size.replace("人", "")
        company_size = company_size.split("-")
        return f"{int(company_size[0].strip())}-{int(company_size[1].strip())}人"
    else:
        return np.nan


def to_sql(df: DataFrame):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    df.to_sql(name="job_info", con=engine, if_exists="replace", index=True, index_label="id")


def mian(df: DataFrame):
    df = df.reset_index(drop=True)
    df.index = df.index + 1  # 将索引从1开始
    df.index.name = "id"  # 将索引名称设置为'id'
    df.drop('省份', axis=1, inplace=True)  # 删除city列
    df["province"] = df.apply(replace_unknown_city, axis=1)
    df["position_tag"] = df["position_tag"].apply(process_position_tag)
    df["work_experience"] = df["work_experience"].apply(replace_error_expercience)
    df = clean_error_company(df)
    # 删除那些错误的行
    df = df[df['company_size'].str.contains('人', na=False)]
    df["company_size"] = df["company_size"].apply(clean_error_size)
    df.drop_duplicates(inplace=True) # 删除重复数据
    df.fillna(value=np.nan,inplace=True)
    return df


if __name__ == "__main__":
    dataFrame = read_data()
    dataFrame = mian(dataFrame)
    print(dataFrame)
    to_sql(dataFrame)
