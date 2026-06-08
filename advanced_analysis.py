"""
Pandas & NumPy 高级实战案例
深入学习数据处理、统计分析和可视化
"""

import pandas as pd
import numpy as np
from modules.data_fetcher import DataFetcher
from modules.indicators import Indicators
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("=" * 60)
print("Pandas & NumPy 高级实战案例")
print("=" * 60)

# ========== 第一部分：高级数据处理 ==========
print("\n" + "=" * 60)
print("第一部分：高级数据处理")
print("=" * 60)

# 1.1 获取多只股票数据进行对比分析
print("\n1.1 获取多只股票数据")
fetcher = DataFetcher()

stocks = {
    '600000': '浦发银行',
    '600036': '招商银行',
    '601318': '中国平安'
}

stock_data = {}
for code, name in stocks.items():
    print(f"正在获取 {name} ({code}) 的数据...")
    df = fetcher.get_stock_data(code, start_date='2024-01-01', end_date='2024-06-01')
    if not df.empty:
        df['stock_code'] = code
        df['stock_name'] = name
        stock_data[code] = df

# 合并数据
all_data = pd.concat(stock_data.values(), ignore_index=True)
print(f"\n合并后数据形状: {all_data.shape}")
print(all_data.head())

# 1.2 数据透视表 - 按股票统计
print("\n1.2 数据透视表分析")
pivot_close = all_data.pivot(index='date', columns='stock_name', values='close')
print("\n收盘价透视表:")
print(pivot_close.head())

# 1.3 计算相关系数矩阵
print("\n1.3 收益率相关性分析")
returns = pivot_close.pct_change().dropna()
corr_matrix = returns.corr()
print("\n相关系数矩阵:")
print(corr_matrix)

# ========== 第二部分：高级统计分析 ==========
print("\n" + "=" * 60)
print("第二部分：高级统计分析")
print("=" * 60)

# 2.1 描述性统计
print("\n2.1 收益率统计描述")
stats_summary = returns.describe()
print(stats_summary)

# 2.2 滚动统计分析
print("\n2.2 滚动波动率计算")
for stock in stocks.values():
    pivot_close[f'{stock}_vol'] = pivot_close[stock].pct_change().rolling(window=20).std() * np.sqrt(252)

print("\n滚动波动率（20日）:")
print(pivot_close[[s for s in stocks.values()]].tail())

# 2.3 分组聚合分析
print("\n2.3 月度收益率分析")
all_data['date'] = pd.to_datetime(all_data['date'])
all_data['year_month'] = all_data['date'].dt.to_period('M')

# 计算月度收益率
monthly_returns = all_data.groupby(['stock_name', 'year_month']).apply(
    lambda x: (x['close'].iloc[-1] / x['close'].iloc[0] - 1)
).reset_index(name='monthly_return')

print("\n月度收益率:")
print(monthly_returns)

# ========== 第三部分：高级策略分析 ==========
print("\n" + "=" * 60)
print("第三部分：高级策略分析")
print("=" * 60)

# 3.1 双均线策略优化
print("\n3.1 双均线策略参数优化")
# 以浦发银行为例
df_pufa = stock_data['600000'].copy()
df_pufa = Indicators.calculate_ma(df_pufa, periods=[5, 10, 20, 60])

# 测试不同均线组合
def test_ma_strategy(df, fast_period, slow_period):
    """测试均线策略"""
    df = df.copy()
    df[f'ma_fast'] = df['close'].rolling(window=fast_period).mean()
    df[f'ma_slow'] = df['close'].rolling(window=slow_period).mean()
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['ma_fast'] > df['ma_slow'], 'signal'] = 1
    df.loc[df['ma_fast'] < df['ma_slow'], 'signal'] = -1
    
    # 计算策略收益率
    df['return'] = df['close'].pct_change()
    df['strategy_return'] = df['signal'].shift(1) * df['return']
    
    # 计算累计收益率
    df['cum_return'] = (1 + df['return']).cumprod()
    df['cum_strategy'] = (1 + df['strategy_return']).cumprod()
    
    # 统计指标
    total_return = df['cum_strategy'].iloc[-1] - 1 if not df.empty else 0
    return total_return

# 网格搜索
param_combinations = [(5, 20), (10, 30), (5, 60), (10, 60), (20, 60)]
results = []

for fast, slow in param_combinations:
    ret = test_ma_strategy(df_pufa, fast, slow)
    results.append({
        'fast_ma': fast,
        'slow_ma': slow,
        'total_return': ret
    })

results_df = pd.DataFrame(results)
print("\n参数优化结果:")
print(results_df.sort_values('total_return', ascending=False))

# 3.2 RSI策略结合均线
print("\n3.2 RSI+均线组合策略")
df_pufa = Indicators.calculate_rsi(df_pufa)

# 先计算收益率
df_pufa['return'] = df_pufa['close'].pct_change()

# 组合策略：RSI超卖 + 均线向上
df_pufa['combined_signal'] = 0
df_pufa.loc[(df_pufa['rsi'] < 30) & (df_pufa['ma5'] > df_pufa['ma20']), 'combined_signal'] = 1
df_pufa.loc[(df_pufa['rsi'] > 70) & (df_pufa['ma5'] < df_pufa['ma20']), 'combined_signal'] = -1

# 计算组合策略收益
df_pufa['combined_strategy_return'] = df_pufa['combined_signal'].shift(1) * df_pufa['return']
df_pufa['cum_combined'] = (1 + df_pufa['combined_strategy_return']).cumprod()

print("\n组合策略前20行信号:")
print(df_pufa[['date', 'close', 'ma5', 'ma20', 'rsi', 'combined_signal', 'cum_combined']].head(20))

# ========== 第四部分：实用函数总结 ==========
print("\n" + "=" * 60)
print("第四部分：职场实用函数总结")
print("=" * 60)

print("""
【Pandas 高频函数】
1. df.head() / df.tail() - 查看首尾数据
2. df.describe() - 统计描述
3. df.info() - 数据信息
4. df.isnull().sum() - 缺失值统计
5. df.dropna() / df.fillna() - 处理缺失值
6. df.groupby() - 分组聚合
7. df.pivot_table() - 数据透视
8. df.merge() / df.concat() - 数据合并
9. df.rolling().mean() - 滚动计算
10. df.apply() - 自定义函数应用

【NumPy 高频函数】
1. np.array() - 创建数组
2. np.mean() / np.std() / np.var() - 统计函数
3. np.max() / np.min() / np.sum() - 聚合函数
4. np.cumsum() / np.cumprod() - 累积计算
5. np.maximum.accumulate() - 累积最大值
6. np.where() - 条件判断
7. np.diff() - 差分计算
8. np.log() / np.exp() - 数学函数
9. np.correlate() - 相关性
10. np.random - 随机数生成

【职场应用场景】
- 金融：量化策略开发、风险分析
- 电商：用户行为分析、销售预测
- 运营：数据报表、KPI统计
- 科研：数据清洗、统计建模
""")

print("\n" + "=" * 60)
print("高级案例学习完成！")
print("=" * 60)
