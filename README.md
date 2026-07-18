# AI 项目合集

我的 AI 学习与实践项目仓库，涵盖大模型 API 调用、RAG 检索增强生成、Flask Web 开发、云服务器部署。

## 技术栈

- **语言**：Python
- **AI**：DeepSeek API、BGE Embedding 模型、ChromaDB 向量数据库
- **Web**：Flask、HTML、CSS、JavaScript
- **运维**：Linux、Nginx、阿里云 ECS、域名解析、SSH

## 项目列表

### 🤖 AI 聊天助手（`ai_chat.py`）
多轮对话 AI，支持上下文记忆。技术点：DeepSeek API 调用、对话历史管理。

### 📋 AI 周报生成器（`weekly_report.py`）
输入关键词自动生成格式化周报。技术点：System Prompt 角色设定。

### 📄 AI 简历优化助手
- 命令行版（`resume_ai.py`）——粘贴简历，AI 评分、优化项目经历、生成自我介绍，支持保存结果到文件
- 网页版（`web_resume.py` + `templates/index.html`）——浏览器操作，更美观的交互界面

### 🔍 RAG 智能问答系统
- 命令行版（`rag_qa.py`）——上传文档 → 向量化 → 语义搜索 → AI 回答
- 网页版（`web_rag.py` + `templates/rag.html`）——支持文件上传、对话历史、原文出处展示

技术点：滑动窗口重叠切块、BAAI/bge-small-zh-v1.5 中文 Embedding、ChromaDB 向量检索

## 在线体验

🌐 **https://mango11.me**（备案中）

当前可直接访问：
- 简历助手：`mango11.me:5000`
- RAG 问答：`mango11.me:5001`

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行网页版简历助手
python web_resume.py

# 运行网页版 RAG 问答
python web_rag.py
```

## 部署

全部项目部署在阿里云 ECS（Ubuntu 22.04），使用 Nginx 反向代理 + systemd 进程守护。
