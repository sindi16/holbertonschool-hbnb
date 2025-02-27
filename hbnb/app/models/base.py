import uuid
from datetime import datetime

class BaseModel:
    """
    BaseModel serves as the base class for all models in the application.

    Attributes:
        id (str): Unique identifier for each instance, generated using UUID.
        created_at (datetime): Timestamp indicating when the instance was created.
        updated_at (datetime): Timestamp indicating when the instance was last updated.
    """
    def __init__(self):
        """
        Initialize a new instance of BaseModel.

        Generates a unique id and sets the created_at and updated_at timestamps
        to the current date and time.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp.

        This method should be called whenever the instance is modified to 
        reflect the current date and time.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Return a dictionary representation of the instance.

        Converts the instance's attributes to a dictionary, with the timestamps
        formatted as ISO strings.

        Returns:
            dict: A dictionary containing the id, created_at, and updated_at of the instance.
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }