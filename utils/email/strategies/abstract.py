from abc import ABC, abstractmethod


class EmailStrategyAbstract(ABC):
    """
    Email strategy abstract class
    """

    @abstractmethod
    def send(self, to: str, **kwargs) -> None:
        """
        Send abstract method

        Parameters
        ----------
        to : str
            The email recipient
        **kwargs : dict
            Arbitrary keyword arguments
        """

        pass
