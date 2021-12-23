import mysql.connector
import json
from abc import ABC, abstractmethod


class ITeacher(ABC):
    """Is used to add teachers the the database"""
    @abstractmethod
    def save(self): 
        """Saves information about a teacher to the database"""
        pass

    @property
    @abstractmethod
    def first_name(self): pass

    @property
    @abstractmethod
    def last_name(self): pass

    @first_name.setter
    @abstractmethod
    def first_name(self, value): pass

    @last_name.setter
    @abstractmethod
    def last_name(self, value): pass


class Teacher:
    def __init__(self, first_name: str, last_name: str):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password']
        )
        self.first_name = first_name
        self.last_name = last_name

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
        mycursor.execute('CREATE TABLE IF NOT EXISTS `Teachers` ('
                         'id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, '
                         'first_name VARCHAR(15), '
                         'last_name VARCHAR(15));')
        self.mydb.commit()
        mycursor.close()

    def __repr__(self):
        return f'\nName: {self.first_name} {self.last_name}'

    def save(self):
        mycursor = self.mydb.cursor(buffered=True)
        func = 'SELECT `first_name`, `last_name` FROM `teachers` WHERE first_name=%s AND last_name=%s'
        mycursor.execute(func, (self.first_name, self.last_name))
        if mycursor.fetchone() is not None:
            raise ValueError('Teacher already exists')
        func = 'INSERT INTO `teachers` (first_name, last_name) VALUES (%s, %s)'
        mycursor.execute(func, (self.first_name, self.last_name))
        self.mydb.commit()
        mycursor.close()

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('First name must be str type')
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Last name must be str type')
        self.__last_name = value
