import pandas as pd
from faker import Faker

fake = Faker("zh_CN")


def generate_data(num_records):
    records = []
    for _ in range(num_records):
        education = fake.random_element(elements=("高中", "专科", "本科", "硕士"))
        major = fake.random_element(
            elements=(
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
            )
        )
        experience = fake.random_element(elements=("有相关经验", "无相关经验"))
        company_size = fake.random_element(
            elements=("<10", "10-49", "50-99", "100-500")
        )
        passed = (
            education in ("本科", "硕士")
            and major in ("工程学", "计算机科学", "理学")
            and experience == "有相关经验"
        )

        record = {
            "报名者编号": fake.unique.random_int(min=1, max=99999),
            "城市": fake.city(),
            "性别": fake.random_element(elements=("男", "女", None)),
            "相关经验": experience,
            "报名大学": fake.random_element(elements=("全日制", "非全日制", "无")),
            "教育水平": education,
            "主修学科": major,
            "经验年限": fake.random_element(
                elements=[str(i) for i in range(1, 21)] + ["<1", ">20"]
            ),
            "公司规模": company_size,
            "公司类型": fake.random_element(
                elements=(
                    "私营公司",
                    "融资创业公司",
                    "公共部门",
                    "早期创业公司",
                    "非政府组织",
                    "其他",
                )
            ),
            "最近一次新工作": fake.random_element(
                elements=("从未", "1", "2", "3", "4", ">4")
            ),
            "培训时长": fake.random_int(min=1, max=336),
            "是否通过": "是" if passed else "否",
        }
        records.append(record)
    return records


fake_data = generate_data(8000)
fake_data_df = pd.DataFrame(fake_data)

# 修改保存路径以避免覆盖原始数据文件
fake_data_csv_path_modified = "modified_job_seeker_data.csv"
fake_data_df.to_csv(fake_data_csv_path_modified, index=False)

fake_data_csv_path_modified
