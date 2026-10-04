import plugins
import flapi

KEY_PARAM_INDEX = 2
SCALE_PARAM_INDEX = 3
MIXER_TRACK = 1
EFFECT_SLOT = 0
AUTOTUNE_PLUGIN_NAME = "Auto-Tune Artist"
KEY_PARAM_NAME = "Key"
SCALE_PARAM_NAME = "Scale"
SCALE_VALUE_MAJOR = 0

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

def check_autotune() -> bool:
    if not plugins.isValid(MIXER_TRACK, EFFECT_SLOT):
        print(f"No valid plugin found on track: {MIXER_TRACK}, in slot: {EFFECT_SLOT}")
        return False
    
    plugin_name = plugins.getPluginName(MIXER_TRACK, EFFECT_SLOT)

    if plugin_name != AUTOTUNE_PLUGIN_NAME:
        print(f"Error, Expected plugin: '{AUTOTUNE_PLUGIN_NAME}'\nFound plugin: '{plugin_name}'")
        return False

    return True

def check_key_param() -> bool:
    param_name = plugins.getParamName(KEY_PARAM_INDEX, MIXER_TRACK, EFFECT_SLOT)

    if param_name != KEY_PARAM_NAME:
        print(f"'{KEY_PARAM_NAME}' parameter not found at expected index: {KEY_PARAM_INDEX}\nFound parameter '{param_name}' instead")
        return False
    
    return True

def check_scale_param() -> bool:
    param_name = plugins.getParamName(SCALE_PARAM_INDEX, MIXER_TRACK, EFFECT_SLOT)

    if param_name != SCALE_PARAM_NAME:
        print(f"'{SCALE_PARAM_NAME}' parameter not found at expected index: {SCALE_PARAM_INDEX}\nFound parameter '{param_name}' instead")
        return False
    
    return True

def check_setup() -> bool:
    if check_autotune():
        if check_key_param():
            return check_scale_param()

    return False

def set_scale_to_major():
    try:
        plugins.setParamValue(SCALE_VALUE_MAJOR, SCALE_PARAM_INDEX, MIXER_TRACK, EFFECT_SLOT)
    except:
        print(f"Scale was not able to be changed to major")


def get_key_val(desired_key: str) -> float | None:
    if desired_key not in KEY_VALUES:
        print(f"{desired_key} is not an acceptable key")
        return
    
    return KEY_VALUES[desired_key]

def change_key(desired_key: str):
    
    key_val = get_key_val(desired_key)

    if key_val is not None:
        try:
            plugins.setParamValue(key_val, KEY_PARAM_INDEX, MIXER_TRACK, EFFECT_SLOT)
            print(f"Key was changed to: {desired_key}")
        except:
            print(f"Key was not able to be changed to {desired_key}")


def set_up_flapi_connection() -> bool:
    try:
        flapi.enable()
        if check_setup():
            set_scale_to_major()
            return True
        else:
            return False

    except:
        print("Connection to FL studio was unsuccesful...")
        return False


