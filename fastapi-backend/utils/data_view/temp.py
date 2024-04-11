import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("zh_CN")


file_path = "aug_train.csv"
df = pd.read_csv(file_path)  # 读取SQL数据库，并获得pandas数据帧。
df = df.set_index("enrollee_id")
# Replace city with fake Chinese provinces
df["city"] = [fake.province() for _ in range(len(df))]

# Replace gender with Chinese male and female, keeping NaN values as is
df["gender"] = (
    df["gender"]
    .map({"Male": "男", "Female": "女", "Other": "其他"})
    .where(pd.notnull(df["gender"]), np.nan)
)

replacements = {
    "relevent_experience": {
        "Has relevent experience": "有相关经验",
        "No relevent experience": "无相关经验",
    },
    "enrolled_university": {
        "no_enrollment": "未入学",
        "Full time course": "全日制课程",
        "Part time course": "非全日制课程",
    },
    "education_level": {
        "Graduate": "本科",
        "Masters": "硕士",
        "Phd": "博士",
        "High School": "高中",
        "Primary School": "小学",
    },
    "major_discipline": {
        "STEM": "理工科",
        "Business Degree": "商学",
        "Arts": "文学",
        "Humanities": "人文学科",
        "No Major": "无专业",
        "Other": "其他",
    },
    "experience": {"<1": "少于1年", ">20": "超过20年"},
    "company_size": {
        "<10": "少于10人",
        "10/49": "10-49人",
        "50-99": "50-99人",
        "100-500": "100-500人",
        "500-999": "500-999人",
        "1000-4999": "1000-4999人",
        "5000-9999": "5000-9999人",
        "10000+": "10000人以上",
    },
    "company_type": {
        "Pvt Ltd": "私营公司",
        "Funded Startup": "融资创业公司",
        "Public Sector": "公共部门",
        "Early Stage Startup": "初创公司",
        "NGO": "非政府组织",
        "Other": "其他",
    },
    "last_new_job": {"never": "从未", "1": "1年内", ">4": "超过4年"},
}

# Apply the replacements to the dataframe
for column, mapping in replacements.items():
    df[column] = df[column].map(mapping).where(pd.notnull(df[column]), df[column])

# # For 'experience' with numeric values, handle separately
# df["experience"] = df["experience"].apply(
#     lambda x: x if x in replacements["experience"] else (x + "年" if x.isdigit() else x)
# )
# df["experience"] = df["experience"].apply(
#     lambda x: x
#     if pd.isnull(x) or x in replacements["experience"]
#     else (x + "年" if isinstance(x, str) and x.isdigit() else x)
# )

# 指定保存修改后文件的路径
output_file_path = "modified_aug_train.csv"

# 保存修改后的文件
df.to_csv(output_file_path)
