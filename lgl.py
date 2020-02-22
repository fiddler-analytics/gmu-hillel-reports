"""Module that handles making REST calls to the Little Green Light API."""
import os
import urllib

from requests import Session

BASE_URL = 'https://api.littlegreenlight.com/api/v1/'


class LittleGreenLight(Session):
    def __init__(self, token=None):
        """A sub-class of the requests.Session class that sets the header
        for LGL authentication and applies the base url for the LGL API."""
        super().__init__()

        token = self._get_token(token)
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

    def request(self, method, url, *args, **kwargs):
        """Overwrites the default request method on the Session class to
        prefix any requests with the Little Green Light API base URL.

        Parameters
        ----------
        method : callable
            a method of the Session class. For instance, get
        url : str
            the LGL end point to call

        Returns
        -------
        requests.Response
        """
        url = urllib.parse.urljoin(BASE_URL, url)
        return super().request(method, url, *args, **kwargs)

    def _get_token(self, token):
        """Gets the API token that is used for LGL API requests.

        Parameters
        ----------
        token : str
            the LGL API token. If None, looks for the API token in
            the LGL_TOKEN environemental variable and prompts the user
            if it is unavailable

        Returns
        -------
        token : str
            the API token that will be used in requeests
        """
        if not token:
            if 'LGL_TOKEN' in os.environ:
                token = os.environ['LGL_TOKEN']
            else:
                token = input('Enter your LGL API Token: ')
        return token
