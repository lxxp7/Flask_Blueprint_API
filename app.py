from flasgger import Swagger
from flask_cors import CORS
from waitress import serve

from FlaskBlueprintTemplateApp import create_app

# Create the Flask app instance
# If you want to use another configuration than the default `settings-dev.py`,
# you can pass the config file path as parameter of the create_app function
app = create_app()

# Custom Swagger configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Template API",
        "description": "Documentation of Template API (Database CRUD, cron jobs).",
        "version": "1.0",
    },
}

swagger = Swagger(app, template=swagger_template)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Root route for the main page at http://host:port/
@app.route('/')
def home():
    return ""

# Run the app
if __name__ == '__main__':
    serve(app, host=app.config.get('FLASK_HOST'), port=app.config.get('FLASK_PORT'))
