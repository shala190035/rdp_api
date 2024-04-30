import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_delete_value_by_id(database_session):
    # Pass the engine, not the session, to the Crud constructor
    crud = Crud(engine)
    
    # Add some test values to the database
    crud.add_value(value_time=123456, value_type=1, value_value=10.0, device_id=1)
    crud.add_value(value_time=123457, value_type=1, value_value=20.0, device_id=1)
    crud.add_value(value_time=123458, value_type=1, value_value=30.0, device_id=1)
    
    # Get the IDs of the values
    values = crud.get_values()
    value_ids = [value.id for value in values]
    
    # Delete one of the values by ID
    value_to_delete_id = value_ids[0]
    assert crud.delete_by_id(value_to_delete_id) == True
    
    # Check if the value was deleted
    remaining_values = crud.get_values()
    remaining_value_ids = [value.id for value in remaining_values]

    assert value_to_delete_id not in remaining_value_ids
