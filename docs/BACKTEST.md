# 策略回测指南

本文档介绍如何进行量化策略回测，以及如何正确解读回测结果。

## 目录

1. [什么是回测](#什么是回测)
2. [回测框架](#回测框架)
3. [回测流程](#回测流程)
4. [绩效指标](#绩效指标)
5. [常见陷阱](#常见陷阱)

---

## 什么是回测

回测是指使用历史数据模拟策略交易，评估策略在过去的表现。

### 回测的价值

1. **验证策略有效性**：策略在历史数据上是否有效
2. **参数优化**：找出最优参数组合
3. **风险评估**：了解策略的最大回撤和波动
4. **信心建立**：通过历史验证增加实盘信心

### 回测的局限性

1. **过去不代表未来**：历史表现不能保证未来收益
2. **过度拟合风险**：过度优化可能导致过拟合
3. **流动性假设**：假设能以回测价格成交
4. **忽略滑点**：实际交易存在滑点成本

---

## 回测框架

### 事件驱动回测

```python
class Backtester:
    def __init__(self, initial_capital, commission=0.0003):
        self.initial_capital = initial_capital
        self.commission = commission
        self.cash = initial_capital
        self.position = 0
        
    def on_bar(self, bar):
        """每个交易日调用一次"""
        signal = self.strategy.generate_signal(bar)
        if signal == 'BUY':
            self.buy(bar)
        elif signal == 'SELL':
            self.sell(bar)
            
    def run(self, data):
        """运行回测"""
        for bar in data:
            self.on_bar(bar)
```

---

## 回测流程

### 1. 数据准备

```python
# 获取数据
data = get_stock_data('600000', '2020-01-01', '2024-12-31')

# 数据清洗
data = clean_data(data)

# 计算指标
data = calculate_indicators(data)
```

### 2. 策略实现

```python
def strategy(row, history):
    # 金叉买入
    if row['MA5'] > row['MA20'] and history['MA5'].iloc[-1] <= history['MA20'].iloc[-1]:
        return 'BUY'
    # 死叉卖出
    if row['MA5'] < row['MA20'] and history['MA5'].iloc[-1] >= history['MA20'].iloc[-1]:
        return 'SELL'
    return 'HOLD'
```

### 3. 执行回测

```python
bt = Backtester(initial_capital=1000000)
results = bt.run(data, strategy)
```

### 4. 绩效评估

```python
metrics = calculate_performance_metrics(results)
print(metrics)
```

---

## 绩效指标

### 核心指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| 总收益率 | 策略总收益 | 越高越好 |
| 年化收益率 | 年化后的收益 | 越高越好 |
| 夏普比率 | 风险调整后收益 | > 1.5 |
| 最大回撤 | 最大亏损幅度 | < 20% |
| 胜率 | 盈利交易比例 | 越高越好 |
| 盈亏比 | 平均盈利/平均亏损 | > 1.5 |

### 详细说明

#### 总收益率

```python
total_return = (final_equity - initial_capital) / initial_capital
```

#### 年化收益率

```python
years = trading_days / 252
annual_return = (1 + total_return) ** (1/years) - 1
```

#### 夏普比率

```python
daily_returns = equity.pct_change()
sharpe = np.sqrt(252) * daily_returns.mean() / daily_returns.std()
```

#### 最大回撤

```python
peak = equity.cummax()
drawdown = (equity - peak) / peak
max_drawdown = drawdown.min()
```

---

## 常见陷阱

### 1. 过度拟合

**问题**：策略在历史数据上表现过于完美，但实盘可能无效。

**表现**：
- 胜率 > 90%
- 利润曲线过于平滑
- 参数精度要求过高

**解决方法**：
- 使用样本外数据测试
- 简化策略逻辑
- 参数敏感性分析

### 2. 前视偏差

**问题**：使用了未来才能获得的信息。

**例子**：
- 使用当天收盘价决定是否在当天买入
- 使用财务报表公布后的数据

**解决方法**：
- 确保信号使用前一日的数据
- 模拟实际交易延迟

### 3. 幸存者偏差

**问题**：只使用当前存在的股票进行回测。

**解决方法**：
- 包含已退市股票
- 使用当时可获得的数据

### 4. 忽略交易成本

**问题**：回测时未考虑手续费、滑点等成本。

**实际成本**：
- 手续费：约万分之一至万分之三
- 印花税：千分之一（卖出时）
- 滑点：0.1%-0.5%

**解决方法**：
- 在回测中加入成本估算
- 使用保守的成本假设

### 5. 流动性风险

**问题**：假设可以买卖任意数量的股票。

**解决方法**：
- 设置最大持仓比例
- 考虑每日成交量限制

---

## 最佳实践

1. **样本外验证**：将数据分为训练集和测试集
2. **稳健性检验**：测试不同市场环境下的表现
3. **敏感性分析**：检查参数变化对结果的影响
4. **Monte Carlo模拟**：多次随机模拟评估稳定性
5. **实际交易记录**：保持详细的交易日志
