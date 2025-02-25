from app.models.base import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password="", is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string")
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string")
        self._last_name = last_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        self._email = email

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        self._password = password
    
    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be a boolean")
        self._is_admin = is_admin
    
    def update_user(self, user_data):
        self.first_name = user_data.get('first_name', self.first_name)
        self.last_name = user_data.get('last_name', self.last_name)
        self.email = user_data.get('email', self.email)
        self.password = user_data.get('password', self.password)
        self.is_admin = user_data.get('is_admin', self.is_admin)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
            })
        return user_dict
    