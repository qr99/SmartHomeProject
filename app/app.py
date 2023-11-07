from api import api_blueprint
from web import web_blueprint
from flask import Flask


app = Flask(__name__, template_folder="webapp")

api_url_prefix = "/api/1.0/"

# load api functions
app.register_blueprint(api_blueprint, url_prefix=api_url_prefix)

# load functions serving the webapp
app.register_blueprint(web_blueprint)


if __name__ == "__main__":
    port = 4000
    host = "0.0.0.0"

    app.run(port=port, host=host, debug=False, threaded=True)
