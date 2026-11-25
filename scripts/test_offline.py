"""Run synthetic Django regressions without provider or model-download access."""
import os
from pathlib import Path
import socket
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ['DJANGO_SETTINGS_MODULE'] = 'car_rental.test_settings'


def blocked(*args, **kwargs):
    raise RuntimeError('Network access is forbidden in the isolated test suite')


socket.socket.connect = blocked
socket.socket.connect_ex = blocked
socket.create_connection = blocked

from django.core.management import execute_from_command_line

execute_from_command_line(['manage.py', 'test', 'rentals.tests'])
