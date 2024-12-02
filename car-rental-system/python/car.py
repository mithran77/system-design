class Car:
    def __init__(self, make, model, year, license_plate, rental_price_per_day):
        self.make = make
        self.model = model
        self.year = year
        self.license_plate = license_plate
        self.rental_price_per_day = rental_price_per_day
        self.available = True

    def get_make(self):
        return self.make

    def get_model(self):
        return self.model

    def get_year(self):
        return self.year

    def get_license_plate(self):
        return self.license_plate

    def get_rental_price_per_day(self):
        return self.rental_price_per_day

    def is_available(self):
        return self.available

    def set_available(self, value):
        self.available = value
