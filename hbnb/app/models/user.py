from app.models.base import BaseModel
import re

class User(BaseModel):
    """
    User represents an individual who can interact with the system.

    Inherits from BaseModel to include id, created_at, and updated_at attributes.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
        is_admin (bool): Indicates if the user has admin privileges.
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a new instance of User.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            password (str): The user's password.
            is_admin (bool, optional): If True, the user has admin privileges. Defaults to False.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def validate_email(self):
        """
        Validate the email format.

        Raises:
            ValueError: If the email format is invalid.
        """
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

    def to_dict(self):
        """
        Override to_dict to exclude the password.

        Returns:
            dict: A dictionary containing the user's details, excluding the password.
        """
        user_dict = super().to_dict()
        user_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return user_dict

    def register(self):
        """
        Simulate user registration by validating the email.

        Additional registration logic can be added here.
        """
        self.validate_email()
        # Additional registration logic can be added here

    def update_profile(self, first_name=None, last_name=None, email=None, password=None):
        """
        Update user profile information.

        Args:
            first_name (str, optional): The new first name.
            last_name (str, optional): The new last name.
            email (str, optional): The new email address.
            password (str, optional): The new password.

        Raises:
            ValueError: If the email format is invalid.
        """
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
            self.validate_email()
        if password:
            self.password = password

    def delete(self):
        """
        Simulate user deletion.

        Additional deletion logic can be added here.
        """
        pass