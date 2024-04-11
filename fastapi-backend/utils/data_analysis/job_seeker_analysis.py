import pandas as pd
from sqlalchemy import create_engine

from config.database import SQLALCHEMY_DATABASE_URL


def read_data():
    file_path = "modified_aug_train.csv"
    df = pd.read_csv(file_path)  # 读取SQL数据库，并获得pandas数据帧。
    df = df.set_index("enrollee_id")
    return df


def analyze_field_values(df: pd.DataFrame, field: str):
    result = df.groupby(field).size().reset_index(name="count")
    return result.sort_values(by="count", ascending=True)


if __name__ == "__main__":
    data = read_data()
    city_values = analyze_field_values(data, "city")
    education_level_values = analyze_field_values(data, "education_level")
    experience_values = analyze_field_values(data, "experience")
    training_hours_values = analyze_field_values(data, "training_hours")
    enrolled_university_values = analyze_field_values(data, "enrolled_university")
    target = analyze_field_values(data, "target")
    print(city_values)
    print(education_level_values)
    print(experience_values)
    print(training_hours_values)
    print(enrolled_university_values)
    print(target)
    filtered_result = training_hours_values[training_hours_values['training_hours'] > 50]
    total_count_greater_than_50 = filtered_result['count'].sum()
    print(total_count_greater_than_50)
