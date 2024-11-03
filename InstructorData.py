class Instructor:
    def __init__(self, name, days, time_slots):
        self.name = name
        #self.role = role
        self.time = {day : {slot  : 0 for slot in time_slots} for day in days }
        self.load = {}
