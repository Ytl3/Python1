import random
class Book:
    def __init__(self,name, desc, writers,booknbr, rembks):
        self.id = "BK" + str(random.randint(10009000, 9111111119999))
        self.name = name
        self.desc = desc
        self.writers = writers
        self.booknbr = booknbr
        self.rembks = rembks

    def __str__(self):
        return f"{self.name} ({self.rembks}/{self.booknbr} disponibles)"


class Author:
    def __init__(self, name, books=None):
        self.id = "AU" + str(random.randint(100000999, 999903432992873))
        self.name = name
        self.books = books if books else []

    def __str__(self):
        return f"{self.name}"


class Student:
    def __init__(self, name, password,books=None):
        self.id = "ST" + str(random.randint(125500000, 999999345999))
        self.name = name
        self.password = password
        self.books =books if books else []

    def can_borrow(self):
        return len(self.books) < 3


class Admin:
    def __init__(self, name, email, password):
        self.id = "AD" + str(random.randint(12000000, 999999999888))
        self.name = name
        self.email = email
        self.password = password
