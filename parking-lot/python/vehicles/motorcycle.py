from vehicles.vehicle_type import VehicleType
from vehicles.vehicle import Vehicle

class MotorCycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)