# 快速启动指南

## 前置要求

- Python 3.10+
- uv (Python 包管理器)

## 安装 uv

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux / macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 快速启动

### 重要提示

**使用 uv 时，请使用 `uv run` 来运行命令，而不是直接使用 `python`。**

如果之前激活了其他虚拟环境（如 pipenv），请先退出：
```powershell
deactivate  # 退出旧环境
```

### 1. 同步依赖
```bash
uv sync --dev
```

### 2. 启动开发服务器

**Windows:**
```powershell
.\scripts\dev-start.ps1
```

**Linux / macOS:**
```bash
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh
```

服务器将在 `http://localhost:8080` 启动。

### 3. (可选) 启动 Celery Worker

在另一个终端中：

**Windows:**
```powershell
.\scripts\dev-celery.ps1
```

**Linux / macOS:**
```bash
./scripts/dev-celery.sh
```

## 手动启动步骤

如果脚本无法运行，可以手动执行：

**重要：使用 `uv run` 而不是直接使用 `python`**

```bash
# 1. 同步依赖（在项目根目录）
uv sync --dev

# 2. 进入项目目录
cd sphinxquant

# 3. 数据库迁移（使用 uv run）
uv run python manage.py makemigrations
uv run python manage.py migrate

# 4. 收集静态文件
uv run python manage.py collectstatic --noinput

# 5. 启动服务器
uv run python manage.py runserver 0.0.0.0:8080
```

**或者激活 uv 创建的虚拟环境：**
```powershell
# Windows
.venv\Scripts\activate

# 然后可以直接使用 python
python manage.py runserver
```

## 常见问题

### 依赖安装失败

某些依赖需要特殊配置，请参考 `docs/guide/uv/README.md` 中的详细说明。

### Python 版本问题

确保已安装 Python 3.10+：
```bash
uv python install 3.10
```

### 数据库连接

确保 MySQL 服务已启动，并检查 `sphinxquant/sphinxquant/settings.py` 中的数据库配置。

### uwsgi 安装失败（Windows）

`uwsgi` 仅支持 Linux/Unix 系统，在 Windows 上无法安装。这是正常的，Windows 开发环境使用 Django 自带的开发服务器即可。如需在生产环境部署，请在 Linux/Unix 系统上安装生产依赖：`uv sync --extra production`

## 更多信息

详细文档请查看：`docs/guide/uv/README.md`

