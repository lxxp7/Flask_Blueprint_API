"""SQLAlchemy utils module containing all functions making operations using the database."""
from typing import Any, Dict, Optional, Type, TypeVar

from sqlalchemy.inspection import inspect

from Flask_API import utils
from Flask_API.db import db

T = TypeVar('T')


def create_record(model: Type[T], data: Dict[str, Any]) -> bool:
    """
    Insert a new record into the database with validation for foreign keys.

    Args:
        model (Type[T]): The SQLAlchemy model class to insert into.
        data (Dict[str, Any]): A dictionary containing the data for the new record.

    Returns:
        bool: True if the insert is a success, else False
    """
    # Extract primary keys from the model
    primary_keys = [key.name for key in inspect(model).primary_key]
    filter_criteria = {key: data.get(key) for key in primary_keys if key in data}

    if not filter_criteria:
        utils.log_warning(f"No primary key provided in data for model : {model.__tablename__} : {data}")
        return False

    # Validate foreign key references
    fk_validation_errors = validate_foreign_key_references(model, data)
    if fk_validation_errors:
        utils.log_warning(f"Foreign key validation failed: {fk_validation_errors}")
        return False

    # Check if the record exists based on primary keys
    existing_record = get_record_by_key(model, filter_criteria)
    if existing_record:
        utils.log_warning(f"Record with primary key(s) {filter_criteria} already exists")
        return False
    try:
        # Create and insert the new record
        new_record = model(**data)
        db.session.add(new_record)
        db.session.commit()
        utils.log_info(f"Data successfully created : {record_as_dict(new_record)}")
        return True

    except Exception as e:
        db.session.rollback()
        utils.log_error(f"Error inserting data: {str(e)}")
        return False


def update_record(model: Type[T], data: Dict[str, Any]) -> bool:
    """
    Update an existing record in the database with validation for foreign keys.

    Args:
        model (Type[T]): The SQLAlchemy model class to update.
        data (Dict[str, Any]): A dictionary containing primary key(s) and updated field values.

    Returns:
        bool: True if the update is a success, else False
    """
    # Extract primary keys from the model
    primary_keys = [key.name for key in inspect(model).primary_key]
    filter_criteria = {key: data.get(key) for key in primary_keys if key in data}

    if not filter_criteria:
        utils.log_warning(f"No primary key provided in data : {data}")
        return False

    # Find the existing record
    record = get_record_by_key(model, filter_criteria)
    if not record:
        utils.log_warning(f"Record with primary key(s) {filter_criteria} not found")
        return False

    # Validate foreign key references for update
    fk_validation_errors = validate_foreign_key_references(model, data)
    if fk_validation_errors:
        utils.log_warning(f"Foreign key validation failed: {fk_validation_errors}")
        return False

    # Update fields
    for key, value in data.items():
        if key not in primary_keys:  # Avoid modifying primary keys
            setattr(record, key, value)
    try:
        db.session.commit()
        utils.log_info(f"Update successful of : {record_as_dict(record)}")
        return True
    except Exception as e:
        db.session.rollback()
        utils.log_error(f"Error updating record {record_as_dict(record)}: {str(e)}")
        return False


def delete_record(model: Type[T], primary_key_values: Dict[str, Any]) -> bool:
    """
    Delete a record from the database based on its primary key(s).

    Args:
        model (Type[T]): The SQLAlchemy model class.
        primary_key_values (Dict[str, Any]): A dictionary where keys are primary key column names
                                             and values are their corresponding values.

    Returns:
        bool: True if the deletion is a success, else False
    """
    record = get_record_by_key(model, primary_key_values)
    if not record:
        utils.log_warning(f"Record with primary key(s) {primary_key_values} not found")
        return False

    db.session.delete(record)
    db.session.commit()
    utils.log_info(f"Deletion successful of : {record_as_dict(record)}")
    return True


def get_record_by_key(model: Type[T], key_value_dict: dict) -> Optional[T]:
    """
    Retrieve a single record from the database that matches the given key-value filters.

    Args:
        model (Type[T]): The SQLAlchemy model class to query.
        key_value_dict (dict): A dictionary where keys are column names and values are the corresponding
                               values to filter the record by.

    Returns:
        Optional[T]: The first matching record if found, otherwise None.
    """
    return db.session.query(model).filter_by(**key_value_dict).first()


