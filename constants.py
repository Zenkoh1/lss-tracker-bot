from enum import Enum

import pytz

#keys
EQUIPMENT = 'Equipment'
LAST_CHANGED_TIME = 'last_changed_time'
LAST_CHANGED_NAME = 'last_changed_name'
AIRCRAFT = 'Aircraft'

#other constants
# TIMEZONE = pytz.timezone('Asia/Singapore')


class RawTextType(Enum):
    NEW_AIRCRAFT = 1
    NEW_EQUIPMENT = 2
    ADD_EQUIPMENT = 3
    REMOVE_EQUIPMENT = 4
    AIRCRAFT_INFO = 5
    EQUIPMENT_INFO = 6
    DELETE_AIRCRAFT = 7
    DELETE_EQUIPMENT = 8
    