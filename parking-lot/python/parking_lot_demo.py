from parking_lot import ParkingLot
from level import Level
from vehicles.car import Car
from vehicles.motorcycle import MotorCycle
from vehicles.truck import Truck

class ParkingLotDemo:
    def run():
        parking_lot = ParkingLot.get_instance()
        parking_lot.add_level(Level(1, 10))
        parking_lot.add_level(Level(2, 12))

        motorcycle = MotorCycle("M1234")
        car = Car("C3456")
        truck = Truck("T09808")


        parking_lot.park_vehicle(car)
        parking_lot.park_vehicle(motorcycle)
        parking_lot.park_vehicle(truck)
        
        parking_lot.display_availability()
        
        parking_lot.unpark_vehicle(car)
        
        parking_lot.display_availability()

if __name__ == "__main__":
    ParkingLotDemo.run()
