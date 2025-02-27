from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    """
    Resource for handling place operations such as creating and retrieving places.
    """
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new place.

        This endpoint allows for the creation of a new place. It validates the input data,
        checks if the owner exists, and creates the place.

        Returns:
            response (dict): Contains the ID of the newly created place and a success message.
            status_code (int): 201 if creation is successful, otherwise 400 if input data is invalid or owner not found.
        """
        place_data = api.payload
        
        owner_id = place_data.get('owner_id')
        owner = facade.get_user(owner_id)

        if not owner:
            return {'error': 'Owner not found'}, 400

        # Populate the 'owner' field with the retrieved user object
        place_data['owner'] = owner.to_dict()

        new_place = facade.create_place(place_data)
        return {'id': str(new_place.id), 'message': 'Place created successfully'}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places.

        This endpoint retrieves a list of all places with basic details.

        Returns:
            response (list): A list of place objects with their basic details.
            status_code (int): 200 if retrieval is successful.
        """
        places = facade.get_all_places()
        return [
            {
                'id': str(place.get('id')),  # Ensure it's a dictionary
                'title': place.get('title'),
                'latitude': place.get('latitude'),
                'longitude': place.get('longitude')
            }
            for place in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource for handling individual place operations such as retrieving and updating a place.
    """
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID.

        This endpoint retrieves the details of a specific place based on its ID. It includes
        information about the owner, amenities, and reviews.

        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            response (dict): The place's details, including owner, amenities, and reviews.
            status_code (int): 200 if retrieval is successful, otherwise 404 if the place is not found.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Ensure place is a dictionary
        place_data = place if isinstance(place, dict) else place.to_dict()

        # Add owner details to the response
        owner = facade.get_user(place_data['owner_id'])
        place_data['owner'] = owner.to_dict() if owner else {}

        # Add amenities details to the response
        place_data['amenities'] = [facade.get_amenity(amenity_id).to_dict()
                                   for amenity_id in place_data.get('amenities', [])]

        # Add reviews to the response
        reviews = facade.get_reviews_for_place(place_id)
        place_data['reviews'] = [review.to_dict() for review in reviews]

        return place_data, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update a place's information.

        This endpoint updates the information of a specific place based on its ID.

        Args:
            place_id (str): The ID of the place to update.

        Returns:
            response (dict): A success message indicating that the place was updated.
            status_code (int): 200 if update is successful, otherwise 404 if the place is not found or 400 if input data is invalid.
        """
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        updated_place = facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200