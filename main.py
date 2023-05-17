import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from privat.config import dsn
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = dsn
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)

with open('base.json', 'r') as fd:
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




def publisher_search(search_query):
    if search_query.isdigit():
        for books in session.query(Book.title, Publisher.name, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(
            Stock).join(Sale).join(Shop).filter(Publisher.id == search_query).all():
            print(' '.join(str(book) for book in books))
    else:
        for books in session.query(Book.title, Publisher.name, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(
            Stock).join(Sale).join(Shop).filter(Publisher.name.like(search_query)).all():
            print(' '.join(str(book) for book in books))
if __name__ == '__main__':
    search_query = input("для поиска необходимо ввести имя или айди публициста: ") #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    publisher_search(search_query) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше    







session.close()