import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_delete_by_time(database_session):
    # Pass the engine, not the session, to the Crud constructor
    crud = Crud(engine)
    crud.add_value(value_time=123456, value_type=1, value_value=42.0, device_id=2)
    crud.add_value(value_time=123457, value_type=1, value_value=42.0, device_id=2)
    crud.add_value(value_time=123458, value_type=1, value_value=42.0, device_id=2)

    timestamp_to_delete = 123457
    
    crud.delete_by_time(timestamp_to_delete)
    
    remaining_values = crud.get_values()
    for value in remaining_values:
        assert value.time != timestamp_to_delete
