"""Check all reachable history without logging matched private content."""
import os
from pathlib import PurePosixPath
import re
import subprocess
import sys


def git(*args):
    return subprocess.check_output(['git', *args])


def main():
    prohibited = {'.doc', '.docx', '.pdf', '.xls', '.xlsx', '.csv', '.pyc', '.sqlite3', '.db'}
    patterns = {
        'private-key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        'github-token': re.compile(rb'\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}'),
        'telegram-token': re.compile(rb'\b\d{7,12}:[A-Za-z0-9_-]{30,50}\b'),
        'cloud-key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    }
    private_pattern = os.environ.get('PRIVACY_FORBIDDEN_PATTERN')
    if private_pattern:
        patterns['private-pattern'] = re.compile(private_pattern.encode(), re.I)
    objects = git('rev-list', '--objects', '--all').splitlines()
    failures = []
    blobs = 0
    for row in objects:
        oid, _, name = row.partition(b' ')
        kind = git('cat-file', '-t', oid.decode()).strip()
        if kind == b'blob':
            blobs += 1
            path = name.decode(errors='replace')
            if PurePosixPath(path).suffix.lower() in prohibited:
                failures.append((oid.decode(), 'private-document-format'))
            if '/__pycache__/' in '/' + path or path.startswith('staticfiles/'):
                failures.append((oid.decode(), 'generated-output'))
        if kind not in {b'blob', b'commit', b'tag'}:
            continue
        data = git('cat-file', kind.decode(), oid.decode())
        for label, pattern in patterns.items():
            if pattern.search(data) or pattern.search(name):
                failures.append((oid.decode(), label))
    for oid, label in failures:
        print(f'{label}: object {oid}', file=sys.stderr)
    print(f'Checked {blobs} reachable blobs; findings: {len(failures)}')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
