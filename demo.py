from application.functions import *
from application.schemes import *

#create_user('ADMIN', 'admin_1', 12345678)
user = get_user_username("admin_1")
#print(get_user_name("ADMIN"))
print(get_all_users_v2())
print(User(*user))