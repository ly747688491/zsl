import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

from config.database import SQLALCHEMY_DATABASE_URL


def read_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    sql = r'select * from sheet1'  # 查询数据库中的表
    # 读取SQL数据库
    df = pd.read_sql_query(sql=sql, con=engine)  # 读取SQL数据库，并获得pandas数据帧。
    df = df.set_index('id')
    return df


def replace_unknown_city(row):
    if row['province'] == '未知城市':
        return row['location'].split('·')[0]
    else:
        return row['province']


def clean_error_company(df: DataFrame):
    # 创建一个包含错误数据的列表
    wrong_data = ['20-99人', '100-299人', '20人以下', '500-999人']
    return df[~df['company_type'].isin(wrong_data)]


if __name__ == '__main__':
    df = read_data()
    df = df.drop('id')

    # df['province'] = df.apply(replace_unknown_city, axis=1)
    # df = clean_error_company(df)
    # df.drop_duplicates(inplace=True)

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    df.to_sql(name='job_info', con=engine, if_exists='replace', index=True, index_label='id')
