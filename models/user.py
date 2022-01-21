from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Date
from config.db import meta, engine

users = Table("users", meta,
    Column("user_id", String(255), primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("birth_date", Date()))

meta.create_all(engine)
