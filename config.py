"""
配置文件 - 量化投资学习系统
"""

# 数据源配置
DATA_SOURCE = {
    'baostock': {
        'enabled': True,
        'username': '',
        'password': ''
    },
    'akshare': {
        'enabled': True,
        '备用数据源': True
    }
}

# 回测默认参数
BACKTEST_CONFIG = {
    'initial_capital': 1000000,      # 初始资金 100万
    'commission_rate': 0.0003,       # 手续费 0.03%
    'stamp_tax': 0.001,              # 印花税 0.1% (卖出时收取)
    'slippage': 0.001,               # 滑点 0.1%
    'default_start_date': '2020-01-01',
    'default_end_date': '2024-12-31'
}

# Flask应用配置
FLASK_CONFIG = {
    'SECRET_KEY': 'quant-invest-learning-secret-key',
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5001
}

# 风险参数
RISK_CONFIG = {
    'max_position_size': 0.2,        # 单只股票最大仓位 20%
    'max_total_position': 0.9,        # 最大总仓位 90%
    'stop_loss': 0.05,               # 止损线 5%
    'take_profit': 0.15              # 止盈线 15%
}

# 技术指标默认参数
INDICATOR_CONFIG = {
    'ma_periods': [5, 10, 20, 60],   # 均线周期
    'rsi_period': 14,                # RSI周期
    'bollinger_period': 20,          # 布林带周期
    'bollinger_std': 2,              # 布林带标准差倍数
    'macd_fast': 12,                 # MACD快线周期
    'macd_slow': 26,                 # MACD慢线周期
    'macd_signal': 9                 # MACD信号线周期
}
