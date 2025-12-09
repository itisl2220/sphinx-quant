# 项目重构总结

## 重构内容

项目已从 Django + MySQL + React 重构为 FastAPI + PostgreSQL + Vue3。

## 后端重构 (Django → FastAPI)

### 技术栈变更
- **框架**: Django → FastAPI
- **数据库**: MySQL → PostgreSQL
- **ORM**: Django ORM → SQLAlchemy
- **迁移工具**: Django Migrations → Alembic
- **认证**: djangorestframework-jwt → python-jose

### 项目结构
```
backend/
├── app/
│   ├── api/v1/endpoints/    # API 端点
│   │   ├── auth.py           # 认证
│   │   ├── users.py          # 用户
│   │   ├── strategies.py     # 策略
│   │   └── backtests.py      # 回测
│   ├── core/                 # 核心配置
│   │   ├── config.py         # 配置
│   │   ├── database.py       # 数据库
│   │   └── security.py       # 安全
│   ├── models/               # 数据库模型
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── source_code.py
│   │   ├── strategy.py
│   │   └── backtest.py
│   └── schemas/              # Pydantic 模式
│       ├── user.py
│       ├── token.py
│       ├── source_code.py
│       ├── strategy.py
│       └── backtest.py
├── alembic/                  # 数据库迁移
└── requirements.txt
```

### 主要变更
1. **模型迁移**: 从 Django Model 迁移到 SQLAlchemy Model
2. **API 视图**: 从 Django REST Framework 迁移到 FastAPI 路由
3. **序列化**: 从 DRF Serializer 迁移到 Pydantic Schema
4. **认证**: 从 JWT (djangorestframework-jwt) 迁移到 python-jose

## 前端重构 (React/Ant Design Pro → Vue3/Element Plus)

### 技术栈变更
- **框架**: React → Vue 3
- **组件库**: Ant Design Pro → Element Plus
- **构建工具**: Webpack → Vite
- **语言**: JavaScript → TypeScript
- **状态管理**: dva → Pinia
- **路由**: React Router → Vue Router

### 项目结构
```
frontend/
├── src/
│   ├── api/                  # API 客户端
│   │   ├── index.ts
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   ├── strategy.ts
│   │   └── backtest.ts
│   ├── views/                # 页面组件
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── Strategies/
│   │   └── Backtests/
│   ├── layouts/              # 布局组件
│   │   └── BasicLayout.vue
│   ├── stores/               # Pinia 状态管理
│   │   └── user.ts
│   ├── types/                # TypeScript 类型
│   │   ├── user.ts
│   │   ├── auth.ts
│   │   ├── strategy.ts
│   │   └── backtest.ts
│   └── router/               # 路由配置
│       └── index.ts
├── package.json
└── vite.config.ts
```

### 主要变更
1. **组件**: 从 React 类组件/函数组件迁移到 Vue 3 Composition API
2. **状态管理**: 从 dva 迁移到 Pinia
3. **路由**: 从 React Router 迁移到 Vue Router
4. **UI 组件**: 从 Ant Design 迁移到 Element Plus

## API 端点映射

### 认证
- `POST /api/v1/auth/login` - 登录（原 `POST /api-token-auth`）

### 用户
- `GET /api/v1/users/me` - 获取当前用户（原 `GET /currentUser`）

### 策略
- `GET /api/v1/strategies/` - 策略列表（原 `GET /strategy/list`）
- `GET /api/v1/strategies/{id}` - 策略详情（原 `GET /strategy/detail/{id}`）
- `POST /api/v1/strategies/` - 创建策略（原 `POST /strategy/create`）
- `PUT /api/v1/strategies/{id}` - 更新策略（原 `PUT /strategy/detail/{id}`）
- `DELETE /api/v1/strategies/{id}` - 删除策略（原 `DELETE /strategy/detail/{id}`）

### 回测
- `GET /api/v1/backtests/` - 回测列表（原 `GET /backtest/list`）
- `GET /api/v1/backtests/{id}` - 回测详情（原 `GET /backtest/detail/{id}`）
- `POST /api/v1/backtests/{strategy_id}/test` - 启动回测（原 `POST /backtest/test/{id}`）

## 数据库迁移

### 模型对应关系
- `SourceCode` - 策略代码（保持不变）
- `Strategy` - 策略（保持不变）
- `Backtest` - 回测（保持不变）
- `User` - 用户（从 Django User 迁移）

### 迁移步骤
1. 使用 Alembic 创建初始迁移
2. 从 MySQL 导出数据
3. 转换数据格式（如需要）
4. 导入到 PostgreSQL

## 部署

### Docker Compose
新的 `docker-compose.new.yml` 包含：
- PostgreSQL 数据库
- RabbitMQ 消息队列
- FastAPI 后端服务
- Celery Worker
- Vue3 前端服务

### 环境变量
后端需要配置 `.env` 文件（参考 `backend/.env.example`）

## 下一步

1. **数据迁移**: 从 MySQL 迁移数据到 PostgreSQL
2. **Celery 任务**: 迁移回测任务到新的 Celery 配置
3. **测试**: 编写单元测试和集成测试
4. **文档**: 完善 API 文档和开发文档

## 注意事项

1. 旧的前端代码在 `frontend/` 目录，新的前端代码在 `frontend/` 目录
2. 旧的 Django 后端代码在 `sphinxquant/` 目录，新的 FastAPI 后端代码在 `backend/` 目录
3. 使用 `docker-compose.new.yml` 启动新架构的服务
4. 数据库迁移需要手动执行 Alembic 命令

