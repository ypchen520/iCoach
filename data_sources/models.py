from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

@dataclass
class ResistanceEntry:
    date: Any = datetime.now()
    count: int = 0

@dataclass
class JournalEntry:
    date: date
    mood_before: list[str]
    reflection: str
    mood_after: list[str]

@dataclass
class Item(ABC):
    @abstractmethod
    def read_from_db():
        raise NotImplementedError
    
    @abstractmethod
    def write_to_db():
        raise NotImplementedError

class User:
    id = None

    biceps = None

    @property
    def data(self):
        return {key: value}

    def read_task_from_db(self, db, category, subcategory, task):
        # setattr
        db.collections("users").document(self.id)
        pass
    
    def get_task(category, subcategory, task):
        
        pass

class Productivity:
    pass

class Health:
    cardio = None
    mental = None
    resistance = None
    sport = None
    food = None

class Cardio:
    pass

class Resistance:
    biceps = None
    triceps = None
    deltoids = None
    leg = None
    chest = None
    back = None

class Fashion:
    def __init__(self):
        pass

class Task:
    id = None
    total = None
    date = None
    def __init__(self, id=None, total=0, date=None):
        self.id = id
        self.total = total
        self.date = date
    def __str__(self):
        pass

class Resistance(Item):
    # date: datetime
    # count: int
    def __init__(self, date: datetime, count: int, id: Optional[str] = None):
        self.id = id
        self.date = date
        self.count = count
    
    def read_from_db(self, doc):
        self.id = doc.id
        data = doc.to_dict()
        for key, value in data.items():
            setattr(self, key, value)

    def write_to_db(self, collection_ref=None, data=None, existing=False):
        if not collection_ref:
            raise ValueError("A Firestore collection reference is required")
        if not data:
            raise ValueError("Data is required")
        if existing:
            collection_ref.document(self.id).update(data)

class Clothes(Item):
    id: str
    name: str
    date: datetime
    last_time: datetime
    brand: str
    color: str
    type: str
    frequency: int
    location: dict
    # status = None
    madein: str
    count: int
    owned: int # how many years have I owned this item
    washed: int
    def __init__(self, id=None, name=None, date=None, brand=None, color=None, type=None, freq=None, location=None):
        pass
        # self.id
        # self.name
        # self.date = date
        # self.last_time = self.date
        # self.brand = brand
        # self.color = color
        # self.type = type
        # self.frequency = freq
    def read_from_db(self, doc):
        self.id = doc.id
        data = doc.to_dict()
        for key, value in data.items():
            setattr(self, key, value)

    def write_to_db(self, collection_ref=None, data=None, existing=False):
        if not collection_ref:
            raise ValueError("A Firestore collection reference is required")
        if not data:
            raise ValueError("Data is required")
        if existing:
            collection_ref.document(self.id).update(data)