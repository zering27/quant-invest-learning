# 部署到 Render (免费方案)

## 准备工作

1. 注册 GitHub 账号 (https://github.com)
2. 注册 Render 账号 (https://render.com)

## 步骤一：推送到 GitHub

1. 在 GitHub 创建新仓库
2. 推送项目代码：

```bash
cd /Users/chenzerui/Documents/TRAE\ SOLO\ CN/quant-invest-learning

# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 连接到远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

## 步骤二：在 Render 部署

1. 访问 https://render.com 并登录
2. 点击 **"New +"** → **"Web Service"**
3. 选择刚才创建的 GitHub 仓库
4. 配置部署参数：

| 参数 | 值 |
|------|-----|
| Name | quant-invest-learning |
| Region | 选择离你最近的地区 |
| Branch | main |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT app:app` |

5. 点击 **"Create Web Service"**
6. 等待几分钟，部署完成后会获得一个免费域名！

## 访问您的网站

部署成功后，您的网站地址类似：
`https://quant-invest-learning-abc123.onrender.com`

## 注意事项

- 免费版有休眠期（15分钟无访问会休眠）
- 再次访问时需要约30秒唤醒
- 每月有免费额度限制
