import e_meter_abstraction as em
import tomli
import logging
import sys


config = {}

def parse_config():
    try:
        with open("backend-config.toml", "rb") as f:
            config = tomli.load(f)
                
            #-polling frequency needs to be >= 0
            #-meter names need to be unique
            #-meter addresses need to be unique && > 0
            #-meter type needs to exist
            general_info: str = 'In config file at ../backend-config.toml:\n'

            if config["meters"]["pollingfrequency"] < 0:
                raise ValueError( general_info, 'Polling frequency needs to be >= 0')
            
            
            
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