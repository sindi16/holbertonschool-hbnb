from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the review (1 to 5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user')
})

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    """
    Resource for handling review operations such as creating and retrieving reviews.
    """
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new review.

        This endpoint allows for the creation of a new review. It validates the input data and
        attempts to create the review.

        Returns:
            response (dict): Contains the ID of the newly created review and a success message.
            status_code (int): 201 if creation is successful, otherwise 400 if input data is invalid.
        """
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {'id': str(new_review.id), 'message': 'Review created successfully'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        This endpoint retrieves a list of all reviews with their details.

        Returns:
            response (list): A list of review objects with their details.
            status_code (int): 200 if retrieval is successful.
        """
        reviews = facade.get_all_reviews()
        return [
            {
                'id': str(review.id),  # Ensure it's a dictionary
                'text': review.get('text'),
                'rating': review.get('rating'),
                'place_id': review.get('place_id'),
                'user_id': review.get('user_id')
            }
            for review in reviews
        ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource for handling individual review operations such as retrieving, updating, and deleting a review.
    """
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.

        This endpoint retrieves the details of a specific review based on its ID.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            response (dict): The review's details if found.
            status_code (int): 200 if retrieval is successful, otherwise 404 if the review is not found.
        """
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update a review's information.

        This endpoint updates the information of a specific review based on its ID.

        Args:
            review_id (str): The ID of the review to update.

        Returns:
            response (dict): A success message indicating that the review was updated.
            status_code (int): 200 if update is successful, otherwise 404 if the review is not found or 400 if input data is invalid.
        """
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, **review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review.

        This endpoint deletes a specific review based on its ID.

        Args:
            review_id (str): The ID of the review to delete.

        Returns:
            status_code (int): 204 if deletion is successful, otherwise 404 if the review is not found.
        """
        try:
            facade.delete_review(review_id)
            return '', 204
        except ValueError as e:
            return {'error': str(e)}, 404