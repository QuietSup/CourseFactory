import mysql.connector


class Course:
    def __init__(self, title: str, teacher_id: int, topic_id: list[int], location_id: int):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='vfrc15403'
        )
        self.title = title
        self.teacher_id = teacher_id
        self.topic_id = topic_id
        self.location_id = location_id

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


# a = Course('Math course', 1, [1, 2], 1)
# a.save()
