// 仪表盘页面JavaScript

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
});

async function loadDashboardData() {
    try {
        // 示例：加载默认策略的统计数据
        // 实际应用中应该从后端API获取
        const mockData = {
            total_return: 0.25,
            annual_return: 0.12,
            sharpe_ratio: 1.5,
            max_drawdown: 0.08
        };

        updateMetrics(mockData);
    } catch (error) {
        console.error('加载仪表盘数据失败:', error);
    }
}

function updateMetrics(data) {
    document.getElementById('totalReturn').textContent = formatPercent(data.total_return);
    document.getElementById('annualReturn').textContent = formatPercent(data.annual_return);
    document.getElementById('sharpeRatio').textContent = formatNumber(data.sharpe_ratio);
    document.getElementById('maxDrawdown').textContent = formatPercent(data.max_drawdown);
}

function drawDashboardChart() {
    const chartContainer = document.getElementById('equityCurve');
    chartContainer.innerHTML = '<canvas id="dashboardCanvas"></canvas>';

    const canvas = document.getElementById('dashboardCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = chartContainer.clientWidth;
    canvas.height = 500;

    // 示例图表
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#333';
    ctx.font = '14px Arial';
    ctx.fillText('权益曲线图表区域', canvas.width / 2 - 50, canvas.height / 2);
}
