from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_place = api.payload
        new_place = facade.create_place(user_place)
        return {'id': new_place.id, 'title': new_place.title, 'description': new_place.description, 'price': new_place.price, 'latitude': new_place.latitude, 'longitude': new_place.longitude, 'owner_id': new_place.owner_id, 'amenities': new_place.amenities}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        places_list = [{'id': str(place.id), 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner': {'id': str(place.owner.id), 'first_name': place.owner.first_name, 'last_name': place.owner.last_name, 'email': place.owner.email}, 'amenities': [{'id': str(amenity.id), 'name': amenity.name} for amenity in place.amenities]} for place in places]	

    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if place:
            return {'id': str(place.id), 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner': {'id': str(place.owner.id), 'first_name': place.owner.first_name, 'last_name': place.owner.last_name, 'email': place.owner.email}, 'amenities': [{'id': str(amenity.id), 'name': amenity.name} for amenity in place.amenities]}, 200
        return {'message': 'Place not found'}, 404

      

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        place_data = api.payload
        facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200