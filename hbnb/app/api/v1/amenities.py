from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')  # Added field
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    """
    Resource for handling amenity operations such as creating and retrieving amenities.
    """
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.

        This endpoint allows for the creation of a new amenity. It validates the input data 
        and creates a new amenity.

        Returns:
            response (dict): Contains the ID of the newly created amenity and a success message.
            status_code (int): 201 if creation is successful, otherwise 400 if input data is invalid.
        """
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': str(new_amenity.id), 'message': 'Amenity created successfully'}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.

        This endpoint retrieves a list of all amenities.

        Returns:
            response (list): A list of amenity objects with their details.
            status_code (int): 200 if retrieval is successful.
        """
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource for handling individual amenity operations such as retrieving and updating an amenity.
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.

        This endpoint retrieves details of a specific amenity based on its ID.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            response (dict): The amenity's details.
            status_code (int): 200 if retrieval is successful, otherwise 404 if the amenity is not found.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity's information.

        This endpoint updates the information of a specific amenity based on its ID.

        Args:
            amenity_id (str): The ID of the amenity to update.

        Returns:
            response (dict): A success message indicating that the amenity was updated.
            status_code (int): 200 if update is successful, otherwise 404 if the amenity is not found or 400 if input data is invalid.
        """
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        if not all([amenity_data.get('name'), amenity_data.get('description')]):
            return {'error': 'Invalid input data'}, 400

        # Update the amenity's details
        facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity updated successfully'}, 200