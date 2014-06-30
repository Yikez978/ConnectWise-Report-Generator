import views
from flask import render_template, Flask, g, redirect, url_for

app = Flask(__name__)
app.register_blueprint(views.mod)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is for the index of the BMT Reporting website.
        Contains the landing and launchpad for BMT reporting.
    """
    return render_template('index.html')

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    app.run(port=8000)