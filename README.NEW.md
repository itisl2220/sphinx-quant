# Sphinx Quant - 量化交易平台

重构后的项目，采用 FastAPI + PostgreSQL 后端和 Vue3 + Element Plus + Vite + TypeScript 前端。

## 项目结构

```
sphinx-quant/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   └── schemas/     # Pydantic 模式
│   ├── alembic/         # 数据库迁移
│   └── requirements.txt
├── frontend/        # Vue3 前端
│   ├── src/
│   │   ├── api/         # API 客户端
│   │   ├── views/       # 页面组件
│   │   ├── layouts/     # 布局组件
│   │   ├── stores/      # Pinia 状态管理
│   │   └── types/       # TypeScript 类型
│   └── package.json
└── docker-compose.new.yml
```

## 快速开始

### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Docker Compose

```bash
# 启动所有服务
docker-compose -f docker-compose.new.yml up -d

# 查看日志
docker-compose -f docker-compose.new.yml logs -f

# 停止服务
docker-compose -f docker-compose.new.yml down
```

## 技术栈

### 后端
- FastAPI - 现代、快速的 Web 框架
- PostgreSQL - 关系型数据库
- SQLAlchemy - ORM
- Alembic - 数据库迁移
- Celery - 异步任务队列
- JWT - 身份认证

### 前端
- Vue 3 - 渐进式 JavaScript 框架
- Element Plus - Vue 3 组件库
- Vite - 下一代前端构建工具
- TypeScript - 类型安全的 JavaScript
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP 客户端

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发

### 后端开发

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm run dev
```

前端开发服务器运行在 http://localhost:5173，已配置代理到后端 API。

## 部署

### 生产环境

1. 配置环境变量
2. 构建前端：`cd frontend && npm run build`
3. 使用 Docker Compose 部署或单独部署各服务

## 迁移说明

从 Django 迁移到 FastAPI：
- 数据库模型从 Django ORM 迁移到 SQLAlchemy
- API 视图从 Django REST Framework 迁移到 FastAPI
- 认证从 JWT (djangorestframework-jwt) 迁移到 python-jose
- 数据库从 MySQL 迁移到 PostgreSQL

从 React/Ant Design Pro 迁移到 Vue3/Element Plus：
- 组件库从 Ant Design 迁移到 Element Plus
- 状态管理从 dva 迁移到 Pinia
- 构建工具从 webpack 迁移到 Vite

