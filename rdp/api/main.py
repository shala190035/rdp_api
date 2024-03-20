from typing import Union, List, Optional

from fastapi import FastAPI, HTTPException, Query

from rdp.sensor import Reader
from rdp.crud import create_engine, Crud
from . import api_types as ApiTypes
import logging

logger = logging.getLogger("rdp.api")
app = FastAPI()

@app.get("/")
def read_root() -> ApiTypes.ApiDescription:
    """This url returns a simple description of the api

    Returns:
        ApiTypes.ApiDescription: the Api description in json format 
    """    
    return ApiTypes.ApiDescription()

@app.get("/type/")
def read_types() -> List[ApiTypes.ValueType]:
    """Implements the get of all value types

    Returns:
        List[ApiTypes.ValueType]: list of available valuetypes. 
    """    
    global crud
    return crud.get_value_types()

@app.get("/type/{id}/")
def read_type(id: int) -> ApiTypes.ValueType:
    """returns an explicit value type identified by id

    Args:
        id (int): primary key of the desired value type

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ApiTypes.ValueType: the desired value type 
    """
    global crud
    try:
         return crud.get_value_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 
    return value_type 

@app.put("/type/{id}/")
def put_type(id, value_type: ApiTypes.ValueTypeNoID) -> ApiTypes.ValueType:
    """PUT request to a special valuetype. This api call is used to change a value type object.

    Args:
        id (int): primary key of the requested value type
        value_type (ApiTypes.ValueTypeNoID): json object representing the new state of the value type. 

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed 

    Returns:
        ApiTypes.ValueType: the requested value type after persisted in the database. 
    """
    global crud
    try:
        crud.add_or_update_value_type(id, value_type_name=value_type.type_name, value_type_unit=value_type.type_unit)
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/value/")
def get_values(type_id:int=None, start:int=None, end:int=None) -> List[ApiTypes.Value]:
    """Get values from the database. The default is to return all available values. This result can be filtered.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        List[ApiTypes.Value]: _description_
    """
    global crud
    try:
        values = crud.get_values(type_id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")

@app.on_event("startup")
async def startup_event() -> None:
    """start the character device reader
    """    
    logger.info("STARTUP: Sensor reader!")
    global reader, crud
    engine = create_engine("sqlite:///rdb.test.db")
    crud = Crud(engine)
    reader = Reader(crud)
    reader.start()
    logger.debug("STARTUP: Sensor reader completed!")

@app.on_event("shutdown")
async def shutdown_event():
    """stop the character device reader
    """    
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")

@app.post("/device/")
def create_device(device: ApiTypes.DeviceCreate, location_id: int) -> ApiTypes.Device:
    global crud
    created_device = crud.add_device(name=device.name, device_type=device.device_type, location_id=location_id)
    return ApiTypes.Device(id=created_device.id, name=created_device.name, device_type=created_device.device_type, location_id=created_device.location_id)


@app.get("/devices/", response_model=List[ApiTypes.Device])
def read_all_devices():
    """Endpoint to retrieve all registered devices.

    Returns:
        List[ApiTypes.Device]: A list of all devices.
    """
    devices = crud.get_all_devices()
    return devices

@app.get("/values/by-device/", response_model=List[ApiTypes.Value])
def read_values_by_device(device_id: Optional[int] = None, device_name: Optional[str] = None):
    if device_id is None and device_name is None:
        raise HTTPException(status_code=400, detail="Either device_id or device_name must be provided")
    try:
        values = crud.get_values_by_device(device_id=device_id, device_name=device_name)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Device not found or no values for this device")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/location/")
def create_location(location: ApiTypes.LocationCreate) -> ApiTypes.Location:
    """Endpoint zum Erstellen einer neuen Location.

    Args:
        location (ApiTypes.LocationCreate): Das Location-Objekt, das erstellt werden soll.

    Returns:
        ApiTypes.Location: Das erstellte Location-Objekt.
    """
    global crud
    created_location = crud.add_location(name=location.name, description=location.description)
    return ApiTypes.Location(id=created_location.id, name=created_location.name, description=created_location.description)

@app.get("/locations/", response_model=List[ApiTypes.Location])
def read_all_locations():
    """Endpoint, um alle Locations abzurufen.

    Returns:
        List[ApiTypes.Location]: Eine Liste aller Locations.
    """
    global crud
    locations = crud.get_all_locations()
    return locations