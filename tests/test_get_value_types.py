import datetime
from typing import Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError, StatementError

from rdp.crud.crud import Crud
from rdp.crud.model import Value

def test_get_values(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    crud_in_memory.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit", )
    crud_in_memory.add_value(value_time=123456, value_type=1, value_value=42.0, device_id=1)
    

    values = crud_in_memory.get_values(value_type_id=1)

    assert len(values) == 1
    assert values[0].time == 123456
    assert values[0].value == 42.0
