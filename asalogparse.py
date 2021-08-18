import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///sqlite3.db') # using relative path
engine.connect()
print(engine)

""" 
CREATE TABLE asalogs(connid INTEGER PRIMARY KEY, startdate TEXT NOT NULL, protocol TEXT NOT NULL,
                         ifclient TEXT NOT NULL, ipclient TEXT NOT NULL, portclient INTEGER,
                         ifserver TEXT NOT NULL, ipserver TEXT NOT NULL, portserver INTEGER,
                         duration INTEGER, bytes INTEGER, closeflag TEXT);
"""

blog = Table('asalogs', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('post_title', String(200), nullable=False),
    Column('post_slug', String(200),  nullable=False),
    Column('content', Text(),  nullable=False),
    Column('published', Boolean(),  default=False),
    Column('startdate', DateTime(), default=datetime.now),
    Column('enddate', DateTime(), default=datetime.now)
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)



