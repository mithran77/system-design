from abc import ABC
from vehicles.vehicle_type import VehicleType

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

    # def get_license_plate(self) -> str:
    #     return self.license_plate

    def get_type(self) -> VehicleType:
        return self.type
