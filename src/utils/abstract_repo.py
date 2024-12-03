from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        """
        Add one item to the database
        """
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        """
        Find all items in the database
        """
        raise NotImplementedError

    @abstractmethod
    async def check_exists():
        """
        Check if the item exists in the database
        """
        raise NotImplementedError

    @abstractmethod
    async def deactivate_user():
        """
        Ban user by ID
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_id():
        """
        Find item by ID
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_username():
        """
        Find item by username
        """
        raise NotImplementedError

    @abstractmethod
    async def add_by_user_id():
        """
        Add item by user ID
        """
        raise NotImplementedError
