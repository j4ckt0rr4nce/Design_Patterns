from abc import ABC, abstractmethod
import sqlite3


class Products(ABC):
    @abstractmethod
    def products_query(self):
        """Method to run concrete products query from database"""

class ConcreteProducts(Products):
    def products_query(self):
        pass