from app.models.base import BaseModel

class Amenity(BaseModel):
	def __init__(self, name, description):
		super().__init__()
		self.name = name
		self.description = description
	
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		if not isinstance(name, str):
			raise TypeError("Name must be a string")
		self._name = name
	
	@property
	def description(self):
		return self._description
	
	@description.setter
	def description(self, description):
		if not isinstance(description, str):
			raise TypeError("Description must be a string")
		self._description = description
	
	
	def to_dict(self):
		amenity_dict = super().to_dict()
		amenity_dict.update({
			'name': self.name,
			'description': self.description
		})
		return amenity_dict
