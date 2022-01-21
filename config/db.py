from sqlalchemy import create_engine, MetaData

# create the engine string connection
engine = create_engine("mysql+pymysql://root:secret@localhost:33060/twitterdb")

# Create the metadata
meta = MetaData()

# create the connection
conn = engine.connect()