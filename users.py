from abc import ABC, abstractmethod
import sqlite3


class Users(ABC):
    @abstractmethod
    def users_query(self) -> None:
        """Method to run concrete users query from database"""


class ConcreteUsers(Users):
    def users_query(self, user_num: int) -> str:
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""SELECT user_id, count(user_id)
                                FROM ordered_products
                                GROUP by user_id
                                ORDER BY count(user_id) DESC""")
            records = self.cur.fetchall()
            if len(records)+1 <= user_num:
                raise Exception("Entered number exceeded the number of users")
            for r in records[:user_num]:
                print(f"user ID {r[0]}: number of ordered products {r[1]}")
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if self.conn:
                self.conn.close()