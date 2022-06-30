class Switch:
    def __init__(self, wafer='', sector='', switch_id='', r_on=0, r_off=0, threshold=0):
        self.id = switch_id
        self.wafer = wafer
        self.sector = sector
        self.r_on = r_on
        self.r_off = r_off
        self.threshold = threshold
