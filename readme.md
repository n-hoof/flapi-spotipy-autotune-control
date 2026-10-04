# Autotune Key Automated via Currently Playing Spotify Song

This is a project to automatically change the key of my autotune plugin instance in fl studio based on my currently playing song on spotify.

### Required set up currently:
- FL Studio
- Antares Auto-Tune Artist plugin
- Autotune plugin must be in slot 1 of mixer track 1
- Follow flapi installation set up process from [here](https://github.com/MaddyGuthridge/Flapi)

---

#### Implemented functionality:
- Changing key in autotune from python
- Getting my currently playing spotify song
- Getting the key of the currently playing song via ReccoBeats API
- Control autotune key changing python program via key info gathered from spotify and ReccoBeats API

#### To-Do functionality:
- Get key via JS program using song-finder library, when ReccoBeats API fails to get key



