# from django.db import connection



# def db_table_exists(table_name):
#     return table_name in connection.introspection.table_names()


# def create_user():
# 	if db_table_exists('core_member'):
# 		from core.models import Member
# 		users_list = Member.objects.all().exists()
# 		if not users_list :
# 			user = Member.objects.create_superuser('admin@promedic.com.ng', '1password1') 
# 			user.first_name = 'Su'
# 			user.last_name = 'Admin'
# 			user.user_type= 'SU'
# 			user.save()
# 			print 'created user...'



