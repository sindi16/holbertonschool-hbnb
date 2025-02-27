from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract base class for repository operations. Defines the contract for 
    any repository implementation.

    Methods:
        add(obj): Add an object to the repository.
        get(obj_id): Retrieve an object by its ID.
        get_all(): Retrieve all objects from the repository.
        update(obj_id, data): Update an object's attributes.
        delete(obj_id): Delete an object by its ID.
        get_by_attribute(attr_name, attr_value): Retrieve an object by a specific attribute.
    """
    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj (BaseModel): The object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.

        Returns:
            BaseModel: The object with the specified ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            list: A list of all objects in the repository.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object's attributes.

        Args:
            obj_id (str): The ID of the object to update.
            data (dict): A dictionary of attributes to update.

        Raises:
            KeyError: If the object with the specified ID is not found.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id (str): The ID of the object to delete.

        Raises:
            KeyError: If the object with the specified ID is not found.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute.

        Args:
            attr_name (str): The name of the attribute to search by.
            attr_value: The value of the attribute to match.

        Returns:
            BaseModel: The object with the specified attribute value, or None if not found.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository class. Stores objects in a 
    dictionary for quick access.

    Attributes:
        _storage (dict): A dictionary to store objects with their IDs as keys.

    Methods:
        add(obj): Add an object to the repository.
        get(obj_id): Retrieve an object by its ID.
        get_all(): Retrieve all objects from the repository.
        update(obj_id, data): Update an object's attributes.
        delete(obj_id): Delete an object by its ID.
        get_by_attribute(attr_name, attr_value): Retrieve an object by a specific attribute.
    """
    def __init__(self):
        """
        Initializes the object with dictionary to store objects with their IDs as keys.
        """
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj (BaseModel): The object to add.
        """
        self._storage[obj.id] = obj
    
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.

        Returns:
            BaseModel: The object with the specified ID, or None if not found.
        """
        obj = self._storage.get(obj_id)
        if obj:
            print(f"Retrieved object: {obj_id}")
        else:
            print(f"Object not found: {obj_id}")
        return obj

    def get_all(self):
        """
        Retrieve all objects from the repository.

        Returns:
            list: A list of all objects in the repository.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object's attributes.

        Args:
            obj_id (str): The ID of the object to update.
            data (dict): A dictionary of attributes to update.

        Raises:
            KeyError: If the object with the specified ID is not found.
        """
        if obj_id in self._storage:
            obj = self._storage[obj_id]
            # Update the attributes of the object based on the provided data
            for key, value in data.items():
                setattr(obj, key, value)
                print(f"Updated object with ID: {obj_id}")  # Debug output
        else:
            raise KeyError("Object not found")

    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id (str): The ID of the object to delete.

        Raises:
            KeyError: If the object with the specified ID is not found.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            print(f"Deleted object with ID: {obj_id}")  # Debug output

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute.

        Args:
            attr_name (str): The name of the attribute to search by.
            attr_value: The value of the attribute to match.

        Returns:
            BaseModel: The object with the specified attribute value, or None if not found.
        """
        obj = next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
        if obj:
            print(f"Found object with {attr_name}: {attr_value}")  # Debug output
        else:
            print(f"Object not found with {attr_name}: {attr_value}")  # Debug output
        return obj