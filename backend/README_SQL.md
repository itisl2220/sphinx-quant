# 数据库初始化说明

## 使用 SQL 文件初始化数据库

### 步骤 1: 创建数据库

```sql
-- 连接到 PostgreSQL
CREATE DATABASE sphinxquant;
CREATE USER sphinxquant WITH PASSWORD 'sphinxquant';
GRANT ALL PRIVILEGES ON DATABASE sphinxquant TO sphinxquant;
```

### 步骤 2: 执行 SQL 文件

**方法 1: 使用 psql 命令行**

```bash
psql -U sphinxquant -d sphinxquant -f init_db.sql
```

**方法 2: 在 PostgreSQL 客户端中执行**

1. 打开 pgAdmin 或其他 PostgreSQL 客户端
2. 连接到数据库
3. 打开 `init_db.sql` 文件
4. 执行整个脚本

**方法 3: 使用 PowerShell**

```powershell
# 如果 PostgreSQL 在本地
psql -U sphinxquant -d sphinxquant -f backend\init_db.sql
```

### 步骤 3: 验证表是否创建成功

```sql
-- 连接到数据库后执行
\dt

-- 或者
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

应该看到以下表：
- users
- source_codes
- strategies
- backtests

### 表结构说明

1. **users** - 用户表
   - 存储用户信息和认证数据

2. **source_codes** - 策略代码表
   - 存储策略的源代码

3. **strategies** - 策略表
   - 存储策略信息
   - 外键关联到 source_codes

4. **backtests** - 回测表
   - 存储回测结果
   - 外键关联到 strategies 和 source_codes

### 注意事项

1. SQL 文件会自动创建 UUID 扩展
2. 所有表都有 `created_at` 和 `updated_at` 字段，会自动维护
3. 外键约束设置为 CASCADE 删除，删除策略时会自动删除相关回测
4. 已创建必要的索引以提高查询性能

### 创建初始管理员用户

如果需要创建初始管理员用户，可以使用以下 Python 脚本：

```python
from app.core.security import get_password_hash
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

admin_user = User(
    username="admin",
    email="admin@sphinxquant.com",
    hashed_password=get_password_hash("admin123"),  # 请修改密码
    is_active=True,
    is_superuser=True,
    first_name="Admin",
    last_name="User"
)

db.add(admin_user)
db.commit()
db.close()
```

