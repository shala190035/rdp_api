import datetime
from typing import Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError, StatementError

from rdp.crud.crud import Crud
from rdp.crud.model import Value

def test_delete_value_by_id(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, _ = crud_session_in_memory
    
    # Add some test values to the database
    crud_in_memory.add_value(value_time=123456, value_type=1, value_value=10.0, device_id=1)
    crud_in_memory.add_value(value_time=123457, value_type=1, value_value=20.0, device_id=1)
    crud_in_memory.add_value(value_time=123458, value_type=1, value_value=30.0, device_id=1)
    
    # Get the IDs of the values
    values = crud_in_memory.get_values()
    value_ids = [value.id for value in values]
    
    # Delete one of the values by ID
    value_to_delete_id = value_ids[0]
    assert len(values) == 3
    crud_in_memory.delete_by_id(value_to_delete_id)
    
    # Check if the value was deleted
    remaining_values = crud_in_memory.get_values()
    remaining_value_ids = [value.id for value in remaining_values]

    assert value_to_delete_id not in remaining_value_ids
