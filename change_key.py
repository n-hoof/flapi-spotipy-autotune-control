import plugins

KEY_PARAM_VAL = 2

KEY_VALUES = {
    "C": 0,
    "Db": 0.09,
    "D": 0.18,
    "Eb": 0.27,
    "E": 0.36,
    "F": 0.45,
    "Gb": 0.54,
    "G": 0.63,
    "Ab": 0.72,
    "A": 0.81,
    "Bb": 0.9,
    "B": 1
}

def change_key(desired_key: str, mixer_track: int, effect_slot: int) -> bool:
    if desired_key not in KEY_VALUES:
        print(f"{desired_key} is not an acceptable key")
        return False
    key_val = KEY_VALUES[desired_key]
    
    #This check should be ran outside this function, but I just put it here for now.
    #Should be included at the start of the program
    if not plugins.isValid(mixer_track, effect_slot):
        print(f"No valid plugin found on track: {mixer_track}, in slot: {effect_slot}")
        return False

    try:
        plugins.setParamValue(key_val, KEY_PARAM_VAL, mixer_track, effect_slot)
    except:
        print(f"Key was not abled to be changed to {desired_key}")

    print(f"Key changed to: {desired_key}")
    return True

