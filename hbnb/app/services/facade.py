from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    """
    Facade for managing the interactions between various models and their repositories.

    Attributes:
        user_repo (InMemoryRepository): Repository for User entities.
        place_repo (InMemoryRepository): Repository for Place entities.
        review_repo (InMemoryRepository): Repository for Review entities.
        amenity_repo (InMemoryRepository): Repository for Amenity entities.
    """
    _shared_user_repo = InMemoryRepository()
    _shared_place_repo = InMemoryRepository()
    _shared_review_repo = InMemoryRepository()
    _shared_amenity_repo = InMemoryRepository()

    def __init__(self):
        """
        Initialize HBnBFacade with shared repositories 
        for users, places, reviews, and amenities.
        """
        self.user_repo = HBnBFacade._shared_user_repo
        self.place_repo = HBnBFacade._shared_place_repo
        self.review_repo = HBnBFacade._shared_review_repo
        self.amenity_repo = HBnBFacade._shared_amenity_repo


    def create_user(self, user_data):
        """
        Create a new user and add it to the user repository.

        Args:
            user_data (dict): User attributes including 'first_name', 'last_name', 'email', and 'password'.

        Returns:
            User: The created User object.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        print(f"User created with ID: {user.id}")  # Debug print
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID from the user repository.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            User: The User object if found, otherwise None.
        """
        user = self.user_repo.get(user_id)
        if user:
            print(f"Found user with ID: {user.id}")  # Debug print
        else:
            print(f"User with ID {user_id} not found")  # Debug print
        return user

    def get_user_by_email(self, email):
        """
        Retrieve a user by email from the user repository.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User: The User object if found, otherwise None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieve all users from the user repository.

        Returns:
            list: A list of User objects.
        """
        return self.user_repo.get_all()

    def update_user(self, user):
        """
        Update an existing user in the user repository.

        Args:
            user (User): The User object with updated attributes.
        """
        self.user_repo.update(user.id, user.to_dict())

    def create_amenity(self, amenity_data):
        """
        Create a new amenity and add it to the amenity repository.

        Args:
            amenity_data (dict): Amenity attributes including 'name' and 'description'.

        Returns:
            Amenity: The created Amenity object.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID from the amenity repository.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            Amenity: The Amenity object if found, otherwise None.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities from the amenity repository.

        Returns:
            list: A list of Amenity objects.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity in the amenity repository.

        Args:
            amenity_id (str): The ID of the amenity to update.
            amenity_data (dict): Updated attributes for the amenity.

        Returns:
            Amenity: The updated Amenity object, or None if not found.
        """

        # Fetch the existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        # Update the amenity's attributes
        amenity.update(name=amenity_data.get('name', amenity.name),
                       description=amenity_data.get('description', amenity.description))
        
        # Update the repository
        self.amenity_repo.update(amenity_id, amenity.to_dict())
        return amenity
    
    def create_place(self, place_data):
        """
        Create a new place and add it to the place repository.

        Args:
            place_data (dict): Place attributes including 'title', 'description', 'price', 'latitude', 
                               'longitude', and 'owner_id'.

        Returns:
            Place: The created Place object.

        Raises:
            ValueError: If the owner does not exist.
        """
        owner_id = place_data['owner_id']
        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError("Owner does not exist")
        
        # Remove the 'owner' key if it exists
        place_data.pop('owner', None)

        place = Place(**place_data)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        """
        Retrieve a place by ID from the place repository.

        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            dict: A dictionary containing place details, including owner, amenities, and reviews.
        """
        # Retrieve the place object
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Ensure place is a Place object before converting to dict
        place_dict = place.to_dict() if not isinstance(place, dict) else place

        owner = self.user_repo.get(place_dict.get('owner_id'))

        # Include owner details in the returned dictionary
        if owner:
            place_dict['owner'] = {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            }

        # Ensure 'amenities' key exists and is iterable
        amenities_ids = place_dict.get('amenities', [])
        place_dict['amenities'] = [self.amenity_repo.get(amenity_id).to_dict()
                                for amenity_id in amenities_ids]
        
        # Fetch reviews
        reviews = [self.review_repo.get(review_id).to_dict()
                for review_id in place_dict.get('reviews', [])]
        place_dict['reviews'] = reviews

        return place_dict

    def get_all_places(self):
        """
        Retrieve all places from the place repository.

        Returns:
            list: A list of dictionaries representing all places.
        """
        # Retrieve all place objects
        places = self.place_repo.get_all()

        # Convert each place to dict and include owner and amenities details
        place_list = []
        for place in places:
            # Ensure place is a Place object before converting to dict
            place_dict = place.to_dict() if not isinstance(place, dict) else place

            owner = self.user_repo.get(place_dict.get('owner_id'))

            if owner:
                place_dict['owner'] = {
                    "id": owner.id,
                    "first_name": owner.first_name,
                    "last_name": owner.last_name,
                    "email": owner.email
                }

            # Ensure 'amenities' key exists and is iterable
            amenities_ids = place_dict.get('amenities', [])
            place_dict['amenities'] = [self.amenity_repo.get(amenity_id).to_dict()
                                    for amenity_id in amenities_ids]

            place_list.append(place_dict)

        return place_list
    
    
    def update_place(self, place_id, place_data):
        """
        Update an existing place in the place repository.

        Args:
            place_id (str): The ID of the place to update.
            place_data (dict): Updated attributes for the place.

        Returns:
            Place: The updated Place object, or None if not found.
        """
        # Fetch the existing place
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Update place's attributes
        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        # Update the repository
        self.place_repo.update(place_id, place.to_dict())
        return place
    
    def create_review(self, review_data):
        """
        Create a new review and add it to the review repository.

        Args:
            review_data (dict): Review attributes including 'text', 'rating', 'place_id', and 'user_id'.

        Returns:
            Review: The created Review object.

        Raises:
            ValueError: If the place or user does not exist.
        """
        text = review_data.get('text')
        rating = review_data.get('rating')
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')

        # Validate place and user existence
        place = self.place_repo.get(place_id)
        user = self.user_repo.get(user_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found.")
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        
        # Create and validate the review
        review = Review(text=text, rating=rating, place_id=place_id, user_id=user_id)
        review.validate_rating()
        self.review_repo.add(review)
        
        # Add review to the place
        if not hasattr(place, 'reviews'):
            place.reviews = []
        place.reviews.append(review.id)  # Ensure review ID is stored
        self.place_repo.update(place_id, place.to_dict())

        return review


    def get_review(self, review_id):
        """
        Retrieve a review by ID from the review repository.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            Review: The Review object if found, otherwise None.

        Raises:
            ValueError: If the review does not exist.
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")
        return review

    def get_all_reviews(self):
        """
        Retrieve all reviews from the review repository.

        Returns:
            list: A list of Review objects.
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, **kwargs):
        """
        Update an existing review in the review repository.

        Args:
            review_id (str): The ID of the review to update.
            **kwargs: Keyword arguments for updating review attributes. 
                      Possible keys are 'rating' and 'text'.

        Returns:
            Review: The updated Review object.

        Raises:
            ValueError: If the review with the specified ID is not found.
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")

        if "rating" in kwargs:
            review.rating = kwargs["rating"]
            review.validate_rating()
        if "text" in kwargs:
            review.text = kwargs["text"]

        self.review_repo.update(review_id, review.to_dict())
        return review

    def delete_review(self, review_id):
        """
        Delete a review from the review repository.

        Args:
            review_id (str): The ID of the review to delete.

        Raises:
            ValueError: If the review with the specified ID is not found.
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")
        self.review_repo.delete(review_id)

    def get_reviews_for_place(self, place_id):
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id (str): The ID of the place whose reviews are to be retrieved.

        Returns:
            list: A list of Review objects associated with the specified place.

        Raises:
            ValueError: If the place with the specified ID is not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found.")
        
        # Assuming reviews are stored as a list of review IDs in the place model
        reviews = [self.review_repo.get(review_id) for review_id in place.reviews]
        return reviews