import re
import os
import io
import sys
import json
import http.client
import urllib
import urllib.request


PYPI_URL = "https://pypi.org/pypi/%s/json"
VERBOSE = False
COMPACT = False
INPLACE = False
YESMAN = False
SORTED = False


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


def get_releases(name: str) -> dict:
    try:
        return json.loads(web.get(PYPI_URL % name).decode())['releases']
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f'\u2715 No such package: {name!r}')
        else:
            print(f'\u2715 Could not retrieve info for package {name!r} (status code {e.code})')
        exit(1)
    except (KeyError, AssertionError) as e:
        print(f'\u2715 Could not retrieve info for package {name!r}')
        exit(1)


def get_latest(name: str) -> str:
    err('Fetching latest release number for', name)
    releases = get_releases(name)
    err('available releases:', list(releases.keys()))
    eligible_releases = [
        r for r in releases
        if re.match(r'^[0-9.]+$', r)
    ]
    latest_release = sorted(
        eligible_releases,
        key=lambda v: tuple(map(int, v.split('.')))
    )[-1]
    return latest_release


def round_up(filepath: str, file=sys.stdout, *, inplace: bool = False):

    with open(filepath) as f:
        lines = f.readlines()

    if inplace:
        file = open(filepath, mode='w')

    for line in map(str.strip, lines):
        if line.startswith('#') or not line:
            if not COMPACT:
                print(line, file=file)
            continue
        name = get_name(line)
        if line != name:
            print(line, file=file)
        else:
            vv = name + '==' + get_latest(name)
            print(vv, file=file)

    if inplace:
        print(f'\u2714 Wrote frozen pip requirements to {filepath}')


def yesno(question: str, default: str = 'y', skip: bool = False) -> bool:
    if skip is not None:
        return skip
    default = default.lower()
    ans = default.upper() + '/' + 'yn'.strip(default)
    return input(f'{question} ({ans})') in ['', 'y', 'Y']


def implicit():

    # detect file
    src = 'requirements.txt'
    if not os.path.exists(src):
        print('No pip requirements file found')
        exit(1)

    # write to requirements.txt if inplace
    dest = 'requirements.lock'
    if INPLACE:
        dest = src
    else:
        if os.path.exists(dest):
            YESMAN or print(f'\u2715 File {dest!r} already exists.', end=' ')
            cont = yesno('Replace ?', skip=YESMAN or None)
            # YESMAN and print()
            cont or exit(1)

    ss = io.StringIO()
    print('Fetching ...')
    round_up(src, ss)
    ss.seek(0)

    with open(dest, mode='w') as f:
        lines = ss.readlines()
        if SORTED:
            lines = sorted(lines)
        f.writelines(lines)

    print('\033[A', end='')
    print(f'\u2714 Wrote frozen pip requirements to {dest} ({len(lines)})')
