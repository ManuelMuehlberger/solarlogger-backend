import e_meter_abstraction as em
import tomli
import logging
import sys
import sqlite3
import os


class meter_manager:
    
    config: {}
    db = None
    meters = []
    
    def __init__(self, config: {}):
        self.config = config
    
    def log_state(self):
        logging.info("meter_manager State:")
        logging.info(f"Config: {self.config}")
        logging.info(f"Database Connection: {'Connected' if self.db else 'Not Connected'}")
        logging.info(f"Number of Meters: {len(self.meters)}")
        for index, meter in enumerate(self.meters, start=1):
            logging.info(f"Meter {index}: Address {meter.address}, Type {meter.meter_type.name}")

        
    def add_meter(self, meter: em.electricity_meter):
        self.meters.append(meter)

    def add_all_meters(self):
        if self.config == None:
            raise ValueError("No valid configuration found.")
        for meter_name, meter_info in self.config["meters"].items():
            if meter_name.startswith("meter"):
                address = meter_info["address"]
                meter_type = em.electricity_meter_type[meter_info["type"]]
                meter = em.electricity_meter(address, meter_type)
                self.add_meter(meter)

    def read_all_meters(self) -> []:
        all_received_vals = []
        for meter in self.meters:
            received_vals = meter.read_values()
            all_received_vals.append(received_vals)
        return all_received_vals

    def connect_db(self):
        try:
            self.db = sqlite.connect(self.config["database"]["directory"])
            logging.info("Successfully connected to SQLite db at " + self.config["database"]["directory"] + ".")
            if self.is_database_empty():
                logging.info("The database seems to not be initialized yet. Initializing now...")
                self.init_db()
        except Exception as e:
            logging.fatal("Cannot connect to SQLite db at " + self.config["database"]["directory"] + ": " + e)
            sys.exit(1)
            
    def is_database_empty(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return len(tables) == 0
        except Exception as e:
            logging.error("Error checking database status: " + str(e))
            return False


    def init_db(self):
        try:
            if db == None:
                raise ValueError("Db has not been initialized.")
            
            cursor = self.db.cursor()

            # Iterate through meters and create tables
            for meter_name, meter_info in self.config["meters"].items():
                if meter_name.startswith("meter"):
                    meter_address = meter_info["address"]
                    meter_type = meter_info["type"]
                    
                    if meter_type in electricity_meter_lu:
                        meter_table_name = f"meter_{meter_address}"
                        meter_table_definition = ", ".join(
                            [f"{column_name} {data_type}" for column_name, (data_type, _) in electricity_meter_lu[meter_type].items()]
                        )
                        create_table_query = f"CREATE TABLE IF NOT EXISTS {meter_table_name} (timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, {meter_table_definition})"
                        
                        cursor.execute(create_table_query)
                        self.db.commit()
                        logging.info(f"Created table for meter '{meter_name}' with address {meter_address} and type {meter_type}.")
                    else:
                        logging.warning(f"Invalid meter type '{meter_type}' for meter '{meter_name}' with address {meter_address}. Skipping table creation.")
        except Exception as e:
            logging.error(str(e))
            sys.exit(1)        

    def write_data_to_db(self, received_vals: dict):
        try:
            if self.db is None:
                raise ValueError("Db has not been initialized.")
            
            cursor = self.db.cursor()

            for key, value in received_vals.items():
                if key in electricity_meter_lu[0]:
                    column_name, (data_type, _) = key, electricity_meter_lu[0][key]
                    if data_type == 'f':
                        insert_query = f"INSERT INTO meter_{self.address} ({column_name}) VALUES (?)"
                        cursor.execute(insert_query, (value,))
                    elif data_type == 'i':
                        insert_query = f"INSERT INTO meter_{self.address} ({column_name}) VALUES (?)"
                        cursor.execute(insert_query, (value,))
                    else:
                        logging.error(f'Cannot match {data_type} to any data type for column {column_name}. Skipping data insertion.')
            
            self.db.commit()
            logging.info("Inserted data into database.")
        except Exception as e:
            logging.error("Error writing data to database: " + str(e))
            

def parse_config() -> {}:
    config = {}
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
            
            database_directory = config["database"]["directory"]
            if not os.path.exists(database_directory) or not os.access(database_directory, os.R_OK | os.W_OK):
                raise ValueError(general_info + 'Database directory does not exist or is not accessible.')
            
    except tomli.TOMLDecodeError as e:
        logging.fatal('Can not parse TOML config file at ../backend-config.toml.', e)
        sys.exit(1)
    except ValueError as e:
        logging.fatal(e)
        sys.exit(1)
    return config

#def setup():



def startup():
    
    #check config file
    manager = meter_manager(parse_config())
    manager.log_state()

    #connect to meters
    manager.add_all_meters()
    manager.log_state()
    #connect to database
    #if database empty -> setup
    manager.connect_db()
    manager.write_data_to_db(manager.read_all_meters())
    
    #meter = em.electricity_meter(2, em.electricity_meter_type.SDM72DM)
    #print(meter.read_values())

#database architecture:




def lol():
    return "hi"





if __name__ == "__main__":
    startup()