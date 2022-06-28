import psycopg2
from datetime import datetime
class PostgresApi:
    # parametrized constructor and is assigned values once the object is created (instance initialize)
    def __init__(self, user, password, host, port, dbname):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        # object connect function is also called here whose body is defined below
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                dbname = self.dbname
            )
            # open a cursor  to perform database operations
            # cursor should have conection open to perform CRUD queries
            self.cursor = self.connection.cursor()
            print(
                '------------------------------------------------------------'
                '\n-# PostgreSQL connection & transaction is ACTIVE\n'
                )
            print(self.cursor)
        except (Exception, psycopg2.Error) as error :
            print(error, error.pgcode, error.pgerror, sep = '\n')
            #sys.exit()
        # else:
        #     self.connection = connection
        #     self.cursor = cursor

    def all(self,table):
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        print(f"Rows of Table:{table}")
        for row in rows:
            print(f"{row}\n")
        return rows

    def close(self):
        self.cursor.close()
        self.connection.close()

    def create(self, title, content):
        time=str(datetime.now())
        author_id=2
        self. cursor.execute(f" INSERT INTO post_post (title, content, created_date, author_id) values (%s, %s, %s, %s)", (title,content,time,author_id))
        self.connection.commit()

class BlogApi:
    def populate(self):
        db = PostgresApi(user='postgres',password='admin', host="localhost", port=5432, dbname='blog_db')
        titles=['Travelling','Health','Fitness','Nutrition', 'Hiking', 'Long Drive', 'Camping','Sightseeing']
        content='Travelling is good'
        for i in range(50):
            for title in titles:
                db.create(title,content)
        db.close()