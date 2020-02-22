"""Pulls contact info from HEART and checks to see if that contact
info exists in Little Green Light. Produces a report that lists
any e-mail address or phone numbers that appear in HEART but not in LGL."""
import json
import time

from lgl import LittleGreenLight


LGL = LittleGreenLight()


def get_lgl_contact_info():
    """Pulls contact information from Little Green Light. Sleeps
    for 1.5 seconds after each REST call to avoid exceeding the rate
    limit for the LGL API.


    Returns
    -------
    emails : set
        the set of email address that are currently in LGL
    phones : set
        the set of phone numbers that are currently in LGL
    """
    constituents = _lgl_get('constituents')['items']
    total = len(constituents)

    emails = set()
    phones = set()

    for i, constituent in enumerate(constituents):
        print('Processing constituent {}/{}'.format(i+1, total))
        constituent_id = constituent['id']
        url = 'constituents/{}'.format(constituent_id)
        constituent = _lgl_get(url)

        for email in constituent['email_addresses']:
            emails.add(email['address'])

        for phone in constituent['phone_numbers']:
            phones.add(phone['number'])

        time.sleep(1.5) # Avoid the LGL API rate limit
    return emails, phones


def _lgl_get(url):
    """Makes a GET call to the LGL API and handles appropriately based
    on the HTTP status code

    Parameters
    ----------
    url : str
        the url for the GET call

    Returns
    -------
    items : dict
        a dictionary of metadata for the object of interest
    """
    r = LGL.get(url)
    if r.status_code != 200:
        raise ValueError('LGL API call failed. '
                         'Status code: {}'.format(r.status_code))
    return json.loads(r.text)




