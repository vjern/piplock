import re
import sys
import json
import http.client
import urllib.request


PYPI_URL = "https://pypi.org/pypi/%s/json"
VERBOSE = False
COMPACT = False


def err(*a):
    if VERBOSE:
        print(*a, file=sys.stderr)


class web:
    @staticmethod
    def get(url: str) -> bytes:
        err('url =', url)
        response: http.client.HTTPResponse = urllib.request.urlopen(url)
        body = response.read()
        assert response.status == 200, (response.status, url, body)
        return body


def get_name(line: str) -> str:
    m = re.match(r'^[\w\[\]-]*', line)
    assert m is not None
    return m.group()


def get_latest(name: str) -> str:
    data = json.loads(web.get(PYPI_URL % name).decode())
    eligible_releases = [
        r for r in data['releases']
        if re.match(r'^[0-9.]+$', r)
    ]
    latest_release = sorted(
        eligible_releases,
        key=lambda v: tuple(map(int, v.split('.')))
    )[-1]
    return latest_release


def round_up(filepath: str):
    with open(filepath) as f:
        for line in map(str.strip, f):
            if line.startswith('#') or not line:
                if not COMPACT:
                    print(line)
                continue
            name = get_name(line)
            if line != name:
                print(line)
            else:
                print(name + '==' + get_latest(name))
