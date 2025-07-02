import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/vercel/path0/.venv/lib/python3.9/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/vercel/path0')
sys.path.append('/vercel/path0/flask_app.py')

from flask_app import app as application

def handler(event, context):
    """
    Vercel serverless function handler for Flask.
    """
    from werkzeug.wrappers import Request, Response
    from werkzeug.routing import MapAdapter
    from werkzeug.exceptions import HTTPException, NotFound

    request = Request(event)
    request.environ['wsgi.url_scheme'] = 'https'
    request.environ['SERVER_NAME'] = event.get('headers', {}).get('host', '')
    request.environ['SERVER_PORT'] = '443'

    # Bind the URL map to the current request environment
    application.url_map.bind_to_environ(request.environ)
    
    response = application.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }
