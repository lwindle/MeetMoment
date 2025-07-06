#!/usr/bin/env python3
import bcrypt

# 生成密码 "123456" 的bcrypt哈希
password = "123456"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"Password: {password}")
print(f"Bcrypt hash: {hashed.decode('utf-8')}") 