from .constants import Guess
from .urls import parse_url_for_date, filter_url_for_undateable


def guess_date(url):
    """Guess the date of publication of a url.

    Attributes
    ----------
    url : str
        url used to retrieve the webpage

    Returns
    -------
    date_guesser_rc.constants.Guess object.
    """
    return DateGuesser().guess_date(url)


class DateGuesser(object):
    def __init__(self):
        pass

    def guess_date(self, url):
        """Guess the date of publication of a URL.

        Attributes
        ----------
        url : str
            url used to retrieve the webpage

        Returns
        -------
        date_guesser_rc.constants.Guess object.
        """
        reason_to_skip = filter_url_for_undateable(url)
        if reason_to_skip is not None:
            return reason_to_skip

        # default guess
        guess = Guess(date=None)
        # Try using the url
        guess = parse_url_for_date(url)

        return guess