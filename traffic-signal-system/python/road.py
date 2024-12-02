class Road:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.traffic_light = None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_traffic_light(self):
        return self.traffic_light

    def set_traffic_light(self, traffic_light):
        self.traffic_light = traffic_light
