# Pandas & NumPy 学习指南
基于量化投资项目的实战学习

## 📚 已创建的学习文件

1. **pandas_numpy_tutorial.py** - 基础入门教程
2. **advanced_analysis.py** - 高级实战案例
3. **LEARNING_GUIDE.md** - 本学习指南

---

## 🎯 学习目标

通过本项目，你将掌握：
- NumPy 数组操作和向量化计算
- Pandas 数据处理和分析技巧
- 金融数据分析和量化策略开发
- 职场实用数据分析技能

---

## 📊 项目结构

```
quant-invest-learning/
├── modules/
│   ├── data_fetcher.py      # 数据获取模块
│   ├── indicators.py         # 技术指标模块
│   └── ...
├── pandas_numpy_tutorial.py  # 基础教程
├── advanced_analysis.py        # 高级案例
└── LEARNING_GUIDE.md       # 学习指南
```

---

## 💡 Pandas 高频函数速查

### 数据读取与查看
```python
df.head()      # 查看前5行
df.tail()      # 查看后5行
df.describe()   # 统计描述
df.info()       # 数据信息
df.shape        # 数据形状
```

### 数据选择
```python
df['col']              # 选择单列
df[['col1', 'col2']]  # 选择多列
df.iloc[0:5]           # 按位置选择
df.loc[条件]           # 按条件选择
```

### 数据清洗
```python
df.isnull().sum()       # 统计缺失值
df.dropna()             # 删除缺失值
df.fillna(0)           # 填充缺失值
df.drop_duplicates()     # 删除重复值
```

### 数据转换
```python
df['new_col'] = df['col'].pct_change()  # 计算变化率
df['log_col'] = np.log(df['col'])        # 对数转换
df['date'] = pd.to_datetime(df['date'])   # 日期转换
```

### 分组与聚合
```python
df.groupby('category').mean()    # 分组聚合
df.pivot_table()                 # 数据透视
pd.concat([df1, df2])              # 数据合并
```

### 时间序列
```python
df.set_index('date')             # 设置日期索引
df.rolling(window=20).mean()    # 滚动平均
df.resample('M').mean()           # 重采样
```

---

## 🚀 NumPy 高频函数速查

### 数组创建
```python
np.array([1,2,3])       # 创建数组
np.zeros((3,3))             # 全0数组
np.ones((3,3))              # 全1数组
np.arange(0,10,2))         # 等差数列
```

### 统计计算
```python
np.mean(arr)      # 平均值
np.std(arr)       # 标准差
np.var(arr)       # 方差
np.max(arr)       # 最大值
np.min(arr)       # 最小值
np.sum(arr)       # 求和
```

### 累积计算
```python
np.cumsum(arr)    # 累积和
np.cumprod(arr)   # 累积积
np.maximum.accumulate(arr)  # 累积最大值
```

### 数学函数
```python
np.log(arr)       # 自然对数
np.exp(arr)       # 指数
np.diff(arr)      # 差分
np.where(条件, x, y)  # 条件判断
```

---

## 💼 职场应用场景

### 1. 金融行业
- 量化策略回测
- 风险指标计算（最大回撤、夏普比率）
- 投资组合优化
- 相关性分析

### 2. 电商行业
- 用户行为分析
- 销售数据统计
- A/B测试分析
- 用户留存分析

### 3. 运营分析
- 月度/季度KPI统计
- 数据报表自动化
- 趋势分析与预测
- 异常检测

---

## 📝 学习建议

### 第一阶段：基础入门（1-2周）
1. 运行 `pandas_numpy_tutorial.py`
2. 理解每个例子并尝试修改参数
3. 练习 Pandas 和 NumPy 基础函数

### 第二阶段：深入实践（2-4周）
1. 运行 `advanced_analysis.py`
2. 理解项目中的技术指标模块
3. 尝试添加新的策略或指标

### 第三阶段：项目实战（持续）
1. 修改项目代码
2. 添加新的数据源
3. 开发自己的策略

---

## 🔗 学习资源

- Pandas 官方文档：https://pandas.pydata.org/
- NumPy 官方文档：https://numpy.org/
- 量化投资入门书籍

---

## 📌 关键要点

1. **向量化操作**比循环快很多，优先使用
2. **Pandas**处理表格数据，**NumPy**处理数值计算
3. 善用**rolling()**做时间序列分析
4. 用**groupby()**做分组聚合
5. 实际项目中多实践是最快的学习方式！

---

祝你学习愉快！🎉
