from config import DEFAULT_PX_PER_METER
def change_meter_to_px(val):
    return val * DEFAULT_PX_PER_METER

def change_px_to_meter(val):
    return val / DEFAULT_PX_PER_METER