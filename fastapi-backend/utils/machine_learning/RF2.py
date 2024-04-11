import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 解决画图中文显示问题
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 14

# 加载数据
data_ = pd.read_csv("modified_aug_train.csv")
# 删除含有 NaN 的行
data = data_.dropna().copy()

# 对非数值型数据进行编码
label_encoders = {}
for column in data.columns[:-1]:  # 遍历特征列
    if data[column].dtype == "object":  # 如果是非数值型数据
        le = LabelEncoder()
        data.loc[:, column] = le.fit_transform(data.loc[:, column])
        label_encoders[column] = le  # 将 LabelEncoder 存储在字典中，以备后续使用

# 将特征和目标变量分离
X = data.drop("target", axis=1)
y = data["target"]


# 创建随机森林回归模型
rf_model = RandomForestClassifier()
# y = data["target"].map({"是": 1, "否": 0})

# 将数据分割成训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 训练模型
rf_model.fit(X_train, y_train)

# 获取特征重要性
feature_importance = rf_model.feature_importances_
# 创建一个DataFrame来存储特征和其对应的重要性值
feature_importance_df = pd.DataFrame(
    {"Feature": X.columns, "Importance": feature_importance}
)

# 按重要性值降序排序
feature_importance_df = feature_importance_df.sort_values(
    by="Importance", ascending=False
)

# 打印每个特征的重要性值
print("特征重要性值按降序排列:")
print(feature_importance_df)

# 设置特征重要性阈值
threshold = 0.05  # 设置阈值为你需要的值

# 根据阈值筛选特征
selected_features = X.columns[feature_importance >= threshold]

# 创建新的DataFrame，包括保留的特征和目标列
new_data = data[selected_features.append(pd.Index(["target"]))]

# 保存新的DataFrame到Excel文件
new_data.to_excel("selected_data_rf.xlsx", index=False)

# 对特征重要性进行降序排序并获取索引/升序-1
sorted_idx = np.argsort(feature_importance)[::1]

# 根据排序后的索引重新排列特征和重要性数组
sorted_features = X.columns[sorted_idx]
sorted_importance = feature_importance[sorted_idx]

# 创建图表和子图
fig, ax = plt.subplots(figsize=(8, 6))

# 使用Matplotlib绘制横向柱状图，设置柱状图颜色为黑色
ax.barh(sorted_features, sorted_importance, color="black")

# 设置字体为Times New Roman
ax.set_xlabel("Importance Score")
ax.set_ylabel("Features")
ax.set_title("Feature Importance using Random Forest")

# 旋转y轴标签
plt.yticks(rotation=45)

# 保存图像
plt.savefig("feature_importance_plot.png", dpi=600)

# 显示图像
plt.show()

# 在测试集上进行预测
y_pred = rf_model.predict(X_test)

# 计算R方（R²）
r2 = r2_score(y_test, y_pred)

# 计算均方误差（MSE）
mse = mean_squared_error(y_test, y_pred)

# 计算平均绝对误差（MAE）
mae = mean_absolute_error(y_test, y_pred)

# 输出R方、MSE和MAE
print("R方（R²）:", r2)
print("均方误差（MSE）:", mse)
print("平均绝对误差（MAE）:", mae)
y_test = np.array(y_test)
import matplotlib.pyplot as plt

# 创建高分辨率图形
plt.figure(figsize=(8, 6))
# 绘制真实值的点线图，使用蓝色
plt.plot(
    y_test, marker="o", linestyle="-", markersize=5, label="真实值", color="#1f77b4"
)
# 绘制预测值的点线图，使用橙色
plt.plot(
    y_pred, marker="o", linestyle="--", markersize=5, label="预测值", color="#ff7f0e"
)
# 添加标签和标题
plt.title(f"R²: {r2:.4f}     MSE: {mse:.4f}     MAE: {mae:.4f}", fontsize=16)
plt.xlabel("样本编号", fontsize=12)
plt.ylabel("值", fontsize=12)
# 添加网格线
plt.grid(True)
# 调整刻度字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 添加图例
plt.legend(fontsize=10)
# 保存图形为高分辨率图像文件
plt.tight_layout()
plt.savefig("Comparison_plot.png", dpi=300)
# 显示图形
plt.show()


# 创建高分辨率图形
plt.figure(figsize=(8, 6))
# 绘制散点图
plt.scatter(
    y_test, y_pred, color="#8c564b", marker="o", label="预测值", alpha=0.3, s=50
)
# 绘制比较线
plt.plot(y_test, y_test, color="#d62728", linestyle="--", label="y=x", linewidth=1.5)
# 添加标签和标题
plt.xlabel("真实值", fontsize=12)
plt.ylabel("预测值", fontsize=12)
plt.title("真实值 vs 预测值", fontsize=14)
# 添加图例
plt.legend(fontsize=10)
# 去除网格线
plt.grid(True)
# 调整刻度字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 保存图形为高分辨率图像文件
plt.tight_layout()
plt.savefig("scatter_plot.png", dpi=300)
# 显示图形
plt.show()

# 残差图（Residual Plot）
residuals = y_test - y_pred
residual_mean = residuals.mean()  # 计算残差的平均值
plt.figure(figsize=(8, 6))
plt.hist(
    residuals, bins=30, color="blue", alpha=0.7, edgecolor="black", label="残差分布"
)
plt.axvline(
    x=residual_mean,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"平均值 = {residual_mean:.2f}",
)  # 添加标签
plt.title("残差分布直方图")
plt.xlabel("残差")
plt.ylabel("频率")
plt.grid(True)
plt.legend()  # 显示图例
plt.savefig("Residual_plot.png", dpi=300)
plt.show()
