from datetime import datetime
import random

def __uniqueid__():
    mynow = datetime.now
    sft = datetime.strftime
    old_time = mynow()
    seed_range_bits = 14 # max range for seed
    seed_max_value = 2**seed_range_bits - 1 # seed could not exceed 2**nbbits - 1
    # get random seed
    seed = random.getrandbits(seed_range_bits)
    current_seed = str(seed)
    # producing new ids
    while True:
        # get current time 
        current_time=mynow()
        if current_time <= old_time:
            # previous id generated in the same microsecond or Daylight
            # saving time event occurs (when clocks are adjusted backward)
            seed = max(1,(seed + 1) % seed_max_value)
            current_seed = str(seed)
        # generate new id (concatenate seed and timestamp as numbers)
        #newid=hex(int(''.join([sft(current_time,'%f%S%M%H%d%m%Y'),current_seed])))[2:-1]
        newid=''.join([sft(current_time, '%f%S%M%H%d%m%Y'), current_seed])
        # save current time
        old_time=current_time
        # return a new id
        yield newid

""" you get a new id for each call of uniqueid() """
uniqueid = __uniqueid__().next