import sae
from app import app

sae.add_vendor_dir('vendor')
application = sae.create_wsgi_app(app)
