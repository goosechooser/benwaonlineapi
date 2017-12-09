import pytest
from marshmallow import pprint
from flask import url_for

post_headers = {'Accept': 'application/vnd.api+json',
                'Content-Type': 'application/vnd.api+json'}

# unit test the processors
# test(s) that prove the processors are chained in the right order