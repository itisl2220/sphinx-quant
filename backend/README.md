# Sphinx Quant Backend

FastAPI + PostgreSQL 后端项目

## 环境要求

- Python 3.10+
- PostgreSQL 12+
- RabbitMQ (用于 Celery)

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

## 数据库初始化

使用 SQL 文件直接初始化数据库：

```bash
# 使用 psql 执行 SQL 文件
psql -U postgres -d sphinxquant -f init_db.sql

# 或者在 PostgreSQL 客户端中直接执行 init_db.sql 文件
```

详细说明请查看 [README_SQL.md](README_SQL.md)

## 运行

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API 文档

启动服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/          # API 路由
│   ├── core/         # 核心配置
│   ├── models/       # 数据库模型
│   └── schemas/      # Pydantic 模式
├── init_db.sql       # 数据库初始化 SQL
├── README_SQL.md     # SQL 初始化说明
└── requirements.txt  # 依赖列表
```

