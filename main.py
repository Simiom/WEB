from db import DB
from users_model import UsersModel

db = DB()
UsersModel(db.get_connection()).init_table()
um = UsersModel(db.get_connection())
um.insert("admin", "admin")