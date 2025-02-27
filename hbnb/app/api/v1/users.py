from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user'),  # Added field
    'is_admin': fields.Boolean(description='Whether the user has admin privileges')  # Added field
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    """
    Resource for handling user operations such as creating and retrieving users.
    """
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        This endpoint allows for the creation of a new user. It checks if the provided email is already registered, 
        validates the input data, and then creates a new user.

        Returns:
            response (dict): Contains the ID of the newly created user and a success message.
            status_code (int): 201 if creation is successful, otherwise 400 if email is already registered or if input data is invalid.
        """
        user_data = api.payload

        # Simulate email uniqueness check
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Validate input data
        if not all([user_data.get('first_name'), user_data.get('last_name'), user_data.get('email'), user_data.get('password')]):
            return {'error': 'Invalid input data'}, 400

        new_user = facade.create_user(user_data)
        return {'id': str(new_user.id), 'message': 'User created successfully'}, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """
        Retrieve all users.

        This endpoint retrieves a list of all users.

        Returns:
            response (list): A list of user objects with their IDs, first names, last names, and emails.
            status_code (int): 200 if retrieval is successful.
        """
        users = facade.get_all_users()
        return [{'id': str(user.id), 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for handling individual user operations such as retrieving, updating, and deleting a user.
    """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.

        This endpoint retrieves details of a specific user based on their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            response (dict): The user's details.
            status_code (int): 200 if retrieval is successful, otherwise 404 if the user is not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update user information.

        This endpoint updates the information of a specific user based on their ID.

        Args:
            user_id (str): The ID of the user to update.

        Returns:
            response (dict): A success message indicating that the user was updated.
            status_code (int): 200 if update is successful, otherwise 404 if the user is not found or 400 if input data is invalid.
        """
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not all([user_data.get('first_name'), user_data.get('last_name'), user_data.get('email')]):
            return {'error': 'Invalid input data'}, 400

        # Update the user's profile with new data
        user.update_profile(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password')
        )
        facade.update_user(user)  
        return {'message': 'User updated successfully'}, 200