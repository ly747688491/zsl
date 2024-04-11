from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 处理缺失值：使用最频繁出现的值填充分类特征，数值特征用中位数填充
categorical_columns = data.select_dtypes(include=['object']).columns
numerical_columns = data.select_dtypes(exclude=['object']).columns.drop(['id'])  # 排除ID

categorical_imputer = SimpleImputer(strategy='most_frequent')
numerical_imputer = SimpleImputer(strategy='median')

data[categorical_columns] = categorical_imputer.fit_transform(data[categorical_columns])
data[numerical_columns] = numerical_imputer.fit_transform(data[numerical_columns])

# 处理`experience`和`last_new_job`中的特殊字符
data['experience'] = data['experience'].apply(lambda x: 0 if x == '<1' else (20 if x == '>20' else int(x)))
data['last_new_job'] = data['last_new_job'].apply(lambda x: 0 if x == '从未' else (5 if x == '>4' else int(x)))

# 将`is_through`目标变量转换为数值型
label_encoder = LabelEncoder()
data['is_through'] = label_encoder.fit_transform(data['is_through'])

# 选择特征列和目标变量
X = data.drop(['id', 'is_through'], axis=1)
y = data['is_through']

# 将分类数据转换为数值型
categorical_features = X.select_dtypes(include=['object']).columns
numerical_features = X.select_dtypes(exclude=['object']).columns

# 创建预处理管道
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
    ]
)

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林模型管道
rf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', RandomForestClassifier(random_state=42))])

# 训练模型
rf_pipeline.fit(X_train, y_train)

# 预测和评估
y_pred = rf_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

accuracy, report
