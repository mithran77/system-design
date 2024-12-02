from threading import Lock
import uuid
from reservation import Reservation
from credit_card_payment_processor import CreditCardPaymentProcessor

class RentalSystem:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.cars = {}
                cls._instance.reservations = {}
                cls._instance.payment_processor = CreditCardPaymentProcessor()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def add_car(self, car):
        self.cars[car.get_license_plate()] = car

    def remove_car(self, car):
        car = self.cars.get(car.get_license_plate(), None)
        if car:
            self.cars.pop(car.get_license_plate())

    def search_cars(self, make, model, start_date, end_date):
        found_cars = []
        for car in self.cars.values():
            if (car.get_make().lower() == make.lower() and car.get_model().lower() == model.lower() and car.is_available()):
                if self.is_car_available(car, start_date, end_date):
                    found_cars.append(car)

        return found_cars

    def is_car_available(self, car, start_date, end_date):
        for reservation in self.reservations.values():
            if reservation.get_car() == car:
                if start_date < reservation.get_end_date and end_date > reservation.get_start_date():
                    return False
        return True

    def make_reservation(self, customer, car, start_date, end_date):
        if car.is_available():
            reservation_id = self.generate_reservation_id()
            reservation = Reservation(reservation_id, customer, car, start_date, end_date)
            car.set_available(False)
            self.reservations[reservation_id] = reservation
            return reservation
        return None
    
    def cancel_reservation(self, reservation_id):
        reservation = self.reservations.pop(reservation_id, None)
        if reservation is not None:
            reservation.get_car().set_available(True)
    
    def process_payment(self, reservation):
        return self.payment_processor.process_payment(reservation.get_total_price())

    def generate_reservation_id(self):
        return "RES" + str(uuid.uuid4())[:8].upper()
