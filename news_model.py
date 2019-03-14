class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 title VARCHAR(100),
                                 image BINARY(10000000),
                                 content VARCHAR(1000),
                                 user_id VARCHAR(50),
                                 rating INTEGER
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, file, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, image, content, user_id, rating) 
                          VALUES (?,?,?,?,?)''', (title, file, content, str(user_id), 0))
        cursor.close()
        self.connection.commit()

    def update_rating(self, news_id, val):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE news SET rating = (?) WHERE id = (?)''', (str(self.get_rating(news_id)[0] + val), str(news_id)))

    def get_rating(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT rating FROM news WHERE id = ?", (str(news_id),))
        rating = cursor.fetchone()
        return rating

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?", (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()