# 使用 uv 进行项目开发

本项目使用 [uv](https://github.com/astral-sh/uv) 作为 Python 包管理器和项目管理工具。

## 安装 uv

### Windows

使用 PowerShell 运行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装完成后，重启终端或运行：

```bash
source $HOME/.cargo/env  # Linux
# 或
source $HOME/.zshrc      # macOS (zsh)
```

## 项目设置

### 1. 同步依赖

首次使用或更新依赖后，运行：

```bash
uv sync --dev
```

这会：
- 创建虚拟环境（如果不存在）
- 安装所有项目依赖和开发依赖
- 生成 `uv.lock` 文件

### 2. 配置额外的包索引

由于项目使用了特殊的包索引（rqdata），需要配置额外的索引源。

**方式一：使用环境变量（推荐）**

在 Windows PowerShell 中：
```powershell
$env:UV_INDEX_RQDATA_URL="https://rquser:ricequant99@py.ricequant.com/simple"
```

在 Linux/macOS 中：
```bash
export UV_INDEX_RQDATA_URL="https://rquser:ricequant99@py.ricequant.com/simple"
```

**方式二：使用命令行参数**

安装 rqdatac 时直接指定索引：
```bash
uv pip install --index-url https://rquser:ricequant99@py.ricequant.com/simple rqdatac
```

**方式三：在 pyproject.toml 中直接指定 URL**

对于需要从特定源安装的包，已在 `pyproject.toml` 中配置为直接 URL 安装。

### 3. 安装特殊依赖

某些依赖需要从特定 URL 安装，这些已经在 `pyproject.toml` 中配置：

- `ibapi`: 从腾讯云 COS 安装
- `vnpy`: 从 GitHub 仓库安装
- `rqdatac`: 从 rqdata 索引安装

如果遇到安装问题，可以手动安装：

```bash
# 安装 ibapi
uv pip install https://sphinx-1253762454.file.myqcloud.com/mirror/ibapi-9.75.1-py3-none-any.whl

# 安装 vnpy
uv pip install git+https://github.com/vnpy/vnpy.git@master

# 安装 rqdatac (需要先配置索引)
uv pip install --index-url https://rquser:ricequant99@py.ricequant.com/simple rqdatac
```

## 开发启动

### 方式一：使用启动脚本（推荐）

#### Windows

```powershell
.\scripts\dev-start.ps1
```

#### Linux / macOS

```bash
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh
```

### 方式二：手动启动

1. 同步依赖：
   ```bash
   uv sync --dev
   ```

2. 进入项目目录：
   ```bash
   cd sphinxquant
   ```

3. 运行数据库迁移：
   ```bash
   uv run python manage.py makemigrations
   uv run python manage.py migrate
   ```

4. 收集静态文件：
   ```bash
   uv run python manage.py collectstatic --noinput
   ```

5. 启动开发服务器：
   ```bash
   uv run python manage.py runserver 0.0.0.0:8080
   ```

## 启动 Celery Worker

如果需要运行 Celery 任务，在另一个终端中启动 Worker：

### Windows

```powershell
.\scripts\dev-celery.ps1
```

### Linux / macOS

```bash
./scripts/dev-celery.sh
```

或手动启动：

```bash
cd sphinxquant
uv run celery -A sphinxquant worker -l info
```

## 常用命令

### 运行 Django 管理命令

```bash
uv run python manage.py <command>
```

### 运行 Python 脚本

```bash
uv run python <script.py>
```

### 添加新依赖

```bash
# 添加生产依赖
uv add <package-name>

# 添加开发依赖
uv add --dev <package-name>
```

### 更新依赖

```bash
uv sync --upgrade
```

### 查看已安装的包

```bash
uv pip list
```

### 激活虚拟环境

虽然 uv 推荐使用 `uv run` 来运行命令，但也可以激活虚拟环境：

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**注意：** 如果之前使用了其他虚拟环境管理工具（如 pipenv），请先退出旧环境：
```powershell
deactivate  # 退出旧环境
# 然后使用 uv sync --dev 创建新环境
```

## 故障排除

### 问题：无法安装某些包

1. 检查网络连接
2. 确认特殊索引源配置正确
3. 尝试使用 `--index-url` 参数指定索引

### 问题：Python 版本不匹配

项目要求 Python 3.10+。检查 Python 版本：

```bash
uv python list
```

安装特定版本：

```bash
uv python install 3.10
```

### 问题：依赖冲突

清理并重新同步：

```bash
rm -rf .venv uv.lock
uv sync --dev
```

### 问题：uwsgi 安装失败（Windows）

`uwsgi` 是一个仅支持 Linux/Unix 的 WSGI 服务器，在 Windows 上无法安装。这是正常的：

- **开发环境**：Windows 开发环境不需要 `uwsgi`，使用 Django 自带的开发服务器即可
- **生产环境**：如果需要在 Linux/Unix 生产环境部署，可以安装生产依赖：
  ```bash
  uv sync --extra production
  ```

注意：`uwsgi` 已从主要依赖中移除，仅在 `production` 可选依赖中提供。

## 从 Pipfile 迁移

项目已从 Pipfile 迁移到 pyproject.toml。如果之前使用 pipenv：

1. 删除旧的虚拟环境（如果存在）
2. 运行 `uv sync --dev` 创建新环境
3. 所有依赖会自动从 `pyproject.toml` 安装

## 更多信息

- [uv 官方文档](https://docs.astral.sh/uv/)
- [uv GitHub 仓库](https://github.com/astral-sh/uv)

