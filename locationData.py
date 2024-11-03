class Location:
    def __init__(self, name, days, time_slots):
        self.name = name
        self.time = {day : {slot  : 0 for slot in time_slots} for day in days }

