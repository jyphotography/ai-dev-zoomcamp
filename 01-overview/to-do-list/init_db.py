#!/usr/bin/env python
"""
Django 数据库初始化脚本
用于创建初始数据库文件和表结构
"""

import os
import sys
import subprocess

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {description}失败")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """主函数"""
    print("🚀 开始初始化 Django 数据库...\n")
    
    # 检查是否在正确的目录
    if not os.path.exists("manage.py"):
        print("❌ 错误: 请在包含 manage.py 的项目根目录运行此脚本")
        sys.exit(1)
    
    # 检查 Django 是否已安装
    try:
        import django
    except ImportError:
        print("❌ 错误: Django 未安装，请先运行: pip install django")
        sys.exit(1)
    
    # 步骤 1: 创建迁移文件
    if not run_command("python manage.py makemigrations", "创建迁移文件"):
        sys.exit(1)
    
    print()
    
    # 步骤 2: 应用迁移
    if not run_command("python manage.py migrate", "应用迁移到数据库"):
        sys.exit(1)
    
    print("\n✅ 数据库初始化完成！")
    print("\n📝 下一步：")
    print("   - 运行 'python manage.py createsuperuser' 创建管理员账户（可选）")
    print("   - 运行 'python manage.py runserver' 启动开发服务器")
    print()

if __name__ == "__main__":
    main()

