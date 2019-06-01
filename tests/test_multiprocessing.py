import os
from multiprocessing import Process

from directaccess import DirectAccessV2

DIRECTACCESS_API_KEY = os.getenv('DIRECTACCESS_API_KEY')
DIRECTACCESS_CLIENT_ID = os.getenv('DIRECTACCESS_CLIENT_ID')
DIRECTACCESS_CLIENT_SECRET = os.getenv('DIRECTACCESS_CLIENT_SECRET')

api_token = DirectAccessV2(
    api_key=DIRECTACCESS_API_KEY,
    client_id=DIRECTACCESS_CLIENT_ID,
    client_secret=DIRECTACCESS_CLIENT_SECRET,
    retries=5,
    backoff_factor=1
).access_token


def query(endpoint, **options):
    """
    Test that the originally acquired access_token is still valid and that no new
    authentication request was sent from within the child process.

    :param endpoint: a valid Direct Access API dataset endpoint
    :param options: kwargs of valid query parameters for the dataset endpoint
    :return:
    """
    client = DirectAccessV2(
        api_key=DIRECTACCESS_API_KEY,
        client_id=DIRECTACCESS_CLIENT_ID,
        client_secret=DIRECTACCESS_CLIENT_SECRET,
        retries=5,
        backoff_factor=1,
        access_token=api_token
    )

    resp = client.query(endpoint, **options)
    next(resp)
    assert api_token == client.access_token
    return


def test_multiple_processes():
    procs = list()
    a = Process(
        target=query,
        kwargs=dict(
            endpoint='rigs',
            pagesize=1
        )
    )
    procs.append(a)

    b = Process(
        target=query,
        kwargs=dict(
            endpoint='permits',
            pagesize=1
        )
    )
    procs.append(b)

    [x.start() for x in procs]
    [x.join() for x in procs]
    return
