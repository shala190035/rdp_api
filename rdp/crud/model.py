from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Float, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(
        back_populates="value_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"


class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))

    value_type: Mapped["ValueType"] = relationship(back_populates="values")
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))

    device: Mapped["Device"] = relationship("Device", back_populates="values")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", name="value integrity"),
    )

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r} value_type={self.value_type.type_name!r}, value={self.value})"


class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    devices: Mapped[List["Device"]] = relationship("Device", back_populates="location")

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name}, description={self.description})"


class Device(Base):
    __tablename__ = "device"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    device_type: Mapped[str] = mapped_column()  
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))

    location: Mapped["Location"] = relationship("Location", back_populates="devices")
    values: Mapped[List["Value"]] = relationship("Value", back_populates="device")

    def __repr__(self) -> str:
        return f"Device(id={self.id!r}, name={self.name}, device_type={self.device_type}, location_id={self.location_id})"