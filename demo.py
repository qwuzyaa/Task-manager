from application.functions import *
import bcrypt

# Хеширование пароля
password = get_pass('admin_1')
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print(hashed)
print("Хеш пароля:", hashed.decode())

# Проверка пароля
input_password = get_pass('admin_1')
if bcrypt.checkpw(input_password.encode(), hashed):
    print("Пароль верный", input_password.encode())
else:
    print("Пароль неверный")

