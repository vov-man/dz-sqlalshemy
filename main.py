import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from privat.config import dsn
from models import create_tables, Publisher, Shop, Book, Stock, Sale 
DSN = dsn
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('/home/vladimir/учеба/dz sqlalchemi/base.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


session.close()