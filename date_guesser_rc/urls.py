import datetime
import itertools
import re
from urllib.parse import urlparse

import arrow
import pytz

from .constants import LOCALE, Guess

# inspired by (MIT licensed) https://github.com/codelucas/newspaper
_LOCALE = arrow.locales.get_locale(LOCALE)
SEPARATOR = r'([\./\-_]{0,1})'
YEAR_PATTERN = r'(?P<year>(?:19|20)\d{2})'
MONTH_PATTERN = r'(?P<month>(?:[0-3]{0,1}[0-9])|(?:[a-zA-Z]{3,5}))'
DAY_PATTERN = r'(?P<day>[0-3]{0,1}[0-9])'
HOUR_PATTERN = r'(?P<hour>(?:[01]\d|2[0-3]))'
MINUTE_PATTERN = r'(?P<minute>(?:[0-5]\d))'
SECOND_PATTERN = r'(?P<second>(?:[0-5]\d))'

URL_DATE_REGEX = re.compile(
    r'{sep}{year}{sep}{month}{sep}(?:{day}{sep})?(?!\d)'.format(
        sep=SEPARATOR, year=YEAR_PATTERN, month=MONTH_PATTERN, day=DAY_PATTERN))

URL_DATE_REGEX_BACKWARDS = re.compile(
    r'{sep}{month}(?:{sep}{day})?{sep}{year}{sep}(?!\d)'.format(
        sep=SEPARATOR, year=YEAR_PATTERN, month=MONTH_PATTERN, day=DAY_PATTERN))

URL_DATE_REGEX_PT = re.compile(
    r'(?:{day}{sep}){sep}{month}{sep}{year}{sep}?(?!\d)'.format(
        sep=SEPARATOR, year=YEAR_PATTERN, month=MONTH_PATTERN, day=DAY_PATTERN))

URL_DATE_REGEX_PTArquivo = re.compile(
    r'{sep}{year}{month}(?:{day}){hour}{minute}{second}?(?!\d)'.format(
        sep=SEPARATOR, year=YEAR_PATTERN, month=MONTH_PATTERN, day=DAY_PATTERN, hour=HOUR_PATTERN,
        minute=MINUTE_PATTERN, second=SECOND_PATTERN))


def url_date_generator(url):
    """Generates possible date matches from a url

    Parameters
    ----------
    url: string

    Yields
    ------
    (dict, str)
        dictionary with keys 'year', 'month', 'day'
        string describing how the dictionary was found
    """
    '''
    matches = itertools.chain(URL_DATE_REGEX.finditer(url), URL_DATE_REGEX_BACKWARDS.finditer(url),
                              URL_DATE_REGEX_PT.finditer(url), URL_DATE_REGEX_PTArquivo.finditer(url))
                              
    '''
    matches = itertools.chain(URL_DATE_REGEX.finditer(url),
                              URL_DATE_REGEX_PT.finditer(url), URL_DATE_REGEX_PTArquivo.finditer(url), URL_DATE_REGEX_BACKWARDS.finditer(url))
    #matches = itertools.chain(URL_DATE_REGEX_PTArquivo.finditer(url))
    for match in matches:
        method = 'Found {} in url'.format(match.group())
        yield match.groupdict(), method


def parse_url_for_date(url):
    """Extracts a date from the url

    Parameters
    ----------
    url: string

    Returns
    -------
    date_guesser_rc.constants.Guess object.
    """
    for captures, method in url_date_generator(url):
        captures['year'] = int(captures['year'])
        if captures['year'] < 1990 or captures['year'] > 2030:
            continue
        try:
            captures['month'] = int(captures['month'])
        except ValueError:  # month is a string
            month = captures['month'].title()
            manual_months = {
                'Sept': 9
            }
            if month in _LOCALE.month_abbreviations:
                captures['month'] = _LOCALE.month_abbreviations.index(month)
            elif month in manual_months:
                captures['month'] = manual_months[month]
            else:
                continue

        if captures['day'] is None:
            captures['day'] = 15
        else:
            captures['day'] = int(captures['day'])

        try:
            captures['hour'] = int(captures['hour'])
        except:
            captures['hour'] = 0

        try:
            captures['minute'] = int(captures['minute'])
        except:
            captures['minute'] = 0

        try:
            captures['second'] = int(captures['second'])
        except:
            captures['second'] = 0

        try:
            date_guess = datetime.datetime(tzinfo=pytz.utc, **captures)
            return Guess(date=date_guess)
        except ValueError:
            pass
    return Guess(date=None)


def filter_url_for_undateable(url):
    """Common sense checks for a page not having a date.

    Reasons for this include being a non-static page or being a login page.
    Common examples are wikipedia, or a nytimes topics page.

    Parameters
    ----------
    url: string

    Returns
    -------
    date_guesser_rc.constants.Guess object or None
        guess describing why the page is undateable or None if it might be dateable
    """
    parsed = urlparse(url)
    # url fragments that are likely to be undateable
    invalid_paths = {
        'search',
        'tag',
    }
    path_parts = set(parsed.path.strip('/').split('/'))

    hostname = parsed.hostname
    if hostname is None:
        return Guess(date=None)

    elif hostname.endswith('wikipedia.org'):
        return Guess(date=None)

    elif hostname.endswith('twitter.com') and ('status' not in path_parts):
        return Guess(date=None)

    elif parsed.path.strip('/') == '':
        return Guess(date=None)
    path_contains = invalid_paths.intersection(path_parts)
    if path_contains:  # nonempty intersection is truthy
        bad_parts = ', '.join(['"{}"' for segment in path_contains])
        return Guess(date=None)

    return None
