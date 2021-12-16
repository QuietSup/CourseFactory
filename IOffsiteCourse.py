import mysql.connector
from ICourse import Course
import json


class OffsiteCourse(Course):
    def __init__(self, title: str, first_name: str, last_name: str, topic: list[str],
                 country: str, city: str, street: str, building: int):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='vfrc15403',
            database='CourseFactory'
        )
        mycursor = self.mydb.cursor(buffered=True)
        topic_id = []
        for item in topic:
            func = 'SELECT id FROM `topics` ' \
                   'WHERE title=%s'
            mycursor.execute(func, (item,))
            topic_id.append(mycursor.fetchone()[0])

        func = 'SELECT id FROM `teachers` ' \
               'WHERE first_name=%s and last_name=%s'
        mycursor.execute(func, (first_name, last_name))
        teacher_id = mycursor.fetchone()[0]

        func = 'SELECT id FROM `locations`' \
               'WHERE country=%s and city=%s and street=%s and building=%s'
        mycursor.execute(func, (country, city, street, building))

        super().__init__(title, teacher_id, topic_id, mycursor.fetchone()[0])


# x = OffsiteCourse('oh', 'George', 'Kim', ['Math', 'Algebra'], 'Akademika', 12)
# x.save()
