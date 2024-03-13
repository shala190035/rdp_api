from pydantic import BaseModel


# Vorhandene Modelle
class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str


class ValueType(ValueTypeNoID):
    id: int


class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float
    device_id: int


class Value(ValueNoID):
    id: int


class ApiDescription(BaseModel):
    description: str = "This is the Api"
    value_type_link: str = "/type"
    value_link: str = "/value"


# Neue Modelle für Geräte
class DeviceCreate(BaseModel):
    name: str
    device_type: str


class Device(DeviceCreate):
    id: int
