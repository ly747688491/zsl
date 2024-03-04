import time

from sqlalchemy.orm import Session

from config.database import engine, Base
from module_data.entity.do.job_info_do import JobInfo


class ScrapySpiderPipeline:

    def open_spider(self, spider):
        self.engine = engine
        Base.metadata.create_all(self.engine)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('爬取结束')

    def process_item(self, item, spider):
        session = Session(self.engine)
        job_info = JobInfo(
            position_name=item['job_name'],
            salary_range=item['job_salary'],
            location=item['job_city'],
            work_experience=item['job_experience'],
            education_requirement=item['job_education'],
            position_tag=item['job_tags'],
            company_name=item['company_name'],
            company_type=item['company_type'],
            company_size=item['company_size'],
            province=item['province'],
        )
        session.add(job_info)
        session.commit()
        session.close()
        return item

    def close_spider(self, spider):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('爬取结束')
