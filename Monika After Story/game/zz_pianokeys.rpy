# proof of concept of piano keys being played
#

# setup sound assets
#define pkey.C4 = "mod_assets/sounds/piano_keys/C4.ogg"
#define pkey.C4sh = "mod_assets/sounds/piano_keys/C4sh.ogg"
#define pkey.D4 = "mod_assets/sounds/piano_keys/D4.ogg"
#define pkey.D4sh = "mod_assets/sounds/piano_keys/D4sh.ogg"
#define pkey.E4 = "mod_assets/sounds/piano_keys/E4.ogg"
define pkey.F4 = "mod_assets/sounds/piano_keys/F4.ogg"
define pkey.F4sh = "mod_assets/sounds/piano_keys/F4sh.ogg"
define pkey.G4 = "mod_assets/sounds/piano_keys/G4.ogg"
define pkey.G4sh = "mod_assets/sounds/piano_keys/G4sh.ogg"
define pkey.A4 = "mod_assets/sounds/piano_keys/A4.ogg"
define pkey.A4sh = "mod_assets/sounds/piano_keys/A4sh.ogg"
define pkey.B4 = "mod_assets/sounds/piano_keys/B4.ogg"
define pkey.C5 = "mod_assets/sounds/piano_keys/C5.ogg"
define pkey.C5sh = "mod_assets/sounds/piano_keys/C5sh.ogg"
define pkey.D5 = "mod_assets/sounds/piano_keys/D5.ogg"
define pkey.D5sh = "mod_assets/sounds/piano_keys/D5sh.ogg"
define pkey.E5 = "mod_assets/sounds/piano_keys/E5.ogg"
define pkey.F5 = "mod_assets/sounds/piano_keys/F5.ogg"
define pkey.F5sh = "mod_assets/sounds/piano_keys/F5sh.ogg"
define pkey.G5 = "mod_assets/sounds/piano_keys/G5.ogg"
define pkey.G5sh = "mod_assets/sounds/piano_keys/G5sh.ogg"
define pkey.A5 = "mod_assets/sounds/piano_keys/A5.ogg"
define pkey.A5sh = "mod_assets/sounds/piano_keys/A5sh.ogg"
define pkey.B5 = "mod_assets/sounds/piano_keys/B5.ogg"
define pkey.C6 = "mod_assets/sounds/piano_keys/C6.ogg"

screen piano_keys():
    $ import store.pkey as pkey
    modal True

    # DISABLING d  because 
    key "d" action NullAction()
    key "D" action NullAction()

    # quit action
    key "z" action Return()

    # alright time to do key things
#    key "c" action Play("audio",pkey.C4)
#    key "f" action Play("audio",pkey.C4sh)
#    key "v" action Play("audio",pkey.D4)
#    key "g" action Play("audio",pkey.D4sh)
#    key "b" action Play("audio",pkey.E4)
    key "q" action Play("audio",pkey.F4)
    key "2" action Play("audio",pkey.F4sh)
    key "w" action Play("audio",pkey.G4)
    key "3" action Play("audio",pkey.G4sh)
    key "e" action Play("audio",pkey.A4)
    key "4" action Play("audio",pkey.A4sh)
    key "r" action Play("audio",pkey.B4)
    key "t" action Play("audio",pkey.C5)
    key "6" action Play("audio",pkey.C5sh)
    key "y" action Play("audio",pkey.D5)
    key "7" action Play("audio",pkey.D5sh)
    key "u" action Play("audio",pkey.E5)
    key "i" action Play("audio",pkey.F5)
    key "9" action Play("audio",pkey.F5sh)
    key "o" action Play("audio",pkey.G5)
    key "0" action Play("audio",pkey.G5sh)
    key "p" action Play("audio",pkey.A5)
    key "-" action Play("audio",pkey.A5sh)
    key '[' action Play("audio",pkey.B5)
    key ']' action Play("audio",pkey.C6)

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
