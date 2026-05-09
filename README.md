# 🕸️ 古诗文网自动化抓取与交互系统 (Gushiwen-Spider)

这是一个基于 Python 开发的 Web 自动化抓取与数据交互脚本。突破了传统的静态页面爬取，实现了涵盖身份认证、会话维持、Ajax 逆向分析到数据批量处理的完整闭环。

## 💡 核心特性 (Features)

- **🔐 模拟登录与身份认证**：
  - 成功破解 ASP.NET 架构下的 `__VIEWSTATE` 与 `__VIEWSTATEGENERATOR` 隐藏域安全机制。
  - 实现验证码图片的动态捕获与同步会话校验。
- **🌐 Session 状态全局维持**：
  - 基于 `requests.Session()` 实现跨页面的 Cookie 自动管理。
  - 攻克了 JavaScript `window.location` 客户端重定向导致的请求断层问题。
- **⚙️ 动态 API 逆向与自动化交互**：
  - 通过 F12 抓包分析出 Ajax 收藏接口的底层逻辑。
  - 利用正则表达式精准提取动态防御 Token，实现规避缓存 (Cache-Busting) 的批量自动化收藏与取消收藏。
- **🛡️ 健壮的工程化设计**：
  - 内置边界判断逻辑（自动识别末尾页并安全退出）。
  - 合理的请求节流（Sleep）与防封控策略。

## 🛠️ 技术栈 (Tech Stack)
- **Python 3.x**
- **Requests**: HTTP 核心请求库，负责构建 Headers、管理 Session 与发起数据包。
- **BeautifulSoup4 & lxml**: DOM 树解析与页面信息提取。
- **Re (正则表达式)**: 复杂 JavaScript 函数体内的 Token 精准切割与匹配。

## 🚀 快速开始 (Quick Start)

1. 克隆本项目到本地：
   `git clone https://github.com/YourUsername/Gushiwen-Spider.git`
2. 安装依赖包：
   `pip install -r requirements.txt`
3. 运行主程序：
   `python spider.py`
4. 根据终端提示，输入需要搜索的诗人名称（如“李白”）、扫描页数以及验证码即可。

## ⚠️ 声明 (Disclaimer)
本项目仅供 Python 爬虫技术学习与交流使用，禁止用于任何恶意攻击或商业用途。代码中已去除个人真实账户信息。
