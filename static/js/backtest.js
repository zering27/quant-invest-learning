// 回测页面JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('backtestForm');
    if (form) {
        form.addEventListener('submit', handleBacktest);
    }
});

async function fetchAPI(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };

    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

async function handleBacktest(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const params = {
        stock_code: formData.get('stockCode'),
        start_date: formData.get('startDate'),
        end_date: formData.get('endDate'),
        initial_capital: parseFloat(formData.get('initialCapital')),
        strategy: formData.get('strategy')
    };

    try {
        const results = await fetchAPI('/api/backtest', {
            method: 'POST',
            body: JSON.stringify(params)
        });

        displayResults(results);
    } catch (error) {
        alert('回测执行失败: ' + error.message);
    }
}

function displayResults(results) {
    const resultsSection = document.getElementById('results');
    const metricsDiv = document.getElementById('metrics');

    resultsSection.classList.remove('hidden');

    // 显示指标
    metricsDiv.innerHTML = `
        <div class="metric-card">
            <h4>总收益率</h4>
            <div class="metric-value">${formatPercent(results.total_return)}</div>
        </div>
        <div class="metric-card">
            <h4>年化收益率</h4>
            <div class="metric-value">${formatPercent(results.annual_return)}</div>
        </div>
        <div class="metric-card">
            <h4>夏普比率</h4>
            <div class="metric-value">${formatNumber(results.sharpe_ratio)}</div>
        </div>
        <div class="metric-card">
            <h4>最大回撤</h4>
            <div class="metric-value">${formatPercent(results.max_drawdown)}</div>
        </div>
        <div class="metric-card">
            <h4>胜率</h4>
            <div class="metric-value">${formatPercent(results.win_rate)}</div>
        </div>
        <div class="metric-card">
            <h4>盈利因子</h4>
            <div class="metric-value">${formatNumber(results.profit_factor)}</div>
        </div>
    `;

    // 绘制权益曲线
    if (results.equity_curve && results.equity_curve.length > 0) {
        drawEquityCurve(results.equity_curve);
    }
}

function drawEquityCurve(equityCurve) {
    const chartContainer = document.getElementById('equityChart');
    chartContainer.innerHTML = '<canvas id="equityCanvas"></canvas>';

    const canvas = document.getElementById('equityCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = chartContainer.clientWidth;
    canvas.height = 400;

    const data = equityCurve.map(item => item.equity);
    const maxEquity = Math.max(...data);
    const minEquity = Math.min(...data);
    const range = maxEquity - minEquity;

    ctx.beginPath();
    ctx.strokeStyle = '#3498db';
    ctx.lineWidth = 2;

    data.forEach((value, index) => {
        const x = (index / (data.length - 1)) * canvas.width;
        const y = canvas.height - ((value - minEquity) / range) * canvas.height;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // 绘制标签
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.fillText(`初始资金: ${formatNumber(data[0])}`, 10, 20);
    ctx.fillText(`最终资金: ${formatNumber(data[data.length - 1])}`, 10, 40);
}