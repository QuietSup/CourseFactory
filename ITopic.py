import mysql.connector
import json
from abc import ABC, abstractmethod


class ITopic(ABC):
    """Is used to add topics to the database"""
    @abstractmethod
    def save(self): pass
    """Save entered data about topic to the database"""

    @property
    @abstractmethod
    def title(self): pass

    @title.setter
    @abstractmethod
    def title(self, value): pass


class Topic(ITopic):
    def __init__(self, title: str):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password']
        )
        self.title = title

        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('CREATE DATABASE IF NOT EXISTS `CourseFactory`')
        mycursor.close()

        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password'],
            database='CourseFactory'
        )
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('CREATE TABLE IF NOT EXISTS `topics` ('
                         'id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, '
                         'title VARCHAR(50))')
        self.mydb.commit()
        mycursor.close()

    def __repr__(self):
        return f'\nTopic title: {self.title}'

    def save(self):
        mycursor = self.mydb.cursor(buffered=True)
        func = 'SELECT `title` FROM `topics` WHERE title=%s'
        mycursor.execute(func, (self.title,))
        if mycursor.fetchone() is not None:
            raise ValueError('Topic already exists')
        func = 'INSERT INTO `topics` (title) VALUES (%s)'
        mycursor.execute(func, (self.title,))
        self.mydb.commit()
        mycursor.close()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError('Title must be str type')
        self.__title = value
