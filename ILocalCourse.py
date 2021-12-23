import mysql.connector
from ICourse import Course
import json
from abc import ABC, abstractmethod


class ILocalCourse(ABC):
    """Headquarters courses"""
    @abstractmethod
    def save(self):
        """Saves all planned changes"""
        pass


class LocalCourse(Course, ILocalCourse):
    def __init__(self, title: str, first_name: str, last_name: str,
                 topic: list[str], street: str, building: int):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password'],
            database='CourseFactory'
        )
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
        topic_id = []
        for item in topic:
            func = 'SELECT id FROM `topics` ' \
                   'WHERE title=%s'
            mycursor.execute(func, (item,))
            value = mycursor.fetchone()
            if value is None:
                raise ValueError('Topic doesn\'t exist')
            topic_id.append(value[0])

        func = 'SELECT id FROM `teachers` ' \
               'WHERE first_name=%s and last_name=%s'
        mycursor.execute(func, (first_name, last_name))
        value = mycursor.fetchone()
        if value is None:
            raise ValueError('Teacher doesn\'t exist')
        teacher_id = value[0]

        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)

        func = 'SELECT id FROM `locations`' \
               'WHERE country=%s and city=%s and street=%s and building=%s'
        mycursor.execute(func, (data['local_country'], data['local_city'],
                                street, building))
        value = mycursor.fetchone()
        if value is None:
            raise ValueError('Location doesn\'t exist')

        super().__init__(title, teacher_id, topic_id, value[0])
