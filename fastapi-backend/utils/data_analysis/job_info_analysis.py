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


def get_type_and_num(df: DataFrame):
    return {
        'total_records': df.shape[0],  # 获取记录总数
        'total_companies': df['company_name'].nunique(),  # 获取公司总数
        'total_provinces': df['province'].nunique(),  # 获取省份总数
        'total_company_types': df['company_type'].nunique(),  # 获取公司类型总数
    }


if __name__ == '__main__':
    data = read_data()
    df_type_num = get_type_and_num(data)
    print(df_type_num)
