# proof of concept of piano keys being played
#

# setup sound assets
define pkey.C4 = "mod_assets/sounds/piano_keys/C4.ogg"
define pkey.C4sh = "mod_assets/sounds/piano_keys/C4sh.ogg"
define pkey.D4 = "mod_assets/sounds/piano_keys/D4.ogg"
define pkey.D4sh = "mod_assets/sounds/piano_keys/D4sh.ogg"
define pkey.E4 = "mod_assets/sounds/piano_keys/E4.ogg"
define pkey.F4 = "mod_assets/sounds/piano_keys/F4.ogg"
define pkey.F4sh = "mod_assets/sounds/piano_keys/F4sh.ogg"
define pkey.G4 = "mod_assets/sounds/piano_keys/G4.ogg"
define pkey.G4sh = "mod_assets/sounds/piano_keys/G4sh.ogg"
define pkey.A4 = "mod_assets/sounds/piano_keys/A4.ogg"
define pkey.A4sh = "mod_assets/sounds/piano_keys/A4sh.ogg"
define pkey.B4 = "mod_assets/sounds/piano_keys/B4.ogg"
define pkey.C5 = "mod_assets/sounds/piano_keys/C5.ogg"

screen piano_keys():
    $ import store.pkey as pkey
    modal True
    
    # quit action
    key "q" action Return()

    # alright time to do key things
    key "c" action Play("audio",pkey.C4)
    key "f" action Play("audio",pkey.C4sh)
    key "v" action Play("audio",pkey.D4)
    key "g" action Play("audio",pkey.D4sh)
    key "b" action Play("audio",pkey.E4)
    key "n" action Play("audio",pkey.F4)
    key "j" action Play("audio",pkey.F4sh)
    key "m" action Play("audio",pkey.G4)
    key "k" action Play("audio",pkey.G4sh)
    key "," action Play("audio",pkey.A4)
    key "l" action Play("audio",pkey.A4sh)
    key "." action Play("audio",pkey.B4)
    key "/" action Play("audio",pkey.C5)

# label that calls this creen
label zz_play_piano:
    m 1a "Play for me, [player]..."
    $ disable_esc()
    $ store.songs.enabled = False
    $ store.hkb_button.enabled = False
    stop music
    call screen piano_keys()
    $ store.songs.enabled = True
    $ store.hkb_button.enabled = True
    $ enable_esc()
    $ play_song(store.songs.selected_track)
    m 1j "That was wonderful, [player]!"
    return
