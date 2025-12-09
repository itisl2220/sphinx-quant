"""
创建管理员用户的脚本
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User


def create_admin_user(username: str = "admin", password: str = "admin123", email: str = "admin@sphinxquant.com"):
    """创建管理员用户"""
    db: Session = SessionLocal()
    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"用户 '{username}' 已存在，正在更新密码...")
            existing_user.hashed_password = get_password_hash(password)
            existing_user.email = email
            existing_user.is_active = True
            existing_user.is_superuser = True
            db.commit()
            print(f"[OK] 用户 '{username}' 的密码已更新")
            return existing_user
        
        # 创建新用户
        admin_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True,
            first_name="Admin",
            last_name="User"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"[OK] 管理员用户 '{username}' 创建成功")
        print(f"  用户名: {username}")
        print(f"  密码: {password}")
        print(f"  邮箱: {email}")
        return admin_user
    except Exception as e:
        db.rollback()
        print(f"[ERROR] 创建用户失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # 可以从命令行参数获取用户名和密码
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin123"
    email = sys.argv[3] if len(sys.argv) > 3 else "admin@sphinxquant.com"
    
    print("正在创建管理员用户...")
    create_admin_user(username, password, email)

