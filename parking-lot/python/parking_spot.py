from constants.vehicle_type import VehicleType
from vehicle.vehicle import Vehicle

class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type = None):
        self.spot_number = spot_number
        # default CAR
        self.vehicle_type = VehicleType.CAR if vehicle_type is None else vehicle_type
        self.parked_vehicle = None

    def is_available(self):
        return self.parked_vehicle is None

    def park_vehicle(self, vehicle: Vehicle):
        if self.is_available() and self.get_vehicle_type() == vehicle.get_type():
            self.parked_vehicle = vehicle
        else:
            raise ValueError("Parking spot is occupied or incorrect vehicle type")

    def unpark_vehicle(self):
        self.parked_vehicle = None

    def get_spot_number(self):
        return self.spot_number

    def get_vehicle_type(self):
        return self.vehicle_type

    def get_parked_vehicle(self):
        return self.parked_vehicle
