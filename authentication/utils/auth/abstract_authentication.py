from abc import ABC, abstractmethod


class AbstractAuthentication(ABC):
    """
    Abstract class for authentication

    Methods
    -------
    validate_data()
        Abstract method to validate data
    validate_user()
        Abstract method to validate user
    """

    @abstractmethod
    def validate_data():
        """
        Abstract method to validate data
        """

        pass

    @abstractmethod
    def validate_user():
        """
        Abstract method to validate user
        """

        pass
