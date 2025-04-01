
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def note_name_to_freq(name):
    map = {
        "c": -9,
        "cs": -8,
        "db": -8,
        "d": -7,
        "ds": -6,
        "eb": -6,
        "e": -5,
        "f": -4,
        "fs": -3,
        "gb": -3,
        "g": -2,
        "gs": -1,
        "ab": -1,
        "a": 0,
        "as": 1,
        "bb": 1,
        "b": 2,
    }
    return map.get(name.lower(), None) # case insensitive, returns None if not found