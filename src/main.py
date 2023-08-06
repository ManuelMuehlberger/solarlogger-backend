import e_meter_abstraction as em

def startup():
    meter = em.electricity_meter(2, em.electricity_meter_type.SDM72DM)
    print(meter.read_values())





def lol():
    return "hi"





if __name__ == "__main__":
    startup()