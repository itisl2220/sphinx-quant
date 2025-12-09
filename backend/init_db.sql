-- Sphinx Quant 数据库初始化脚本
-- PostgreSQL 数据库表结构

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建 users 表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建 users 表索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 创建 source_codes 表
CREATE TABLE IF NOT EXISTS source_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code_text TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建 strategies 表
CREATE TABLE IF NOT EXISTS strategies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(127) NOT NULL,
    source_code_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_strategies_source_code FOREIGN KEY (source_code_id) 
        REFERENCES source_codes(id) ON DELETE CASCADE
);

-- 创建 strategies 表索引
CREATE INDEX IF NOT EXISTS idx_strategies_name ON strategies(name);
CREATE INDEX IF NOT EXISTS idx_strategies_source_code_id ON strategies(source_code_id);

-- 创建 backtests 表
CREATE TABLE IF NOT EXISTS backtests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(127) NOT NULL,
    bar_type VARCHAR(127) NOT NULL,
    logs TEXT,
    total_profit_percent DOUBLE PRECISION,
    year_profit_percent DOUBLE PRECISION,
    max_dropdown_percent DOUBLE PRECISION,
    strategy_id UUID NOT NULL,
    source_code_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_backtests_strategy FOREIGN KEY (strategy_id) 
        REFERENCES strategies(id) ON DELETE CASCADE,
    CONSTRAINT fk_backtests_source_code FOREIGN KEY (source_code_id) 
        REFERENCES source_codes(id) ON DELETE CASCADE
);

-- 创建 backtests 表索引
CREATE INDEX IF NOT EXISTS idx_backtests_name ON backtests(name);
CREATE INDEX IF NOT EXISTS idx_backtests_strategy_id ON backtests(strategy_id);
CREATE INDEX IF NOT EXISTS idx_backtests_source_code_id ON backtests(source_code_id);
CREATE INDEX IF NOT EXISTS idx_backtests_status ON backtests(status);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表创建更新时间触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_source_codes_updated_at BEFORE UPDATE ON source_codes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_strategies_updated_at BEFORE UPDATE ON strategies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_backtests_updated_at BEFORE UPDATE ON backtests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入默认管理员用户（密码: admin123，实际使用时请修改）
-- 注意：这是示例，实际密码应该使用 bcrypt 加密
-- INSERT INTO users (id, username, email, hashed_password, is_active, is_superuser, first_name, last_name)
-- VALUES (
--     uuid_generate_v4(),
--     'admin',
--     'admin@sphinxquant.com',
--     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqBqJqZ5Xm',  -- 需要替换为实际的 bcrypt 哈希
--     TRUE,
--     TRUE,
--     'Admin',
--     'User'
-- );

