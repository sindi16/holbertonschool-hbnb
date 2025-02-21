from app.models.base import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if not isinstance(owner, User):
            raise TypeError("Owner must be user instance")
        self._owner = owner

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number")
        if price < 0:
            raise ValueError("Price must be positive")
        self._price = price

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude does not exist")
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude does not exist")
        self._latitude = latitude

    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("Review must be an object of review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an object of class Amenity")
        self.amenities.append(amenity)
