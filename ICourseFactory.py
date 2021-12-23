import mysql.connector
from abc import ABC, abstractmethod
import json

from ILocation import Location
from ITeacher import Teacher
from ITopic import Topic
from ILocalCourse import LocalCourse
from IOffsiteCourse import OffsiteCourse
from IJsonFill import JsonFill


class ICourseFactory(ABC):
    """General class to operate with all the data including creating and deleting data"""
    @staticmethod
    @abstractmethod
    def new_local(title: str, first_name: str, last_name: str,
                  topic: list[str], street: str, building: int):
        """Creates new local course in the database"""
        pass

    @staticmethod
    @abstractmethod
    def new_offsite(title: str, first_name: str, last_name: str, topic: list[str],
                    country: str, city: str, street: str, building: int):
        """Creates new offsite course in the database"""
        pass

    @property
    @abstractmethod
    def locals(self):
        """Returns all the local courses"""
        pass

    @property
    @abstractmethod
    def offsites(self):
        """Returns all the offsite courses"""
        pass

    @staticmethod
    @abstractmethod
    def new_teacher(first_name: str, last_name: str):
        """Creates teacher field in the database"""
        pass

    @staticmethod
    @abstractmethod
    def new_topic(title: str):
        """Creates new topic"""
        pass

    @abstractmethod
    def del_course(self, title: str):
        """Deletes the course"""
        pass

    @abstractmethod
    def find_teacher(self, first_name: str, last_name: str):
        """Find the teacher by name"""
        pass

    @abstractmethod
    def __getitem__(self, title: str):
        """find a course by a title. Overloaded operator []"""
        pass

    @abstractmethod
    def __iter__(self):
        """Is used for iterator"""
        pass

    @abstractmethod
    def __next__(self):
        """is used to iterate through all courses"""
        pass

    @staticmethod
    @abstractmethod
    def new_headquarters(country, city):
        """Change headquarters country and city"""
        pass

    @staticmethod
    @abstractmethod
    def secure_db(host, user, password):
        """Change host, user and password to access to database"""
        pass


class CourseFactory(ICourseFactory):
    def __init__(self):
        data = {}
        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)
        self.mydb = mysql.connector.connect(
            host=data['host'],
            user=data['user'],
            password=data['password']
        )

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
        self.index = 0

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
        new.save()

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

    def __getitem__(self, title: str):
        func = "SELECT co.title, first_name, last_name, " \
               "country, city, street, building, " \
               "top.title " \
               "FROM `courses` co, `teachers` te, `locations` lo, `topics` top " \
               "WHERE teacher_id=te.id and location_id=lo.id and top.id=co.topic_id " \
               "and co.title=%s"
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func, (title,))
        self.mydb.commit()
        result = mycursor.fetchall()
        mycursor.close()
        return result

    def __iter__(self):
        func = 'SELECT title FROM `courses`'
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute(func)
        self.courses = list(set([x[0] for x in mycursor.fetchall()]))
        return self

    def __next__(self):
        if self.index >= len(self.courses) - 1:
            raise StopIteration()
        self.index += 1
        return self[self.courses[self.index]]

    @staticmethod
    def new_headquarters(country, city):
        secure = JsonFill(None, None, None, country, city)
        info = secure.get_info
        secure = JsonFill(info['host'], info['user'], info['password'], country, city)
        secure.save()

    @staticmethod
    def secure_db(host, user, password):
        secure = JsonFill(host, user, password, None, None)
        info = secure.get_info
        secure = JsonFill(host, user, password, info['local_country'], info['local_city'])
        secure.save()


if __name__ == '__main__':
    obj = CourseFactory()
    # obj.new_local('Django', 'George', 'Kim', ['Math'], 'Akademika', 12)
    # obj.new_location('US', 'LA', 'Hetmana', 29)
    # obj.new_topic('Inheritance')
    # obj.new_topic('Encapsulation')
    # obj.new_teacher('Kim', 'Taehyung')
    # obj.new_teacher('Pak', 'Jimin')
    # obj.new_offsite('OOP', 'Kim', 'Taehyung', ['Inheritance', 'Encapsulation'],
    #                 'US', 'LA', 'Hetmana', 29)
    # print(obj.locals)
    # print(obj.offsites)
    # print(obj['OOP'])
    # for i in obj:
    #     print(i)
    # obj.new_headquarters('US', 'LA')
    # obj.secure_db('avd', 'saas', 'fad')
