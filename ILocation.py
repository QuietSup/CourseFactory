import mysql.connector
import json
from abc import ABC, abstractmethod


class ILocation(ABC):
    """Is used to add locations the the database"""
    @abstractmethod
    def save(self): pass
    """Saves information about locations to the database"""

    @property
    @abstractmethod
    def country(self): pass

    @property
    @abstractmethod
    def city(self): pass

    @property
    @abstractmethod
    def street(self): pass

    @property
    @abstractmethod
    def building(self): pass

    @country.setter
    @abstractmethod
    def country(self, value): pass

    @city.setter
    @abstractmethod
    def city(self, value): pass

    @street.setter
    @abstractmethod
    def street(self, value): pass

    @building.setter
    @abstractmethod
    def building(self, value): pass


class Location(ILocation):
    def __init__(self, country: str, city: str, street: str, building: int):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password']
        )
        self.country = country
        self.city = city
        self.street = street
        self.building = building

        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('CREATE DATABASE IF NOT EXISTS `CourseFactory`')
        mycursor.close()

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='vfrc15403',
            database='CourseFactory'
        )
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(f'CREATE TABLE IF NOT EXISTS `locations` ('
                         'id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, '
                         'country VARCHAR(15), '
                         'city VARCHAR(15), '
                         'street VARCHAR(30), '
                         'building INT)')
        self.mydb.commit()
        mycursor.close()

    def __repr__(self):
        return f'\nLocation: {self.country}, {self.city}, {self.street} {self.building}'

    def save(self):
        mycursor = self.mydb.cursor(buffered=True)
        func = f'SELECT country, city, street, building FROM `locations` ' \
               'WHERE country=%s AND city=%s AND street=%s AND building=%s'
        mycursor.execute(func, (self.country, self.city, self.street, self.building))
        if mycursor.fetchone() is not None:
            raise ValueError('Location already exists')
        func = f'INSERT INTO `locations` (country, city, street, building) VALUES (%s, %s, %s, %s)'
        mycursor.execute(func, (self.country, self.city, self.street, self.building))
        self.mydb.commit()
        mycursor.close()

    @property
    def country(self):
        return self.__country

    @property
    def city(self):
        return self.__city

    @property
    def street(self):
        return self.__street

    @property
    def building(self):
        return self.__building

    @country.setter
    def country(self, value):
        if not isinstance(value, str):
            raise TypeError('Country must be str type')
        self.__country = value

    @city.setter
    def city(self, value):
        if not isinstance(value, str):
            raise TypeError('City must be str type')
        self.__city = value

    @street.setter
    def street(self, value):
        if not isinstance(value, str):
            raise TypeError('Street must be str type')
        self.__street = value

    @building.setter
    def building(self, value):
        if not isinstance(value, int):
            raise TypeError('Building must be int type')
        self.__building = value
