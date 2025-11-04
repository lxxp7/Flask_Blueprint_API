# Flask_API Back

A Flask REST API template for building modular applications using blueprints.

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtualenv

## Installation

### 1. Clone the repository

```bash
git clone <REPO>
```

### 2. Create a virtual environment to install project dependencies

```bash
cd path/to/Flask_API
python -m venv .venv
```

### 3. Activate the virtual environment

```bash
.venv\Scripts\activate
```

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Production Mode

To run the app in production:

1. Set `SQLALCHEMY_DATABASE_URI`, `FLASK_HOST` and `FLASK_PORT` inside `config/settings.py`
2. Configure the app to use production settings in `Flask_API/app.py`:

```python
app = create_app('config/settings.py')
```

3. Run the app (served by Waitress, a production WSGI server):

```bash
python app.py
```

### Development Mode

For development, remove any parameter in the `create_app()` function call in `app.py`.

**Option 1: Flask development server**

```bash
flask run
```

**Option 2: Flask with debug mode**

```bash
flask run --debug
```

## API Returns Convention

All requests to the API routes will result in a response with one of the following status codes:

### Status Codes

- **200 (Success)**: Request was successfully processed and data is returned to the client
- **204 (No Content)**: Request was successfully processed but no data is returned to the client
- **404 (Not Found)**: The route or requested object couldn't be found/processed, returning an error message

### Response Format Examples

**200 - Success**

```json
{
  "data": the_requested_data (list, dict, bool, etc.)
}
```

**204 - No Content**

```
Empty body
```

**404 - Error**

```json
{
  "error": "the error message"
}
```
