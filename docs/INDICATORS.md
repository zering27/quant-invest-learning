# 技术分析指标详解

本文档详细介绍了常用技术分析指标的原理、计算方法和Python实现。

## 目录

1. [移动平均线 MA](#移动平均线-ma)
2. [MACD](#macd)
3. [RSI相对强弱指标](#rsi)
4. [布林带 Bollinger Bands](#布林带)

---

## 移动平均线 MA

### 原理

移动平均线（Moving Average）是趋势跟踪指标，通过计算一定周期内的平均价格来平滑价格波动。

### 计算公式

**简单移动平均 (SMA):**
```
SMA = (C₁ + C₂ + ... + Cₙ) / n
```

**指数移动平均 (EMA):**
```
EMA = (Close - EMA_prev) × k + EMA_prev
其中 k = 2/(n+1)
```

### Python实现

```python
import pandas as pd

def calculate_ma(df, window):
    """计算简单移动平均"""
    return df['close'].rolling(window=window).mean()

def calculate_ema(df, span):
    """计算指数移动平均"""
    return df['close'].ewm(span=span, adjust=False).mean()
```

---

## MACD

### 原理

MACD（Moving Average Convergence Divergence）由Gerald Appel创建，利用两条不同速度的EMA来研判买卖时机。

### 计算公式

```
DIF = EMA(close, 12) - EMA(close, 26)
DEA = EMA(DIF, 9)
MACD = (DIF - DEA) × 2
```

### Python实现

```python
def calculate_macd(df, fast=12, slow=26, signal=9):
    df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
    df['DIF'] = df['EMA_fast'] - df['EMA_slow']
    df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
    df['MACD'] = (df['DIF'] - df['DEA']) * 2
    return df
```

### 交易信号

| 信号 | 条件 |
|------|------|
| 金叉买入 | DIF从下往上穿过DEA |
| 死叉卖出 | DIF从上往下穿过DEA |
| 零轴之上 | 多头趋势较强 |
| 零轴之下 | 空头趋势较强 |

---

## RSI

### 原理

RSI（Relative Strength Index）衡量价格上涨和下跌的幅度，用于判断超买超卖状态。

### 计算公式

```
RS = 平均涨幅 / 平均跌幅
RSI = 100 - (100 / (1 + RS))
```

### Python实现

```python
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.ewm(com=period-1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period-1, min_periods=period).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df
```

### 交易信号

| RSI范围 | 市场状态 | 信号 |
|---------|----------|------|
| > 70 | 超买区 | 考虑卖出 |
| < 30 | 超卖区 | 考虑买入 |
| > 80 | 严重超买 | 强烈卖出信号 |
| < 20 | 严重超卖 | 强烈买入信号 |

---

## 布林带

### 原理

布林带由John Bollinger发明，由三条线组成，反映价格的波动范围。

### 计算公式

```
中轨 = MA(close, 20)
标准差 = Std(close, 20)
上轨 = 中轨 + 2 × 标准差
下轨 = 中轨 - 2 × 标准差
```

### Python实现

```python
def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['BB_middle'] = df['close'].rolling(window=period).mean()
    rolling_std = df['close'].rolling(window=period).std()
    df['BB_upper'] = df['BB_middle'] + (rolling_std * std_dev)
    df['BB_lower'] = df['BB_middle'] - (rolling_std * std_dev)
    return df
```

### 交易信号

| 信号 | 条件 | 含义 |
|------|------|------|
| 突破上轨 | 价格 > 上轨 | 可能强势，考虑买入 |
| 跌破下轨 | 价格 < 下轨 | 可能弱势，考虑卖出 |
| 收窄 | 带宽变小 | 可能大幅波动 |

---

## 指标使用注意事项

### 1. 单一指标的局限性

没有任何指标是万能的。不同市场环境需要使用不同的指标组合。

### 2. 指标参数优化

参数选择对结果影响很大，需要通过回测优化。

### 3. 指标组合使用

建议使用2-3个指标组合，提高信号的可靠性：

- 趋势指标 + 振荡指标
- 短期指标 + 长期指标

### 4. 结合止损

无论使用何种指标，都必须设置止损，控制单次交易的最大亏损。
