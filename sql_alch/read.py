from sql_alch.app import  User

res = User.query.all()

for item in res:
    print(item)