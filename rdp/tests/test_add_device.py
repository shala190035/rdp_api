import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_add_device(database_session):
    crud = Crud(engine)
    crud.add_device(name="Test Device", device_type="Test Type", location_id=1)
    devices = crud.get_all_devices()
    assert len(devices) == 1
    assert devices[0].name == "Test Device"
