import mysql.connector
from abc import ABC, abstractmethod
import json

from ILocation import Location
from ITeacher import Teacher
from ITopic import Topic
from ILocalCourse import LocalCourse
from IOffsiteCourse import OffsiteCourse


class CourseFactory:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='vfrc15403'
        )
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('CREATE DATABASE IF NOT EXISTS `CourseFactory`')
        mycursor.close()

    @staticmethod
    def new_local(title: str, first_name: str, last_name: str,
                  topic: list[str], street: str, building: int):
        new = LocalCourse(title, first_name, last_name,
                          topic, street, building)
        new.save()

    @staticmethod
    def new_offsite(title: str, first_name: str, last_name: str, topic: list[str],
                    country: str, city: str, street: str, building: int):
        new = OffsiteCourse(title, first_name, last_name,
                            topic, country, city, street, building)
        new.save()

    @property
    def locals(self):
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)

        func = 'SELECT title FROM `courses` c ' \
               'JOIN `locations` l ON c.location_id=l.id ' \
               'WHERE country=%s and city=%s'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (data['local_country'], data['local_city']))
        result = mycursor.fetchall()
        mycursor.close()
        return result

    @property
    def offsites(self):
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)

        func = 'SELECT `title` FROM `courses` co ' \
               'WHERE NOT EXISTS ' \
               '(SELECT title FROM `courses` c ' \
               'JOIN `locations` l ON c.location_id=l.id ' \
               'WHERE country=%s and city=%s)'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (data['local_country'], data['local_city']))
        result = mycursor.fetchall()
        mycursor.close()
        return result

    @staticmethod
    def new_teacher(first_name: str, last_name: str):
        new = Teacher(first_name, last_name)
        new.save()

    @staticmethod
    def new_topic(title: str):
        new = Topic(title)
        new.title()

    @staticmethod
    def new_location(country: str, city: str, street: str, building: int):
        new = Location(country, city, street, building)
        new.save()

    def del_course(self, title: str):
        if not isinstance(title, str):
            raise TypeError('title must be str type')
        func = 'DELETE FROM `courses` ' \
               'WHERE title=%s'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (title,))
        self.mydb.commit()
        mycursor.close()

    def find_teacher(self, first_name: str, last_name: str):
        func = 'SELECT first_name, last_name, title ' \
               'FROM `teachers` t, `courses` c ' \
               'WHERE t.id = c.teacher_id and first_name=%s and last_name=%s'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (first_name, last_name))
        self.mydb.commit()
        result = mycursor.fetchall()
        mycursor.close()
        return result

    def find_course(self, title: str):
        func = 'SELECT co.title, CONCAT(first_name, '', last_name) AS teacher, ' \
               'CONCAT(country, city, street, building) AS adress, ' \
               'top.title ' \
               'FROM `courses` co, `teachers` te, `locations` lo, `topics` top ' \
               'WHERE teacher_id=te.id and location_id=lo.id and top.id=co.topic_id ' \
               'and co.title=%s'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (title,))
        self.mydb.commit()
        result = mycursor.fetchall()
        mycursor.close()
        return result
