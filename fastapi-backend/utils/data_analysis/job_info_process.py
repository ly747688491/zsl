from sqlalchemy import create_engine, MetaData, Table, select

from config.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # 更改为你的数据库连接
metadata = MetaData()
connection = engine.connect()

# 加载表结构
job_table = Table('job_info', metadata, autoload_with=engine)  # 更改为你的表名

# 查询所有数据
query = select(job_table.c.id, job_table.c.company_type, job_table.c.province, job_table.c.city)
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()

# 遍历所有数据
for result in ResultSet:
    # 如果company_type字段是类似20-99人这样的错误数据直接删除数据
    if '-' in result.company_type:
        delete_st = job_table.delete().where(job_table.c.id == result.id)
        connection.execute(delete_st)
        continue
    # 如果province字段是'未知城市'，则在city字段例如'大连·甘井子·凌水'中选取大连填充到province
    if result.province == '未知城市':
        city = result.city.split('·')[0]
        update_st = job_table.update().where(job_table.c.id == result.id).values(province=city)
        connection.execute(update_st)

# 关闭连接
connection.close()
