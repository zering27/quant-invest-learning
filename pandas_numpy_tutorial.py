"""
Pandas & NumPy 实战教程 - 基于量化投资项目
本教程结合项目中的实际代码，讲解 pandas 和 numpy 的核心用法
"""

import pandas as pd
import numpy as np
from modules.data_fetcher import DataFetcher
from modules.indicators import Indicators

print("=" * 60)
print("Pandas & NumPy 实战学习教程")
print("=" * 60)

# ========== 第一部分：NumPy 核心功能 ==========
print("\n" + "=" * 60)
print("第一部分：NumPy 核心功能")
print("=" * 60)

# 1.1 创建数组
print("\n1.1 创建数组")
arr1 = np.array([1, 2, 3, 4, 5])
print(f"一维数组: {arr1}")

arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n二维数组:\n{arr2}")

# 1.2 常用数组生成
print("\n1.2 常用数组生成")
zeros_arr = np.zeros((3, 4))  # 全0数组
ones_arr = np.ones((2, 3))    # 全1数组
range_arr = np.arange(0, 10, 2)  # 等差数列
print(f"arange数组: {range_arr}")

# 1.3 数组运算（向量化操作）
print("\n1.3 数组运算（向量化操作）")
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"a + b = {a + b}")
print(f"a * b = {a * b}")
print(f"a ** 2 = {a ** 2}")

# 1.4 统计函数（项目中常用）
print("\n1.4 统计函数")
data = np.array([10, 20, 30, 40, 50])
print(f"平均值: {np.mean(data)}")
print(f"标准差: {np.std(data)}")
print(f"最大值: {np.max(data)}")
print(f"累加和: {np.cumsum(data)}")

# 1.5 项目中的 NumPy 应用 - 最大回撤计算
print("\n1.5 项目实战：最大回撤计算")
equity = np.array([100000, 105000, 102000, 110000, 108000, 115000])
peak = np.maximum.accumulate(equity)  # 累积最大值
drawdown = (peak - equity) / peak
max_drawdown = np.max(drawdown)
print(f"权益曲线: {equity}")
print(f"峰值曲线: {peak}")
print(f"回撤: {drawdown}")
print(f"最大回撤: {max_drawdown:.2%}")

# ========== 第二部分：Pandas 核心功能 ==========
print("\n" + "=" * 60)
print("第二部分：Pandas 核心功能")
print("=" * 60)

# 2.1 创建 DataFrame
print("\n2.1 创建 DataFrame")
data = {
    'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'open': [10.0, 10.5, 10.3, 10.8, 11.0],
    'high': [10.8, 10.9, 11.0, 11.2, 11.5],
    'low': [9.8, 10.2, 10.1, 10.5, 10.8],
    'close': [10.5, 10.3, 10.8, 11.0, 11.2],
    'volume': [1000000, 1200000, 950000, 1500000, 1800000]
}
df = pd.DataFrame(data)
print(df)

# 2.2 数据选择与索引
print("\n2.2 数据选择与索引")
print("\n选择单列:")
print(df['close'])

print("\n选择多列:")
print(df[['open', 'close']])

print("\n条件筛选 (收盘价 > 10.5):")
print(df[df['close'] > 10.5])

# 2.3 数据清洗与转换
print("\n2.3 数据清洗与转换")
df['return'] = df['close'].pct_change()  # 计算收益率
df['log_return'] = np.log(df['close'] / df['close'].shift(1))  # 对数收益率
print(df)

# 2.4 时间序列处理
print("\n2.4 时间序列处理")
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
print(f"\n设置日期为索引:\n{df.index}")

# 2.5 滚动窗口计算（项目核心）
print("\n2.5 滚动窗口计算 - 移动平均线")
df['ma3'] = df['close'].rolling(window=3).mean()
df['ma5'] = df['close'].rolling(window=5).mean()
print(df[['close', 'ma3', 'ma5']])

# 2.6 项目实战：获取真实股票数据
print("\n" + "=" * 60)
print("第三部分：项目实战 - 真实股票数据分析")
print("=" * 60)

# 获取股票数据
print("\n正在获取股票数据...")
fetcher = DataFetcher()
stock_df = fetcher.get_stock_data('600000', start_date='2024-01-01', end_date='2024-06-01')

if not stock_df.empty:
    print(f"\n数据获取成功！共 {len(stock_df)} 条记录")
    print("\n前5行数据:")
    print(stock_df.head())
    
    print("\n数据统计信息:")
    print(stock_df.describe())
    
    # 计算技术指标
    print("\n计算技术指标...")
    stock_df = Indicators.calculate_ma(stock_df)
    stock_df = Indicators.calculate_rsi(stock_df)
    stock_df = Indicators.calculate_bollinger_bands(stock_df)
    
    print("\n添加指标后的前10行:")
    print(stock_df[['date', 'close', 'ma5', 'ma20', 'rsi', 'bb_upper', 'bb_lower']].head(10))
    
    # 简单策略演示
    print("\n" + "=" * 60)
    print("策略演示：均线交叉信号")
    print("=" * 60)
    
    stock_df['signal'] = 0
    stock_df.loc[stock_df['ma5'] > stock_df['ma20'], 'signal'] = 1  # 金叉
    stock_df.loc[stock_df['ma5'] < stock_df['ma20'], 'signal'] = -1  # 死叉
    
    # 找出交易信号
    signals = stock_df[stock_df['signal'] != stock_df['signal'].shift(1)]
    print("\n交易信号点:")
    print(signals[['date', 'close', 'ma5', 'ma20', 'signal']])

print("\n" + "=" * 60)
print("教程完成！")
print("=" * 60)
print("\n关键知识点总结：")
print("1. NumPy: 高效的数值计算，向量化操作，统计函数")
print("2. Pandas: 数据处理，时间序列，滚动窗口，条件筛选")
print("3. 职场应用：数据分析、量化交易、金融建模都离不开这两个库")
