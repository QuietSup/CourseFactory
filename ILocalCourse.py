import mysql.connector
from ICourse import Course
import json


class LocalCourse(Course):
    def __init__(self, title: str, first_name: str, last_name: str,
                 topic: list[str], street: str, building: int):
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

        with open('factory.json', 'r') as read_file:
            data = json.load(read_file)

        func = 'SELECT id FROM `locations`' \
               'WHERE country=%s and city=%s and street=%s and building=%s'
        mycursor.execute(func, (data['local_country'], data['local_city'],
                                street, building))

        super().__init__(title, teacher_id, topic_id, mycursor.fetchone()[0])


x = LocalCourse('oh', 'George', 'Kim', ['Math', 'Algebra'], 'Akademika', 12)
x.save()
