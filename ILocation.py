import mysql.connector


class Location:
    def __init__(self, country: str, city: str, street: str, building: int):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='vfrc15403'
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


# a = Location("Ukraine", 'Kyiv', 'Akademika', 12)
# a.save()
# print(a)
