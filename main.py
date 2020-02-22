"""Pulls contact info from HEART and checks to see if that contact
info exists in Little Green Light. Produces a report that lists
any e-mail address or phone numbers that appear in HEART but not in LGL."""
import csv
from collections import OrderedDict
import datetime
import json
import time
import os

from heartcrm import HeartCRM

from lgl import LittleGreenLight


LGL = LittleGreenLight()

# The keys are the field names that appear in HEART and the entries
# are the column names in the final csv
HEART_CONTACT_FIELDS = OrderedDict([
    ('FirstName', 'First Name'),
    ('LastName', 'Last Name'),
    ('Email', 'Email'),
    ('npe01__AlternateEmail__c', 'Alternate Email'),
    ('npe01__HomeEmail__c', 'Home Email'),
    ('MobilePhone', 'Mobile Phone'),
    ('HomePhone', 'Home Phone')
])


def build_missing_contact_report():
    """Builds a .csv file that shows any contact in the HEART database
    who either (1) does not appear in LGL or (2) has at least one piece
    of contact information that does not appear in LGL. Creates a file
    with the naming convention missing_contact_report_<date>.csv"""
    heart_contacts = get_heart_contact_info()
    names, emails, phones = get_lgl_contact_info()

    report_rows = _build_report_rows(heart_contacts, names, emails, phones)
    _save_missing_contact_report(report_rows)


def _save_missing_contact_report(report_rows):
    """Saves the missing contact report as a csv file

    Parameters
    ----------
    report_rows : list
        a list of dictionaries, which correspond go the rows in the report
    """
    csv_columns = [HEART_CONTACT_FIELDS[k] for k in HEART_CONTACT_FIELDS]
    csv_columns.append('Missing')
    today = datetime.datetime.today()
    filename = 'missing_contact_report_{}.csv'.format(today.date())

    try:
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for row in report_rows:
                writer.writerow(row)
        print('Wrote the report to {}'.format(filename))
    except IOError:
        print('Failed to write the report to CSV.')


def _build_report_rows(heart_contacts, names, emails, phones):
    """Uses the results of the HEART and LGL queries to build the rows
    for the missing contact report

    Parameters
    ----------
    heart_contact : list
        the list of contacts in HEART CRM
    names : set
        the set of names from LGL
    emails : set
        the set of emails from LGL
    phones : set
        the set of phone numbers from LGL

    Returns
    -------
    report_rows : list
        a list of dictionaries, which correspond go the rows in the report
    """
    report_rows = list()
    for contact in heart_contacts:
        missing = set()
        for field in HEART_CONTACT_FIELDS:
            if not contact[field]:
                continue
            if (contact['FirstName'], contact['LastName']) not in names:
                missing.add('Name')
            if 'email' in field.lower() and contact[field] not in emails:
                missing.add('Email')
            if 'phone' in field.lower() and contact[field] not in phones:
                missing.add('Phone')

        # Only write rows to the report if they have missing contact info.
        if any(missing):
            row = dict()
            for field in HEART_CONTACT_FIELDS:
                clean_field = HEART_CONTACT_FIELDS[field]
                row[clean_field] = contact[field]
            row['Missing'] = ', '.join(missing)
            report_rows.append(row)

    return report_rows


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
    constituents = _get_constituents()
    total = len(constituents)

    emails = set()
    phones = set()
    names = set()

    for i, constituent in enumerate(constituents):
        print('Processing constituent {}/{}'.format(i+1, total))
        constituent_id = constituent['id']
        url = 'constituents/{}'.format(constituent_id)
        constituent = _lgl_get(url)

        names.add((constituent['first_name'], constituent['last_name']))

        for email in constituent['email_addresses']:
            emails.add(email['address'])

        for phone in constituent['phone_numbers']:
            phones.add(phone['number'].replace('-',''))

        time.sleep(1.5) # Avoid the LGL API rate limit
    return names, emails, phones


def _get_constituents():
    """Walks the LGL urls until all of the constituents in the database
    have been retrieved.

    Returns
    -------
    constituents : list
        a list of dictionaries with metadata about each constituent
    """
    response = _lgl_get('constituents')
    next_url = response['next_link']
    constituents = response['items']
    while next_url:
        time.sleep(1.5) # Avoid the LGL API rate limit
        url = next_url.split('/')[-1] # Remove the base url
        response = _lgl_get(url)
        constituents.extend(response['items'])
        if 'next_link' not in response:
            break
        next_url = response['next_link']
    return constituents


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


def get_heart_contact_info():
    """Pulls email address and phone numbers from HEART CRM so we can
    see which still need to be entered into LGL.

    Returns
    -------
    results : list
        the records of the SOQL query against Salesforce
    """
    heart = _initialize_heart()
    fields = ', '.join(HEART_CONTACT_FIELDS)
    soql = "SELECT {} FROM Contact".format(fields)
    results = heart.query_all(soql)
    return results['records']


def _initialize_heart():
    """Builds the HeartCRM object that is used to authenticate with
    Salesforce via OAUTH2 and query the database."""
    if 'HEART_CONSUMER_KEY' in os.environ:
        client_id = os.environ['HEART_CONSUMER_KEY']
    else:
        client_id = input('Enter the HEART consumer key: ')

    if 'HEART_CONSUMER_SECRET' in os.environ:
        client_secret = os.environ['HEART_CONSUMER_SECRET']
    else:
        client_secret = input('Enter the HEART consumer secret: ')

    access_code = input('Enter you access code: ')
    sandbox = input('Is this a sandbox account (y/n)? ')
    sandbox = sandbox.lower().startswith('y')
    redirect_uri = 'https://salesforce.shirconnect.com'

    return HeartCRM(client_secret=client_secret, client_id=client_id,
                    redirect_uri=redirect_uri, access_code=access_code,
                    sandbox=sandbox)


if __name__ == '__main__':
    build_missing_contact_report()
