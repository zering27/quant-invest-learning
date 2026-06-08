/* ========================================
   量化投资学习系统 - JavaScript交互
   ======================================== */

// 切换侧边栏
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.querySelector('.content');
    
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
    
    // 添加平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 监控滚动位置更新进度条
    window.addEventListener('scroll', updateProgressFromScroll);
    
    // 初始化当前模块进度
    initModuleProgress();
});

// 根据滚动位置更新进度条
function updateProgressFromScroll() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        // 计算模块内的相对进度
        const contentSections = document.querySelectorAll('.section');
        let currentSectionIndex = 0;
        
        contentSections.forEach((section, index) => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= window.innerHeight / 2) {
                currentSectionIndex = index;
            }
        });
        
        const moduleProgress = (currentSectionIndex + 1) / contentSections.length * 100;
        const baseProgress = parseInt(progressBar.style.width) || 0;
        
        // 平滑更新进度
        if (moduleProgress > baseProgress) {
            progressBar.style.width = moduleProgress + '%';
        }
    }
}

// 初始化模块进度
function initModuleProgress() {
    // 根据当前页面设置初始进度
    const path = window.location.pathname;
    const progressMap = {
        '/learn/python': 20,
        '/learn/data': 40,
        '/learn/indicators': 60,
        '/learn/backtest': 80,
        '/learn/risk': 100
    };
    
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        const progress = progressMap[path] || 0;
        progressBar.style.width = progress + '%';
    }
}

// 代码块折叠功能（可选）
function toggleCodeBlock(button) {
    const codeBlock = button.parentElement.querySelector('pre');
    if (codeBlock) {
        codeBlock.classList.toggle('collapsed');
        button.textContent = codeBlock.classList.contains('collapsed') ? '显示代码' : '隐藏代码';
    }
}

// 复制代码功能
function copyCode(button) {
    const codeBlock = button.parentElement.querySelector('code');
    if (codeBlock) {
        navigator.clipboard.writeText(codeBlock.textContent).then(() => {
            const originalText = button.textContent;
            button.textContent = '已复制!';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        });
    }
}

// 添加代码复制按钮
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.code-section').forEach(section => {
        const pre = section.querySelector('pre');
        if (pre) {
            // 创建复制按钮
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.textContent = '复制';
            copyBtn.onclick = function() { copyCode(this); };
            
            // 创建折叠按钮（仅当代码较长时）
            if (pre.scrollHeight > 200) {
                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'toggle-btn';
                toggleBtn.textContent = '折叠';
                toggleBtn.onclick = function() { toggleCodeBlock(this); };
                section.insertBefore(toggleBtn, pre);
            }
            
            section.insertBefore(copyBtn, pre);
        }
    });
});

// 导航高亮
function highlightNavigation() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-menu a, .nav-menu a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// 运行简单的Python代码片段（浏览器端模拟，仅用于教学演示）
function simulatePythonOutput(codeId) {
    const codeElement = document.getElementById(codeId);
    if (codeElement) {
        // 这里只是简单的教学演示，实际不会运行Python
        // 在真实环境中可能需要后端API支持
        console.log('Python simulation requested for:', codeId);
    }
}
