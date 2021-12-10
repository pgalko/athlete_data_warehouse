import sys
sys.path.append('<eg. /var/www/superset>')
from superset.app import create_app
application = create_app()