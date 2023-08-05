import minimalmodbus
from enum import Enum


class eletricity_meter_type(Enum):
    NONE = 0
    SDM72DM = 1

class eletricity_meter:
    
    address: int = -1
    type: eletricity_meter_type = 0
    
    #to get these addresses from addresses like 30053 remove the first digit and decrease by 1
    values = {
        "current_usage_watts": 53,
        "import_wh_since_last_reset": 72,
        "export_wh_since_last_reset": 74,
        "total_kwh": 342,
        "settable_total_kwh": 384,
        "settable_import_kwh": 388,
        "settable_export_kwh": 390,
        "import_power": 1280,
        "export_power": 1282
    }
    
    def __init__(self, address: int, type: eletricity_meter_type):
        self.address = address
        self.type = type
        

        