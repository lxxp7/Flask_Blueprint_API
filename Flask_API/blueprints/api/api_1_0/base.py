"""
API 1.0 - base.

This is a the file that will contain all of our routes for our api blueprint.
"""
import os

from flask import Response, current_app, request

from Flask_API.blueprints.api.api_1_0 import api
from Flask_API.utils import sqlalchemy_utils, utils


@api.route('/', methods=["GET"])
def routes_list() -> Response:
    """
    Return the main page of the API with available routes.
    ---
    tags:
      - General
    responses:
      200:
        description: List of available routes.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: string
              example:
                - "/api/1.0/"
                - "/api/1.0/logs"
                - "/api/1.0/create/<string:model_name>"
                - "/api/1.0/update/<string:model_name>"
                - "/api/1.0/delete/<string:model_name>"
                - "/api/1.0/search_dependencies/<string:project_name>"
                - "/"
                - "..."
    """
    """
    Return the main page of the API with available routes.

    Returns:
        Response: A response that contains available routes as a dict.
    """
    routes = [
        rule.rule for rule in current_app.url_map.iter_rules()
        if not rule.rule.startswith('/static')
    ]

    return utils.return_response(routes)


@api.route('/logs')
def get_logs():
    """
    Return the last 'limit' lines from the logfile.
    You can add ?limit=<nb:int> after the route url to specify a limit,
    by default will display the last 100 lines.
    ---
    tags:
      - General
    parameters:
      - name: limit
        in: query
        type: integer
        required: false
        description: Number of log lines to return (default 100).
    responses:
      200:
        description: The logs of the app.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: string
              example:
                - "Data successfully created : {...}"
      500:
        description: The error message if the logs file is not accessible.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: string
              example:
                - "Error reading log file: error message"
    """
    """
    Return the last 'limit' lines from the logfile.

    You can add ?limit=<nb:int> after the route url to specify a limit,
    by default will display the last 100 lines.

    Returns:
        list[str]: a list that contains the last 'limit' lines
    """
    limit = int(request.args.get('limit', 100))
    log_file = current_app.config.get('LOG_FILE')

    if not os.path.exists(log_file):
        return []

    logs = []
    try:
        with open(log_file, 'r') as f:
            for line in f.readlines():
                logs.append(line.strip())
    except (IOError, PermissionError) as e:
        current_app.logger.error(f"Error reading log file: {e}")
        return utils.return_error(f"Error reading log file: {e}", 500)

    # Return the last 'limit' logs
    return utils.return_response(logs[-limit:])

@api.route('/logs/clear')
def clear_logs():
  """
    Clear the logs file.
    ---
    tags:
      - General
    responses:
      200:
        description: The logs file cleared successfully.
        schema:
          type: object
          properties:
            data:
              type: string
              example: "Log file cleared successfully."
      500:
        description: The error message if the logs file could not be cleared.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error clearing log file: error message"
  """
  """
  Clears the logs file.

  Returns:
      Response: A response indicating the result of the operation.
  """
  log_file = current_app.config.get('LOG_FILE')
  try:
      open(log_file, 'w').close()
      return utils.return_response("Log file cleared successfully.")
  except Exception as e:
      return utils.return_error(f"Error clearing log file: {e}", 500)


# Generic CRUD routes
@api.route('/create/<string:model_name>', methods=["POST"])
def create_record(model_name: str) -> Response:
    """
    Create a new record in the specified database table.

    ---
    tags:
      - CRUD
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the table/model to insert the new record into.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            table_pk:
              type: string
              example: "123"
            field1:
              type: string
              example: "value1"
            field2:
              type: string
              example: "value2"
    responses:
      200:
        description: Record created successfully.
        schema:
          type: object
          properties:
            data:
              type: object
              example:
                - true
      400:
        description: Invalid JSON, can't create new record. / Model {model_name} not found.
    """
    """
    Create a record in the database using url keyword being the table name to insert into.

    Expects Json:
    {
        table_pk : pk,
        other_data: ...,
    }

    Returns:
        Response : a response containing the return message of the process
    """
    model_class = sqlalchemy_utils.get_class_from_tablename(model_name)
    if not model_class:
        return utils.return_error(f"Model {model_name} not found")

    data = request.get_json()
    if not data:
        return utils.return_error("Invalid JSON, can't create new record")

    result = sqlalchemy_utils.create_record(model_class, data)
    return utils.return_response(result)


@api.route('/get_record/<string:model_name>', methods=["GET"])
def get_record(model_name: str) -> Response:
    """
    Retrieve a record from the specified database table by its primary key.

    ---
    tags:
      - CRUD
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the table/model to retrieve the record from.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            record_pk_to_get:
              type: string
              example: "123"
    responses:
      200:
        description: Record retrieved successfully.
        schema:
          type: object
          properties:
            data:
              type: object
              example:
                table_pk: "123"
                field1: "value1"
                field2: "value2"
      400:
        description: Invalid input or JSON data. / Model/table or record not found.
    """
    """
    Retrieve an existing record in the database using url keyword being the table name to get from.

    Expects Json:
    {
        record_pk_to_get : pk,
    }

    Returns:
        Response : a response containing the return message of the process
    """
    model_class = sqlalchemy_utils.get_class_from_tablename(model_name)
    if not model_class:
        return utils.return_error(f"Model {model_name} not found")

    data = request.get_json()
    if not data:
        return utils.return_error("Invalid JSON, can't get the record")

    result = sqlalchemy_utils.get_record_by_key(model_class, data)
    return utils.return_response(sqlalchemy_utils.record_as_dict(result))


