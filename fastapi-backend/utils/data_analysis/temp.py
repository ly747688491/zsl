import pandas as pd
from faker import Faker
import numpy as np

fake = Faker("zh_CN")


def generate_normal_dist_category(categories, mean, std):
    # 生成一个符合正态分布的随机数
    normal_val = np.random.normal(loc=mean, scale=std)
    # 将这个数映射到分类索引上，同时确保索引值在有效范围内
    index = max(0, min(len(categories) - 1, int(normal_val)))
    return categories[index]


def generate_data(num_records):
    records = []
    for _ in range(num_records):
        education = generate_normal_dist_category(["高中", "专科", "本科", "硕士"], 2, 1)
        major = generate_normal_dist_category(
            [
                "工程学",
                "经济学",
                "管理学",
                "文学",
                "理学",
                "教育学",
                "医学",
                "艺术学",
                "历史学",
                "哲学",
                "无主修",
                "其他",
            ],
            5, 3)

        experience_levels = ["有相关经验", "无相关经验"]
        experience = generate_normal_dist_category(experience_levels, 0.5, 0.5)

        company_sizes = ["<10", "10-49", "50-99", "100-500"]
        company_size = generate_normal_dist_category(company_sizes, 2, 1)

        enrolled_universities = ["全日制", "非全日制", "无"]
        enrolled_university = generate_normal_dist_category(enrolled_universities, 1, 1)

        experience_years = [str(i) for i in range(1, 21)] + ["<1", ">20"]
        years_of_experience = generate_normal_dist_category(experience_years, 10, 5)

        last_new_job_options = ["从未", "1", "2", "3", "4", ">4"]
        last_new_job = generate_normal_dist_category(last_new_job_options, 2, 1)

        city = fake.province()

        record = {
            "id": fake.unique.random_int(min=1, max=99999),
            "city": city,
            "gender": fake.random_element(elements=("男", "女", None)),
            "relevent_experience": experience,
            "enrolled_university": enrolled_university,
            "education_level": education,
            "major_discipline": major,
            "experience": years_of_experience,
            "company_size": company_size,
            "company_type": fake.random_element(
                elements=(
                    "私营公司",
                    "融资创业公司",
                    "公共部门",
                    "早期创业公司",
                    "非政府组织",
                    "其他",
                )
            ),
            "last_new_job": last_new_job,
            "training_hours": int(np.random.normal(loc=100, scale=50, size=1).clip(min=1)),
            "is_through": "是" if (education in ["本科", "硕士"] and major in ["工程学",
                                                                               "理学"]) and experience == "有相关经验" else "否",
        }
        records.append(record)
    return records


# 生成并保存数据
fake_data = generate_data(8000)
fake_data_df = pd.DataFrame(fake_data)

fake_data_csv_path_modified = "modified_job_seeker_data.csv"
fake_data_df.to_csv(fake_data_csv_path_modified, index=False)
