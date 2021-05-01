LOCALE = 'en'

class Guess(object):
    """Date guessing result for the provided URL and its HTML contents."""

    __slots__ = [
        '__date',
    ]

    def __init__(self, date):
        self.__date = date

    @property
    def date(self):
        """datetime.datetime object with the guessed date, or None if a guess can't be made."""
        return self.__date

