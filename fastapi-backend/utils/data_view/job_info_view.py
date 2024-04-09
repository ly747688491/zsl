from pandas import DataFrame
from pyecharts import options as opts
from pyecharts.charts import Bar, Map

from utils.data_analysis.job_info_analysis import analyze_field_values, read_data


def data_preprocessing(df: DataFrame, field: str):
    provinces = df[field].tolist()
    counts = df["count"].tolist()
    return provinces, counts


def building_map(provinces: list, counts: list):
    map_ = Map()
    map_.add("省份数据", [list(z) for z in zip(provinces, counts)], "china")
    map_.set_global_opts(title_opts=opts.TitleOpts(title="省份数据地图"))
    map_.render("province_data_map.html")


def build_bar(provinces: list, counts: list):
    bar_ = Bar()
    bar_.add_xaxis(provinces)
    bar_.add_yaxis("省份数据", counts)
    bar_.set_global_opts(
        title_opts=opts.TitleOpts(title="省份数据柱状图"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
    )
    bar_.render("province_data_bar.html")


def main():
    data = read_data()
    province_info = analyze_field_values(data, "province")
    provinces, counts = data_preprocessing(province_info, "province")
    print(provinces)
    print(counts)
    building_map(provinces, counts)
    build_bar(provinces, counts)


if __name__ == "__main__":
    main()
