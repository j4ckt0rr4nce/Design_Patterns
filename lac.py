import sqlite3
import json
import datetime

file_path = "data.ndjson"

class Product:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        print("Connected to SQLite")
        

    def create_table(self, file_path):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id INT NOT NULL,
                                    name VARCHAR(50) NOT NULL,
                                    city VARCHAR(50) NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ordered_products(
                                    id INT NOT NULL,
                                    name VARCHAR(50) NOT NULL,
                                    price VARCHAR(50) NOT NULL,
                                    user_id INT NOT NULL,
                                    order_id INT NOT NULL,
                                    FOREIGN KEY(user_id) REFERENCES users(id),
                                    FOREIGN KEY(order_id) REFERENCES orders(id))""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS orders(
                                    id INT NOT NULL,
                                    created DATETIME NOT NULL, 
                                    user_id INT NOT NULL,
                                    FOREIGN KEY(user_id) REFERENCES users(id))""")
        records = map(json.loads, open(file_path, encoding="utf8"))
        for r in records:
            date = datetime.datetime.now()-datetime.timedelta(seconds=r.get('created'))
            self.cur.execute("""INSERT INTO users(
                                    id,
                                    name,
                                    city
                            ) VALUES(?, ?, ?);""", (r.get('user')['id'], r.get('user')['name'], r.get('user')['city']))
            self.cur.execute("""INSERT INTO orders(
                                    id,
                                    created,
                                    user_id
                            ) VALUES(?, ?, ?);""", (r.get('id'), date.date(), r.get('user')['id']))
            for p in r.get('products'):
                self.cur.execute("""INSERT INTO ordered_products(
                                    id,
                                    name,
                                    price,
                                    user_id,
                                    order_id
                            ) VALUES(?, ?, ?, ?, ?);""", (p['id'], p['name'], p['price'], r.get('user')['id'], r.get('id')))     
        self.conn.commit()
        self.conn.close()
        print("The Sqlite connection is closed")


    def get_orders(self, start_date, end_date):
        if start_date >= end_date:
            raise Exception("First argument must be bigger than second argument")
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD string")
        try:
            self.cur.execute("SELECT * FROM orders WHERE created BETWEEN (?) AND (?) ORDER BY created", (start_date, end_date))
            records = self.cur.fetchall()
            for r in records:
                print("id: ", r[0])
                print("created: ", r[1])
                print("user_id: ", r[2])
                print("\n")
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if self.conn:
                self.conn.close()
                print("The Sqlite connection is closed")


    def get_users(self, user_num):
        try:
            self.cur.execute('''SELECT user_id, count(user_id) 
                                FROM ordered_products 
                                GROUP by user_id
                                ORDER BY count(user_id) DESC''')
            records = self.cur.fetchall()
            for r in records[:user_num]:
                print(f"user ID {r[0]}: number of ordered products {r[1]}")
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if self.conn:
                self.conn.close()
                print("The Sqlite connection is closed")


if __name__ == '__main__':
    p = Product()
    #p.create_table(file_path)
    #p.get_orders('1973-07-07','1973-07-09')
    p.get_users(5)