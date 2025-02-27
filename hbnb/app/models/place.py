from app.models.base import BaseModel
from app.models.amenity import Amenity
from app.models.user import User
from app.models.review import Review


class Place(BaseModel):
    """
    Place represents a location available for rent.

    Inherits from BaseModel to include id, created_at, and updated_at attributes.

    Attributes:
        title (str): The title of the place.
        description (str): A brief description of the place.
        price (float): The price per night to rent the place.
        latitude (float): The latitude of the place's location.
        longitude (float): The longitude of the place's location.
        owner_id (str): The ID of the user who owns the place.
        amenities (list): A list of amenities available at the place.
        reviews (list): A list of reviews associated with the place.
    """
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a new instance of Place.

        Args:
            title (str): The title of the place.
            description (str): A brief description of the place.
            price (float): The price per night to rent the place.
            latitude (float): The latitude of the place's location.
            longitude (float): The longitude of the place's location.
            owner_id (str): The ID of the user who owns the place.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []

    @property
    def price(self):
        """
        Get the price of the place.

        Returns:
            float: The price per night to rent the place.
        """
        return self._price

    @price.setter
    def price(self, value):
        """
        Set the price of the place. Price must be a non-negative value.

        Args:
            value (float): The price per night to rent the place.

        Raises:
            ValueError: If the price is negative.
        """
        if value < 0:
            raise ValueError("Price must be a non-negative value")
        self._price = float(value)

    @property
    def latitude(self):
        """
        Get the latitude of the place's location.

        Returns:
            float: The latitude of the place's location.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set the latitude of the place's location. Latitude must be between -90 and 90.

        Args:
            value (float): The latitude of the place's location.

        Raises:
            ValueError: If the latitude is not within the range -90 to 90.
        """
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        """
        Get the longitude of the place's location.

        Returns:
            float: The longitude of the place's location.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set the longitude of the place's location. Longitude must be between -180 and 180.

        Args:
            value (float): The longitude of the place's location.

        Raises:
            ValueError: If the longitude is not within the range -180 to 180.
        """
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)
        else:
            raise TypeError("amenity must be an instance of Amenity")

    def add_review(self, review):
        """
        Add an amenity to the place.

        Args:
            amenity (Amenity): An instance of the Amenity class.

        Raises:
            TypeError: If the amenity is not an instance of Amenity.
        """
        if isinstance(review, Review):
            self.reviews.append(review)
        else:
            raise TypeError("review must be an instance of Review")

    def remove_review(self, review):
        """
        Add a review to the place.

        Args:
            review (Review): An instance of the Review class.

        Raises:
            TypeError: If the review is not an instance of Review.
        """
        if review in self.reviews:
            self.reviews.remove(review)
        else:
            raise ValueError("Review not found in this place")

    """
    def to_dict(self):
        # Override to_dict to include amenities and owner details
        place_dict = super().to_dict()
        place_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.id for a in self.amenities],
            # Placeholder for owner details; this would be populated from the User model in the Facade
            "owner": {
                # Example of what might be included
                "id": self.owner_id,  # This would actually pull more detailed info via Facade
            }
        })
        return place_dict
    """

    def to_dict(self):
        """
        Override to_dict to include amenities and owner details.

        Returns:
            dict: A dictionary containing the place's details, including its amenities and reviews.
        """
        place_dict = super().to_dict()
        place_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            # "amenities": [a.id for a in self.amenities],
            # "reviews": [r.id for r in self.reviews]
            # change to below when implementing reviews endpoints
            "amenities": self.amenities,  # Assuming amenities are stored as a list of IDs
            "reviews": self.reviews  # Return the list of review IDs directly
        })
        return place_dict
