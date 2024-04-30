import datetime
from typing import Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError, StatementError

from rdp.crud.crud import Crud
from rdp.crud.model import Value

def test_update_device_name(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory
    device_id = crud_in_memory.add_device(name="test", device_type="test", location_id=1).id
    device = crud_in_memory.get_device_by_id(device_id)
    assert device[0].name == "test"
    new_name ="test2"
    crud_in_memory.update_Device_name_by_id(device_id, new_name)
    updated_device = crud_in_memory.get_device_by_id(device_id)
    assert updated_device[0].name == new_name
