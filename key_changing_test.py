import flapi
from change_key import change_key
from time import sleep

flapi.enable()

mixer_track = 1
effect_slot = 0
desired_key = "C#"

sleep(5)
change_key_status = change_key(desired_key, mixer_track, effect_slot)
if not change_key_status:
    print("Something went wrong...")