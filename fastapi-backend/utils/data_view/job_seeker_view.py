from pandas import DataFrame
from pyecharts import options as opts
from pyecharts.charts import Bar, Map, Radar

from utils.data_analysis.job_seeker_analysis import read_data, analyze_field_values


def data_preprocessing(df: DataFrame, field: str):
    provinces = df[field].tolist()
    counts = df["count"].tolist()
    return provinces, counts


def building_map(provinces: list, counts: list):
    map_ = Map()
    map_.add("省份数据", [list(z) for z in zip(provinces, counts)], "china")
    map_.set_global_opts(title_opts=opts.TitleOpts(title="省份数据地图"))
    map_.render("province_data_map.html")


def building_bar(experience_years: list, counts: list):
    bar = (
        Bar()
        .add_xaxis(experience_years)
        .add_yaxis("求职者数量", counts)
        .set_global_opts(title_opts=opts.TitleOpts(title="求职者的经验年限"))
    )
    bar.render("experience_years_distribution.html")


def building_radar(education_level: list, count: list):
    radar = (
        Radar()
        .add_schema(education_level)
        .add("求职者", count)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="教育背景和工作经历"))
    )

    radar.render("applicant_background_experience.html")


def building_education_level(education_level: list, count: list):
    bar = (
        Bar()
        .add_xaxis(education_level)
        .add_yaxis("求职者数量", count)
        .reversal_axis()  # 将条形图变为横向
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="求职者的教育水平"))
    )

    bar.render("education_level_distribution.html")


def main():
    data = read_data()
    province_info = analyze_field_values(data, "city")
    provinces, counts = data_preprocessing(province_info, "city")
    education_info = analyze_field_values(data, "education_level")
    education_level, education_count = data_preprocessing(education_info, "education_level")
    experience_info = analyze_field_values(data, "experience")
    experience, experience_counts = data_preprocessing(experience_info, "experience")
    training_info = analyze_field_values(data, "training_hours")
    training_info, training_info_counts = data_preprocessing(training_info, "training_hours")
    enrolled_info = analyze_field_values(data, "enrolled_university")
    enrolled_university, enrolled_university_counts = data_preprocessing(enrolled_info, "enrolled_university")
    building_map(provinces, counts)
    building_bar(experience, experience_counts)
    building_radar(enrolled_university, enrolled_university_counts)
    building_education_level(education_level, education_count)


if __name__ == '__main__':
    main()
