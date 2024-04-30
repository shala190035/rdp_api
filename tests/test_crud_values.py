import datetime
from typing import Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError, StatementError

from rdp.crud.crud import Crud
from rdp.crud.model import Value

def test_add_value_invalid(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, _ = crud_session_in_memory

    with pytest.raises(InterfaceError):
        crud_in_memory.add_value([], 1, 76,1)

    with pytest.raises(StatementError):
        crud_in_memory.add_value(0, 1, "test",1)

    with pytest.raises(TypeError):
        crud_in_memory.add_value(0, "test", 76,1)

def test_add_value(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    crud_in_memory.add_or_update_value_type(value_type_id=0, value_type_name="iq", value_type_unit="")
    crud_in_memory.add_or_update_value_type(value_type_id=1, value_type_name="weigth", value_type_unit="kg")
    crud_in_memory.add_or_update_value_type(value_type_id=2, value_type_name="size", value_type_unit="cm")

    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 1, 76,1)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 2, 180,1)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 0, 105,1)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()), 1, 77,1)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()), 2, 181,1)

    with session() as s:
        stmt = select(Value)
        result = s.scalars(stmt).all()
        assert result != None
        assert len(result) == 5
        for value_type in result:
            assert isinstance(value_type, Value)
            assert value_type.id >= 0 and value_type.id <= 5
            assert value_type.value in [76, 180, 105, 77, 181]
            assert value_type.time in [
                datetime.datetime(year=2023, month=9, day=26, second=1).timestamp(),
                datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()
            ]