def get_records_by_key(model: Type[T], key_value_dict: dict) -> list[T]:
    """
    Retrieve multiple records from the database that match the given key-value filters.

    Args:
        model (Type[T]): The SQLAlchemy model class to query.
        key_value_dict (dict): A dictionary where keys are column names and values are the corresponding
                               values to filter records by.

    Returns:
        list[T]: A list of records matching the criteria, or an empty list if no records are found.
    """
    return db.session.query(model).filter_by(**key_value_dict).all()


def get_model_foreign_keys(model_name: str) -> Dict[str, Dict[str, list[str]]]:
    """
    Retrieve all foreign key relationships for a specific model from the database.

    This function inspects the database schema and returns a dictionary containing
    foreign key relationships for the specified table.

    Args:
        model_name (str): The name of the model/table to inspect

    Returns:
        Dict[str, list[str]]: A dictionary where:
            - Keys are referenced table names
            - Values are lists of referenced column names

    Example:
        {
            'users': ['user_id'],
            'projects': ['project_id'],
        }
    """
    # Get database inspector
    inspector = inspect(db.engine)
    # Get foreign keys for the current table
    fks = inspector.get_foreign_keys(table_name=model_name)
    fks_dict = {}

    # Process each foreign key definition
    for fk_data in fks:
        if "referred_table" in fk_data and "referred_columns" in fk_data:
            fks_dict[fk_data["referred_table"]] = fk_data["referred_columns"]

    return fks_dict


def validate_foreign_key_references(model: Type[T], data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate that foreign key references exist before inserting or updating a record.

    Args:
        model (Type[T]): The SQLAlchemy model class to validate against.
        data (Dict[str, Any]): The dictionary containing the data to be validated.

    Returns:
        Dict[str, str]: A dictionary of validation errors, where keys are the invalid foreign key fields
                        and values are error messages. Returns an empty dictionary if all references are valid.
    """
    validation_errors = {}
    try:
        model_fk_dict = get_model_foreign_keys(model.__name__)

        # Loop through each foreign key column to see if it is in data
        for ref_model, fk_cols_list in model_fk_dict.items():
            for fk_column in fk_cols_list:
                if fk_column not in data:
                    continue

                # Get the value provided for this foreign key and the model class to see if the record exists
                fk_value = data[fk_column]
                model_class = get_class_from_tablename(ref_model)

                existing_record = get_record_by_key(model_class, {fk_column: fk_value})
                if not existing_record:
                    validation_errors[fk_column] = f'Could not find {fk_column} value for {fk_value} in {ref_model}'
    except Exception as e:
        validation_errors["foreign_key_validation"] = f"Error validating foreign keys for model {model.__name__}: {str(e)}"

    return validation_errors


def get_class_from_tablename(tablename: str) -> Optional[Type[T]]:
    """
    Sqlalchemy utility function to retrieve a Model class from its table_name.

    Args:
        tablename (str): The name of the database table to search for

    Returns:
        db.Model: The SQLAlchemy model class corresponding to the table name,
                 or None if no matching model is found

    Raises:
        TypeError: If tablename is not a string or not found
    """
    if not isinstance(tablename, str):
        raise TypeError("Tablename must be a string")
    try:
        for model_class in db.Model.__subclasses__():
            name = getattr(model_class, '__tablename__', '')
            if name.lower() == tablename.lower():
                return model_class
    except Exception as e:
        utils.log_error(f"Failed to retrieve a class from the tablename: {str(e)}")
    return None


def record_as_dict(record) -> dict:
    """
    Sqlalchemy utility function to convert a database record to a dictionary.

    Args:
        record (db.Record): A SQLAlchemy record retrieved from the database

    Returns:
        dict: A dictionary containing column names as keys and record values as values

    Raises:
        RuntimeError: if a record to dict fails
    """
    if record is None:
        utils.log_warning(f"No record given to convert to dictionary")
        return {}
    try:
        return {c.name: getattr(record, c.name) for c in record.__table__.columns}
    except Exception as e:
        utils.log_error(f"Failed to convert record to dictionary: {str(e)}")
        return {}


def get_table_schema(model_name):
    """
    Returns the schema of the specified database model.

    Args:
        model_name (str): the model name to get schema for.

    Returns:
        list[dict]: the list of the shema of each column of a table, contains {foreign_keys: list, name: str, primary_key: bool, type: str}
    """
    model_class = get_class_from_tablename(model_name)
    if not model_class:
        return None

    mapper = inspect(model_class)

    schema = []
    for column in mapper.columns:
        col_info = {
            "name": column.name,
            "type": str(column.type),
            "primary_key": column.primary_key,
            "foreign_keys": [str(fk.target_fullname) for fk in column.foreign_keys]
        }
        schema.append(col_info)

    return schema