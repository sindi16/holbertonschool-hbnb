from app.models.base import BaseModel

class Review(BaseModel):
    """
    Review represents feedback provided by a user for a place.

    Inherits from BaseModel to include id, created_at, and updated_at attributes.

    Attributes:
        text (str): The content of the review.
        rating (int): The rating given by the user, between 1 and 5.
        place_id (str): The ID of the place being reviewed.
        user_id (str): The ID of the user who wrote the review.
    """
    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a new instance of Review.

        Args:
            text (str): The content of the review.
            rating (int): The rating given by the user, between 1 and 5.
            place_id (str): The ID of the place being reviewed.
            user_id (str): The ID of the user who wrote the review.

        Raises:
            ValueError: If the rating is not between 1 and 5.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

         # Validate the rating upon initialization
        self.validate_rating()

    def validate_rating(self):
        """
        Validate that the rating is within the allowed range of 1 to 5.

        Raises:
            ValueError: If the rating is not between 1 and 5.
        """
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    def to_dict(self):
        """
        Override to_dict to include place_id and user_id.

        Returns:
            dict: A dictionary containing the review's details, including text, rating, place_id, and user_id.
        """
        review_dict = super().to_dict()
        review_dict.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        })
        return review_dict