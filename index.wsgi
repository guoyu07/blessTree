import sae
import os
import sys

root = os.path.dirname(__file__)
sae.add_vendor_dir('vender')
from blessTree import wsgi

application = sae.create_wsgi_app(wsgi.application)