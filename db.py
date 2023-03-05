import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()
        self.creat = """
                CREATE TABLE IF NOT EXISTS all_dizainiri(
                Name STR,
                Citi STR,
                Telefon STR,
                Url social STR,
                Portfolios STR
                )
                    """
        self.cur.execute(self.creat)
        self.connection.commit()


    def add_user(self, row):
        with self.connection:
            self.cur.execute("""SELECT COUNT (*) FROM all_dizainiri WHERE Name = ?""", (row[0],))
            if int(self.cur.fetchone()[0]) == 0:
                self.cur.execute("""INSERT INTO all_dizainiri VALUES (?,?,?,?,?)""", row)

    async def search_citi(self, text):
        with self.connection:
            name = []
            tel = []
            portfol = []
            result = self.cur.execute("""SELECT Name, Telefon, Portfolios  FROM all_dizainiri WHERE Citi LIKE ?""", (text,)).fetchall()
            all_page = len(result)
            for iten in range(0, len(result)):
                #print(result[iten][0])
                name.append(result[iten][0])
                tel.append(result[iten][1])
                portfol.append(result[iten][2])
            data = {'Имя': name,
                        'Телефон': tel,
                        'Порфолио': portfol}

        return data, all_page

#db = Database('dizainiri.db')
#db.search_citi('%Москва')
