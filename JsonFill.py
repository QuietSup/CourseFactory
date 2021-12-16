import json

from numpy.core.defchararray import endswith


class JsonFill:
    def __init__(self, host, user, password, local_country, local_city):
        self.host = host
        self.user = user
        self.password = password
        self.local_country = local_country
        self.local_city = local_city
        self.file_name = 'factory.json'

    def save(self):
        data = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'local_country': self.local_country,
            'local_city': self.local_city
        }

        with open(self.file_name, 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def get_info(self) -> dict:
        with open(self.file_name, 'r') as read_file:
            return json.load(read_file)

    @property
    def host(self):
        return self.__host

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password

    @property
    def local_country(self):
        return self.__local_country

    @property
    def local_city(self):
        return self.__local_city

    @property
    def file_name(self):
        return self.__file_name

    @host.setter
    def host(self, value):
        if not isinstance(value, str):
            raise TypeError('Host must be str type')
        self.__host = value

    @user.setter
    def user(self, value):
        if not isinstance(value, str):
            raise TypeError('User must be str type')
        self.__user = value

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError('password must be str type')
        self.__password = value

    @local_country.setter
    def local_country(self, value):
        if not isinstance(value, str):
            raise TypeError('local_country must be str type')
        self.__local_country = value

    @local_city.setter
    def local_city(self, value):
        if not isinstance(value, str):
            raise TypeError('local_city must be str type')
        self.__local_city = value

    @file_name.setter
    def file_name(self, value):
        if not isinstance(value, str):
            raise TypeError('local_city must be str type')
        if not endswith(value, '.json'):
            raise TypeError('file must have .json type')
        self.__file_name = value


x = JsonFill('localhost', 'root', 'vfrc15403', 'Ukraine', 'Kyiv')
print(x.get_info())
