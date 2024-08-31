from utils.email.strategies.abstract import EmailStrategyAbstract


class EmailContext:
    """
    Email context
    """

    def __init__(self, strategy: EmailStrategyAbstract) -> None:
        """
        Initializes the email context

        Parameters
        ----------
        strategy : EmailStrategyAbstract
            The email strategy
        """

        self._strategy = strategy

    def send(self, to: str, **kwargs) -> None:
        """
        Sends the email

        Parameters
        ----------
        to : str
            The email recipient
        **kwargs : dict
            Arbitrary keyword arguments
        """

        self._strategy.send(to=to, **kwargs)
