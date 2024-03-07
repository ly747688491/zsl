import ast

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

from config.database import SQLALCHEMY_DATABASE_URL


def read_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    sql = r"select * from job_info"  # 查询数据库中的表
    # 读取SQL数据库
    df = pd.read_sql_query(sql=sql, con=engine)  # 读取SQL数据库，并获得pandas数据帧。
    df = df.set_index("id")
    return df


def get_type_and_num(df: DataFrame):
    return {
        "total_records": df.shape[0],  # 获取记录总数
        "total_companies": df["company_name"].nunique(),  # 获取公司总数
        "total_provinces": df["province"].nunique(),  # 获取省份总数
        "total_company_types": df["company_type"].nunique(),  # 获取公司类型总数
    }


def get_tag_num(df: DataFrame):
    tag_array = df["position_tag"].apply(ast.literal_eval).tolist()
    tag_lis = []
    for tag in tag_array:
        tag_lis += tag
    tag_df = pd.DataFrame(tag_lis, columns=["职位标签"])
    tag_df_cnt = tag_df["职位标签"].value_counts().reset_index()
    tag_df_cnt.columns = ["职位标签", "计数"]
    return list(zip(tag_df_cnt["职位标签"], tag_df_cnt["计数"]))


def get_city_job_num(df: DataFrame):
    job_counts = df.groupby("province").size()
    sorted_job_counts = job_counts.sort_values()

    return sorted_job_counts.to_dict()


def get_experience_num(df: DataFrame):
    result = df.groupby("work_experience").size().reset_index(name="count")
    return result.sort_values(by="count", ascending=True)


def get_education_num(df: DataFrame):
    result = df.groupby("education_requirement").size().reset_index(name="count")
    return result.sort_values(by="count", ascending=True)


def analyze_field_values(df: DataFrame, field: str):
    result = df.groupby(field).size().reset_index(name="count")
    return result.sort_values(by="count", ascending=True)


if __name__ == "__main__":
    data = read_data()
    province_values = analyze_field_values(data, "province")
    work_experience_values = analyze_field_values(data, "work_experience")
    education_requirement_values = analyze_field_values(data, "education_requirement")
    company_type_values = analyze_field_values(data, "company_type")
    print(province_values)
    print(work_experience_values)
    print(education_requirement_values)
    print(company_type_values)
