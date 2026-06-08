# 量化投资学习系统

一个完整的交互式量化投资学习平台，帮助用户从零开始学习量化投资策略。

## 📚 学习模块

### 模块1: Python金融编程基础
学习Python在量化分析中的核心工具：
- Pandas数据结构与数据处理
- NumPy数学计算
- Matplotlib/Plotly数据可视化
- 数据清洗与预处理

### 模块2: 金融市场数据获取
- baostock免费数据源使用
- 股票OHLCV数据结构
- 数据清洗与预处理
- 复权处理

### 模块3: 技术分析指标
- 移动平均线MA（趋势跟踪）
- MACD指标（指数平滑）
- RSI相对强弱（超买超卖）
- 布林带（波动率分析）

### 模块4: 策略回测框架
- 事件驱动回测原理
- 均线交叉策略实现
- 绩效评估指标（收益率、夏普比率、最大回撤）
- 避免过度拟合

### 模块5: 风险管理与实战
- 止损止盈策略
- 仓位管理（凯利公式）
- VaR风险价值
- 交易系统设计

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- Flask: Web框架
- baostock: 股票数据源
- pandas: 数据处理
- numpy: 数学计算
- plotly: 交互式图表

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问: http://localhost:5000

### 4. 开始学习

1. 访问 `/learn` 进入学习中心
2. 按顺序学习各个模块
3. 完成学习后使用 `/backtest` 进行回测实践

## 📁 项目结构

```
quant-invest-learning/
├── app.py                 # Flask应用主文件
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── modules/               # 核心模块
│   ├── backtester.py      # 回测引擎
│   ├── data_fetcher.py    # 数据获取
│   ├── indicators.py      # 技术指标
│   ├── performance.py     # 绩效评估
│   ├── portfolio.py       # 组合管理
│   └── risk_manager.py    # 风险管理
├── templates/             # HTML模板
│   ├── learn/             # 学习页面
│   │   ├── learn_base.html
│   │   ├── learn_center.html
│   │   ├── module1_python.html
│   │   ├── module2_data.html
│   │   ├── module3_indicators.html
│   │   ├── module4_backtest.html
│   │   └── module5_risk.html
│   ├── backtest.html      # 回测页面
│   ├── dashboard.html     # 仪表盘
│   └── index.html         # 首页
├── static/                # 静态资源
│   ├── css/
│   │   └── learn.css      # 学习页面样式
│   └── js/
│       └── learn.js       # 学习页面交互
└── docs/                  # 文档
    ├── README.md
    ├── QUICKSTART.md
    └── ...
```

## 🛠️ 功能特性

### 学习系统
- 左侧可折叠导航栏
- 顶部进度条显示当前模块
- 代码语法高亮
- 代码示例可复制
- 响应式布局

### 回测系统
- 支持多种策略（均线交叉、RSI、布林带）
- 自定义参数设置
- 资金曲线可视化
- 绩效指标展示
- 交易记录查询

### 数据获取
- baostock免费数据源
- 支持沪深股票
- 自动复权处理

## ⚠️ 免责声明

本项目仅供学习交流使用，不构成任何投资建议。量化投资存在风险，过往表现不能代表未来收益。入市需谨慎，投资需自负盈亏。

## 📝 学习资源

- [Pandas官方文档](https://pandas.pydata.org/)
- [baostock文档](https://www.baostock.com/)
- [Plotly文档](https://plotly.com/python/)
- [量化投资学习笔记](docs/)

## 许可证

MIT License
