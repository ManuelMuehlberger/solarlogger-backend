import e_meter_abstraction as em
import tomli
import logging
import sys


config = {}

def parse_config():
    try:
        with open("backend-config.toml", "rb") as f:
            config = tomli.load(f)
                
            general_info: str = 'In config file at ../backend-config.toml: '

            #-polling frequency needs to be >= 0
            if config["meters"]["pollingfrequency"] < 0:
                raise ValueError(general_info, 'Polling frequency needs to be >= 0')
            
            #-meter names need to be unique
            meters_dict = {key: value for key, value in config["meters"].items() if isinstance(value, dict)}
            meter_names = set(meters_dict.keys())
            if len(meter_names) < len(meters_dict):
                raise ValueError(general_info + 'Electricity meter names have to be unique.')
            
            #-meter addresses need to be unique, > 0 and < 248
            address_set = set()
            for value in meters_dict.values():
                if isinstance(value, dict) and 'address' in value:
                    address = value['address']
                    if address in address_set:
                        raise ValueError(general_info + 'Electricity meter addresses have to be unique.')
                    elif address <= 0 or address >= 248:
                        raise ValueError(general_info + 'Electricity meter addresses need to be > 0 and < 248.')
                    address_set.add(address)
                    
            #-meter type needs to exist
            meter_names = {member.name for member in em.electricity_meter_type}
            invalid_types = {value['type'] for value in meters_dict.values() if isinstance(value, dict) and 'type' in value and value['type'] not in meter_names}
            if invalid_types:
                raise ValueError(general_info + 'Electricity meter types need to be any of: "' + '", "'.join(meter_names) + '".')
            
    except tomli.TOMLDecodeError as e:
        logging.fatal('Can not parse TOML config file at ../backend-config.toml.', e)
        sys.exit(1)
    except ValueError as e:
        logging.fatal(e)
        sys.exit(1)



def startup():
    
    #check config file
    parse_config()
    
    #connect to meters
    
    #connect to database
    
    
    #meter = em.electricity_meter(2, em.electricity_meter_type.SDM72DM)
    #print(meter.read_values())

#database architecture:




def lol():
    return "hi"





if __name__ == "__main__":
    startup()