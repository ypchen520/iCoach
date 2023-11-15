class Task:
    def __init__(self, id=None, name=None, total=0, date=None):
        self.id = id
        self.name = name
        self.total = total
        self.date = date
    def __str__(self):
        pass
        

class Health:
    def __init__(self):
        pass

class Fashion:
    def __init__(self):
        pass

class Clothes:
    def __init__(self, id=None, name=None, date=None, brand=None, color=None, type=None, freq=None):
        self.id
        self.name
        self.date = date
        self.last_time = self.date
        self.brand = brand
        self.color = color
        self.type = type
        self.frequency = freq