import minimalmodbus
import logging
import traceback
from enum import Enum


class electricity_meter_type(Enum):
    SDM72DM = 0
    
    

electricity_meter_lu = {
    0: {
            "current_usage_watts": ('f', 52),
            "import_wh_since_last_reset": ('f', 72),
            "export_wh_since_last_reset": ('f', 74),
            "total_kwh": ('f', 342),
            "settable_total_kwh": ('f', 384),
            "settable_import_kwh": ('f', 388),
            "settable_export_kwh": ('f', 390),
            "import_power": ('f', 1280),
            "export_power": ('f', 1282)
        }
}
#to get the actual register from addresses like 30053 remove the first digit and decrease by 1



class electricity_meter:
    
    address: int = -1
    meter_type: electricity_meter_type = None
    bridge: minimalmodbus.Instrument = None
    
    def __init__(self, address: int, meter_type: electricity_meter_type):
        if address < 1:
            raise ValueError('addresses can only be > 0.')
        self.address = address
        self.meter_type = meter_type
        self.connect()
        
    def connect(self):
        try:
            self.bridge = minimalmodbus.Instrument('/dev/ttyACM0', self.address)
        except IOError as e:
            logging.exception('Cannot connect to meter.', e)
    
    def read_values(self) -> {}:
        if self.bridge == None:
            logging.fatal('Can not read from meter that was not initialized!')
            return {}
        received_vals = {}
        try:
            for key, (data_type, data_address) in electricity_meter_lu[self.meter_type.value].items():
                if data_type == 'f':
                    received_vals[key] = self.bridge.read_float(data_address, 4)
                elif data_type == 'i':
                    received_vals[key] = self.bridge.read_register(data_address, 4)
                else:
                    logging.error('Cannot match', data_type, 'to any data type in argument', key + 'in', self.meter_type, '.')
            print(received_vals)
        except IOError as e:
            logging.exception('Cannot read from meter.', e)
        finally:
            return received_vals