from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Amenity represents a specific feature or service offered.

    Inherits from BaseModel to include id, created_at, and updated_at attributes.

    Attributes:
        name (str): The name of the amenity.
        description (str): A brief description of the amenity.
    """
    def __init__(self, name, description):
        """
        Initialize a new instance of Amenity.

        Args:
            name (str): The name of the amenity.
            description (str): A brief description of the amenity.
        """
        super().__init__()
        self.name = name
        self.description = description

    def update(self, name=None, description=None):
        """
        Update the amenity's attributes.

        Args:
            name (str, optional): New name for the amenity. Defaults to None.
            description (str, optional): New description for the amenity. Defaults to None.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description

    def to_dict(self):
        """
        Override to_dict to include description.

        Returns:
            dict: A dictionary containing the id, created_at, updated_at, name, and description of the amenity.
        """
        amenity_dict = super().to_dict()
        amenity_dict.update({
            "name": self.name,
            "description": self.description
        })
        return amenity_dict