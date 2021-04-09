from sql_alch.app import db, User

db.create_all()

u1 = User(username = 'vasya1', email = 'vvv@gg.com')
db.session.add(u1)
db.session.commit()