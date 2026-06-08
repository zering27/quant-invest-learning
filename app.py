"""
量化投资学习系统 - Flask应用主文件
"""

from flask import Flask, render_template, request, jsonify
import config
import os

app = Flask(__name__)
app.config.from_object(config.FLASK_CONFIG)


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/backtest')
def backtest():
    """回测页面"""
    return render_template('backtest.html')


@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    return render_template('dashboard.html')


# ========================================
# 学习系统路由
# ========================================

@app.route('/learn')
def learn():
    """学习中心首页"""
    return render_template('learn/learn_center.html')


@app.route('/learn/python')
def learn_python():
    """模块1: Python金融编程基础"""
    return render_template('learn/module1_python.html')


@app.route('/learn/data')
def learn_data():
    """模块2: 金融市场数据获取"""
    return render_template('learn/module2_data.html')


@app.route('/learn/indicators')
def learn_indicators():
    """模块3: 技术分析指标"""
    return render_template('learn/module3_indicators.html')


@app.route('/learn/backtest')
def learn_backtest():
    """模块4: 策略回测框架"""
    return render_template('learn/module4_backtest.html')


@app.route('/learn/risk')
def learn_risk():
    """模块5: 风险管理与实战"""
    return render_template('learn/module5_risk.html')


# ========================================
# API路由
# ========================================

@app.route('/api/stock/<code>')
def get_stock_data(code):
    """获取股票数据API"""
    from modules.data_fetcher import DataFetcher
    fetcher = DataFetcher()
    data = fetcher.get_stock_data(code)
    return jsonify(data)


@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """执行回测API"""
    from modules.backtester import Backtester
    params = request.json
    bt = Backtester(params)
    result = bt.run()
    return jsonify(result)


if __name__ == '__main__':
    # 优先使用环境变量中的 PORT，否则使用配置文件中的
    port = int(os.environ.get('PORT', config.FLASK_CONFIG['PORT']))
    host = os.environ.get('HOST', config.FLASK_CONFIG['HOST'])
    app.run(
        host=host,
        port=port,
        debug=config.FLASK_CONFIG['DEBUG']
    )
