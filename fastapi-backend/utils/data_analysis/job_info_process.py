import pandas as pd
from sqlalchemy import create_engine

from config.database import SQLALCHEMY_DATABASE_URL


def read_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    sql = r'select * from job_info'  # 查询数据库中的表
    # 读取SQL数据库
    df = pd.read_sql_query(sql=sql, con=engine)  # 读取SQL数据库，并获得pandas数据帧。
    df = df.set_index('id')
    return df


def replace_unknown_city(row):
    if row['province'] == '未知城市':
        return row['location'].split('·')[0]
    else:
        return row['province']


if __name__ == '__main__':
    df = read_data()
    df['province'] = df.apply(replace_unknown_city, axis=1)
    # 创建一个包含错误数据的列表
    wrong_data = ['20-99人', '100-299人', '20人以下', '500-999人']
    # 使用isin方法找到错误数据，然后用~操作符取反，得到正确的数据
    df = df[~df['company_type'].isin(wrong_data)]
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    df.to_sql(name='job_info', con=engine, if_exists='replace', index=True, index_label='id')
