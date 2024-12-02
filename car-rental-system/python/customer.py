class Customer:
    def __init__(self, name, contact_info, drivers_license_number):
        self.name = name
        self.contact_info = contact_info
        self.drivers_license_number = drivers_license_number

    def get_name(self):
        return self.name

    def get_contact_info(self):
        return self.contact_info

    def get_drivers_license_number(self):
        return self.drivers_license_number