@api.route('/get_records/<string:model_name>', methods=["GET"])
def get_records(model_name: str) -> Response:
    """
    Retrieve all records from the specified database table.

    ---
    tags:
      - CRUD
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the table/model to retrieve all records from.
    responses:
      200:
        description: Records retrieved successfully.
        schema:
          type: object
          properties:
            data:
              type: object
              example:
                0:
                  table_pk: "123"
                  field1: "value1"
                  field2: "value2"
                1:
                  table_pk: "124"
                  field1: "value3"
                  field2: "value4"
      400:
        description: Model/table not found.
    """
    """
    Retrieve all existing records in the database using url keyword being the table name to get from.

    Args:
        URL Keyword: model_name to get records from
    Returns:
        Response : a response containing the return message of the process
    """
    model_class = sqlalchemy_utils.get_class_from_tablename(model_name)
    if not model_class:
        return utils.return_error(f"Model {model_name} not found")

    result = sqlalchemy_utils.get_records_by_key(model_class, {})

    records_dict = {}
    for i, record in enumerate(result):
        records_dict[i] = sqlalchemy_utils.record_as_dict(record)

    return utils.return_response(records_dict)


@api.route('/update/<string:model_name>', methods=["PUT"])
def update_record(model_name: str) -> Response:
    """
    Update an existing record in the specified database table.

    ---
    tags:
      - CRUD
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the table/model to update the record in.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            record_pk_to_update:
              type: string
              example: "123"
            data_to_update:
              type: object
              example:
                field1: "new_value1"
                field2: "new_value2"
    responses:
      200:
        description: Record updated successfully.
        schema:
          type: object
          properties:
            data:
              type: object
              example:
                - true
      400:
        description: Invalid JSON, can't update the record. / Bad request / Model/table or record not found.
    """
    """
    Update an existing record in the database using url keyword being the table name to update from.

    Expects Json:
    {
        record_pk_to_update : pk,
        data_to_update: ...,
    }

    Returns:
        Response : a response containing the return message of the process
    """
    model_class = sqlalchemy_utils.get_class_from_tablename(model_name)
    if not model_class:
        return utils.return_error(f"Model {model_name} not found")

    data = request.get_json()
    if not data:
        return utils.return_error("Invalid JSON, can't update the record")

    result = sqlalchemy_utils.update_record(model_class, data)
    return utils.return_response(result)


@api.route('/delete/<string:model_name>', methods=["DELETE"])
def delete_record(model_name: str) -> Response:
    """
    Delete an existing record from the specified database table.

    ---
    tags:
      - CRUD
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the table/model to delete the record from.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            record_pk_to_delete:
              type: string
              example: "123"
    responses:
      200:
        description: Record deleted successfully.
        schema:
          type: object
          properties:
            data:
              type: object
              example:
                - true
      400:
        description: Invalid JSON, can't delete the record. / Model/table not found.
    """
    """
    Delete an existing record in the database using url keyword being the table name to delete from.

    Expects Json:
    {
        record_pk_to_delete : pk,
    }

    Returns:
        Response : a response containing the return message of the process
    """
    model_class = sqlalchemy_utils.get_class_from_tablename(model_name)
    if not model_class:
        return utils.return_error(f"Model {model_name} not found")

    data = request.get_json()
    if not data:
        return utils.return_error("Invalid JSON, can't delete the record")

    result = sqlalchemy_utils.delete_record(model_class, data)
    return utils.return_response(result)


@api.route("/schema/<string:model_name>", methods=["GET"])
def get_table_schema(model_name):
    """
    Get the schema of a specific database model.

    This endpoint retrieves the schema of the specified SQLAlchemy model, including
    column names, types, primary keys, and foreign keys. Useful for dynamically generating forms
    or data tables based on database models in the frontend.

    ---
    tags:
      - Database
    parameters:
      - name: model_name
        in: path
        type: string
        required: true
        description: The name of the database model to inspect.
    responses:
      200:
        description: The schema of the specified model.
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                description: Column name
                example: id
              type:
                type: string
                description: Data type of the column
                example: INTEGER
              primary_key:
                type: boolean
                description: Whether the column is a primary key
                example: true
              foreign_keys:
                type: array
                items:
                  type: string
                description: List of foreign keys pointing to other tables
                example: ["other_table.id"]
      404:
        description: Model not found
    """
    """
    Get the schema of a specific database model.

    This endpoint retrieves the schema of the specified SQLAlchemy model, including
    column names, types, primary keys, and foreign keys. Useful for dynamically generating forms
    or data tables based on database models in the frontend.
    """
    model_schema: list[dict] = sqlalchemy_utils.get_table_schema(model_name)
    if not model_schema:
        return utils.return_error(f"No model found named {model_name}", 404)
    return utils.return_response(model_schema)
