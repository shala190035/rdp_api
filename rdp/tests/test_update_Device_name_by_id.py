import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_update_device_name_by_id(database_session):
    crud = Crud(engine)
    device_id = crud.add_device(name="Test Device", device_type="Test Type", location_id=1).id
    device = crud.get_device_by_id(device_id)[0]
    new_device_name = "Updated Device Name"
    crud.update_Device_name_by_id(device_id, new_device_name)
    updated_device = crud.get_device_by_id(device_id)[0]
    
    assert device.name == "Test Device"
    assert updated_device.name == new_device_name