from hbnb.app.models.base import BaseModel

class Review(BaseModel):
	def __init__(self, text, rating, place, user):
		super.__init__()
		self.text = text
		self.rating = rating
		self.place = place
		self.user = user
	
	@property
	def text(self):
		return self._text
	
	@text.setter
	def text(self, text):
		if not isinstance(text, str):
			raise TypeError("Text must be a string")
		self._text = text
	
	@property
	def rating(self):
		return self._rating
	
	@rating.setter
	def rating(self, rating):
		if not isinstance(rating, float):
			raise TypeError("Rating must be a float")
		if rating < 1 or rating > 5:
			raise ValueError("Rating must be between 1 and 5")
		self._rating = rating
	
	@property
	def place(self):
		return self._place

	@place.setter
	def place(self, place):
		if not isinstance(place, str):
			raise TypeError("Place must be a string")
		self._place = place
	
	@property
	def user(self):
		return self._user
	
	@user.setter
	def user(self, user):
		if not isinstance(user, str):
			raise TypeError("User must be a string")
		self._user = user
	

	def to_dict(self):
		review_dict = super().to_dict()
		review_dict.update({
			'text': self.text,
			'rating': self.rating,
			'place': self.place,
			'user': self.user
            })
		return review_dict
