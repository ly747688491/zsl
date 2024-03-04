from datetime import datetime

from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Index


class SysOperLog(Base):
    """
    操作日志记录
    """
    __tablename__ = 'sys_oper_log'

    oper_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='日志主键')
    title = Column(String(50, collation='utf8_general_ci'), nullable=True, default='', comment='模块标题')
    business_type = Column(Integer, default=0, comment='业务类型（0其它 1新增 2修改 3删除）')
    method = Column(String(100, collation='utf8_general_ci'), nullable=True, default='', comment='方法名称')
    request_method = Column(String(10, collation='utf8_general_ci'), nullable=True, default='', comment='请求方式')
    oper_url = Column(String(255, collation='utf8_general_ci'), nullable=True, default='', comment='请求URL')
    oper_ip = Column(String(128, collation='utf8_general_ci'), nullable=True, default='', comment='主机地址')
    oper_location = Column(String(255, collation='utf8_general_ci'), nullable=True, default='', comment='操作地点')
    oper_param = Column(String(2000, collation='utf8_general_ci'), nullable=True, default='', comment='请求参数')
    json_result = Column(String(2000, collation='utf8_general_ci'), nullable=True, default='', comment='返回参数')
    status = Column(Integer, default=0, comment='操作状态（0正常 1异常）')
    error_msg = Column(String(2000, collation='utf8_general_ci'), nullable=True, default='', comment='错误消息')
    oper_time = Column(DateTime, nullable=True, default=datetime.now(), comment='操作时间')
    cost_time = Column(BigInteger, default=0, comment='消耗时间')

    idx_sys_oper_log_bt = Index('idx_sys_oper_log_bt', business_type)
    idx_sys_oper_log_s = Index('idx_sys_oper_log_s', status)
    idx_sys_oper_log_ot = Index('idx_sys_oper_log_ot', oper_time)
