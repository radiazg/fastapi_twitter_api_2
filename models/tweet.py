from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime
from config.db import meta, engine

tweets = Table("tweets", meta,
    Column("tweet_id", String(255), primary_key=True),
    Column("content", String(255)),
    Column("created_at", DateTime()),
    Column("updated_at", DateTime()),
    Column("user_by", String(255)))

meta.create_all(engine)