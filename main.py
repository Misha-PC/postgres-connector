from connector import Database
from connector import Users


if __name__ == "__main__":
    db = Database(dbname='parsers', user='postgres', password='111111', host='localhost')
    user = Users( db.get_connection() )
    c = user.select(("id", 1))
    print(c)


