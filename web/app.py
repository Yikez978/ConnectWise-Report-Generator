import views
from flask import render_template, Flask, g, redirect, url_for, request
from werkzeug.contrib.cache import SimpleCache

# 14 days
CACHE_TIMEOUT = 60*60*24*14

cache = SimpleCache()

app = Flask(__name__)
app.register_blueprint(views.mod)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is for the index of the BMT Reporting website.
        Contains the landing and launchpad for BMT reporting.
    """
    return render_template('index.html')

@app.before_request
def return_cached():
    if not request.values:
        response = cache.get(request.path)
        if response:
            print "Using cached response: " + str(response)
            return response

@app.after_request
def cache_response(response):
    if not request.values:
        cache.set(request.path, response, CACHE_TIMEOUT)
    return response

if __name__ == '__main__':
    app.testing = True
    #TODO: turn debugging off
    app.debug = True
    app.run(port=8000)