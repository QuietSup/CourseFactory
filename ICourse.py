import mysql.connector
import json
from abc import ABC, abstractmethod


class ICourse(ABC):
    """Class is used to get info about courses and save it to the database"""
    @abstractmethod
    def save(self): 
        """Saves all planned changes"""
        pass

    @property
    @abstractmethod
    def title(self): pass

    @property
    @abstractmethod
    def teacher_id(self): pass

    @property
    @abstractmethod
    def topic_id(self): pass

    @property
    @abstractmethod
    def location_id(self): pass

    @title.setter
    @abstractmethod
    def title(self, value): pass

    @teacher_id.setter
    @abstractmethod
    def teacher_id(self, value): pass

    @topic_id.setter
    @abstractmethod
    def topic_id(self, value): pass

    @location_id.setter
    @abstractmethod
    def location_id(self, value): pass


class Course(ICourse):
    def __init__(self, title: str, teacher_id: int, topic_id: list[int], location_id: int):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password']
        )
        self.title = title
        self.teacher_id = teacher_id
        self.topic_id = topic_id
        self.location_id = location_id

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
        mycursor.execute('CREATE TABLE IF NOT EXISTS `courses` ('
                         'title VARCHAR(50),'
                         'teacher_id INT UNSIGNED,'
                         'topic_id INT UNSIGNED,'
                         'location_id INT UNSIGNED,'
                         'FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE ON UPDATE CASCADE,'
                         'FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE ON UPDATE CASCADE,'
                         'FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE ON UPDATE CASCADE)')
        self.mydb.commit()
        mycursor.close()

    def __repr__(self):
        return f'\nCourse title: {self.title}'

    def save(self):
        mycursor = self.mydb.cursor(buffered=True)
        func = 'SELECT `title` FROM `courses` WHERE title=%s'
        mycursor.execute(func, (self.title,))
        if mycursor.fetchone() is not None:
            raise ValueError(f'Title already exists')

        for item in self.topic_id:
            func = 'INSERT INTO `courses` (title, teacher_id, topic_id, location_id) ' \
                   'VALUES (%s, %s, %s, %s)'
            mycursor.execute(func, (self.title, self.teacher_id, item, self.location_id))
            self.mydb.commit()

        mycursor.close()

    @property
    def title(self):
        return self.__title

    @property
    def teacher_id(self):
        return self.__teacher_id

    @property
    def topic_id(self):
        return self.__topic_id

    @property
    def location_id(self):
        return self.__location_id

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError('Title must be str type')
        self.__title = value

    @teacher_id.setter
    def teacher_id(self, value):
        if not isinstance(value, int):
            raise TypeError('teacher_id must be int type')
        if value < 0:
            raise ValueError('id can\'t be negative')
        self.__teacher_id = value

    @topic_id.setter
    def topic_id(self, value):
        if not isinstance(value, list):
            raise TypeError('topic_id must be list type')
        for item in value:
            if item < 0:
                raise ValueError('id can\'t be negative')
        self.__topic_id = value

    @location_id.setter
    def location_id(self, value):
        if not isinstance(value, int):
            raise TypeError('location_id must be int type')
        if value < 0:
            raise ValueError('id can\'t be negative')
        self.__location_id = value
