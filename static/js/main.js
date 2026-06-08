// 量化投资学习系统 - 主JS文件

document.addEventListener('DOMContentLoaded', function() {
    console.log('量化投资学习系统已加载');
});

// API请求辅助函数
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}

// 格式化数字
function formatNumber(num, decimals = 2) {
    if (typeof num !== 'number' || isNaN(num)) {
        return '--';
    }
    return num.toFixed(decimals);
}

// 格式化百分比
function formatPercent(num) {
    if (typeof num !== 'number' || isNaN(num)) {
        return '--';
    }
    return (num * 100).toFixed(2) + '%';
}
