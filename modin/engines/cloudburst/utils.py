import os
from cloudburst.client.client import CloudburstConnection

cloudburst = None


def get_or_init_client():
    global cloudburst
    if cloudburst is None:
        ip = os.environ.get("MODIN_IP", None)
        conn = os.environ.get("MODIN_CONNECTION", None)
        cloudburst = CloudburstConnection(conn, ip)
    return cloudburst
