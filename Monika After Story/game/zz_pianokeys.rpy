# Module that lets you play the piano
#

# TRANSFORMS
transform piano_quit_label:
    xalign 0.5 yanchor 0 ypos 650

# label that calls this creen
label zz_play_piano:
    m 1j "You want to play the piano?"
    m 1a "Then play for me, [player]..."

    # pre call setup
    python:
        quit_label = Text("Press 'Z' to quit", size=36) 
        disable_esc()
        store.songs.enabled = False
        store.hkb_button.enabled = False
    stop music
    show text quit_label zorder 10 at piano_quit_label

    # call the display
    $ ui.add(PianoDisplayable())
    $ result = ui.interact()

    # post call cleanup
    hide text quit_label
    $ store.songs.enabled = True
    $ store.hkb_button.enabled = True
    $ enable_esc()
    $ play_song(store.songs.selected_track)

    m 1j "That was wonderful, [player]!"
    return

# keep the above for reference
# DISPLAYABLE:

# this is our threshold for determining how many notes the player needs to play
# before we check for dialogue
define zzpk.NOTE_SIZE = 6 

init python:
    import pygame # because we need them keyups 

    # Exception class for piano failures
    class PianoException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "PianoException: " + self.msg

    # this class matches particular sets of notes to some dialogue that 
    # Monika can say.
    # NOTE: only one line of dialogue per set of notes, because brevity is
    #   important
    #
    # PROPERTIES:
    #   say - the line of dialogue to say
    #   notes - list of notes (keys) that we need to hear to show the dialogue
    #       this is ORDER match only. also chords are NOT supported
    #       NOTE: This is expected as a list of ZZPK constants.
    #   notestr - string version of the list of notes, for matching
    #   img - the image of monika to show
    #
    class PianoNoteMatch():
        def __init__(self, say, notes, express="1a"):
            #
            # IN:
            #   say - line of dialogue to say
            #   notes - list of notes (keys) to match
            #   express - the monika expression we want to show

            if say is None or len(say) == 0:
                raise PianoException("Dialogue must exist")
            if notes is None or len(notes) < zzpk.NOTE_SIZE:
                raise PianoException(
                    "Notes list must be longer than " + str(zzpk.NOTE_SIZE)
                )

            self.say = say
            self.notes = notes
            self.notestr = "".join([chr(x) for x in notes])

            # complicated process to convert an expression to a blitable image
            img = renpy.display.image.images.get(("monika", express), None)

            if img is None:
                raise PianoException("Given expression was invalid")

            self.img = img

    # the displayable
    class PianoDisplayable(renpy.Displayable):

        # CONSTANTS
        # timeout
        TIMEOUT = 1.0 # seconds

        # AT_LIST 
        AT_LIST = [i11]

        # keys
        ZZPK_QUIT = pygame.K_z
        ZZPK_F4 = pygame.K_q
        ZZPK_F4SH = pygame.K_2
        ZZPK_G4 = pygame.K_w
        ZZPK_G4SH = pygame.K_3
        ZZPK_A4 = pygame.K_e
        ZZPK_A4SH = pygame.K_4
        ZZPK_B4 = pygame.K_r
        ZZPK_C5 = pygame.K_t
        ZZPK_C5SH = pygame.K_6
        ZZPK_D5 = pygame.K_y
        ZZPK_D5SH = pygame.K_7
        ZZPK_E5 = pygame.K_u
        ZZPK_F5 = pygame.K_i
        ZZPK_F5SH = pygame.K_9
        ZZPK_G5 = pygame.K_o
        ZZPK_G5SH = pygame.K_0
        ZZPK_A5 = pygame.K_p
        ZZPK_A5SH = pygame.K_MINUS
        ZZPK_B5 = pygame.K_LEFTBRACKET
        ZZPK_C6 = pygame.K_RIGHTBRACKET

        # filenames
        ZZFP_F4 =  "mod_assets/sounds/piano_keys/F4.ogg"
        ZZFP_F4SH = "mod_assets/sounds/piano_keys/F4sh.ogg"
        ZZFP_G4 = "mod_assets/sounds/piano_keys/G4.ogg"
        ZZFP_G4SH = "mod_assets/sounds/piano_keys/G4sh.ogg"
        ZZFP_A4 = "mod_assets/sounds/piano_keys/A4.ogg"
        ZZFP_A4SH = "mod_assets/sounds/piano_keys/A4sh.ogg"
        ZZFP_B4 = "mod_assets/sounds/piano_keys/B4.ogg"
        ZZFP_C5 = "mod_assets/sounds/piano_keys/C5.ogg"
        ZZFP_C5SH = "mod_assets/sounds/piano_keys/C5sh.ogg"
        ZZFP_D5 = "mod_assets/sounds/piano_keys/D5.ogg"
        ZZFP_D5SH = "mod_assets/sounds/piano_keys/D5sh.ogg"
        ZZFP_E5 = "mod_assets/sounds/piano_keys/E5.ogg"
        ZZFP_F5 = "mod_assets/sounds/piano_keys/F5.ogg"
        ZZFP_F5SH = "mod_assets/sounds/piano_keys/F5sh.ogg"
        ZZFP_G5 = "mod_assets/sounds/piano_keys/G5.ogg"
        ZZFP_G5SH = "mod_assets/sounds/piano_keys/G5sh.ogg"
        ZZFP_A5 = "mod_assets/sounds/piano_keys/A5.ogg"
        ZZFP_A5SH = "mod_assets/sounds/piano_keys/A5sh.ogg"
        ZZFP_B5 = "mod_assets/sounds/piano_keys/B5.ogg"
        ZZFP_C6 = "mod_assets/sounds/piano_keys/C6.ogg"

        # piano images
        ZZPK_IMG_BACK = "mod_assets/piano/piano.png"

        # overlay, white
        ZZPK_W_OVL_F4 = "mod_assets/piano/white_ovl/F4.png"
        ZZPK_W_OVL_G4 = "mod_assets/piano/white_ovl/G4.png"
        ZZPK_W_OVL_A4 = "mod_assets/piano/white_ovl/A4.png"
        ZZPK_W_OVL_B4 = "mod_assets/piano/white_ovl/B4.png"
        ZZPK_W_OVL_C5 = "mod_assets/piano/white_ovl/C5.png"
        ZZPK_W_OVL_D5 = "mod_assets/piano/white_ovl/D5.png"
        ZZPK_W_OVL_E5 = "mod_assets/piano/white_ovl/E5.png"
        ZZPK_W_OVL_F5 = "mod_assets/piano/white_ovl/F5.png"
        ZZPK_W_OVL_G5 = "mod_assets/piano/white_ovl/G5.png"
        ZZPK_W_OVL_A5 = "mod_assets/piano/white_ovl/A5.png"
        ZZPK_W_OVL_B5 = "mod_assets/piano/white_ovl/B5.png"
        ZZPK_W_OVL_C6 = "mod_assets/piano/white_ovl/C6.png"

        # overlay black
        ZZPK_B_OVL_F4SH = "mod_assets/piano/black_ovl/F4SH.png"
        ZZPK_B_OVL_G4SH = "mod_assets/piano/black_ovl/G4SH.png"
        ZZPK_B_OVL_A4SH = "mod_assets/piano/black_ovl/A4SH.png"
        ZZPK_B_OVL_C5SH = "mod_assets/piano/black_ovl/C5SH.png"
        ZZPK_B_OVL_D5SH = "mod_assets/piano/black_ovl/D5SH.png"
        ZZPK_B_OVL_F5SH = "mod_assets/piano/black_ovl/F5SH.png"
        ZZPK_B_OVL_G5SH = "mod_assets/piano/black_ovl/G5SH.png"
        ZZPK_B_OVL_A5SH = "mod_assets/piano/black_ovl/A5SH.png"

        # offsets for rendering
        ZZPK_IMG_BACK_X = 10
        ZZPK_IMG_BACK_Y = 10
        
        def __init__(self):
            super(renpy.Displayable,self).__init__()

            # setup images

            # background piano
            self.piano_back = Image(self.ZZPK_IMG_BACK)
            self.PIANO_BACK_WIDTH = 437
            self.PIANO_BACK_HEIGHT = 214

            # setup sounds
            # sound dict:
            self.pkeys = {
                self.ZZPK_F4: self.ZZFP_F4,
                self.ZZPK_F4SH: self.ZZFP_F4SH,
                self.ZZPK_G4: self.ZZFP_G4,
                self.ZZPK_G4SH: self.ZZFP_G4SH,
                self.ZZPK_A4: self.ZZFP_A4,
                self.ZZPK_A4SH: self.ZZFP_A4SH,
                self.ZZPK_B4: self.ZZFP_B4,
                self.ZZPK_C5: self.ZZFP_C5,
                self.ZZPK_C5SH: self.ZZFP_C5SH,
                self.ZZPK_D5: self.ZZFP_D5,
                self.ZZPK_D5SH: self.ZZFP_D5SH,
                self.ZZPK_E5: self.ZZFP_E5,
                self.ZZPK_F5: self.ZZFP_F5,
                self.ZZPK_F5SH: self.ZZFP_F5SH,
                self.ZZPK_G5: self.ZZFP_G5,
                self.ZZPK_G5SH: self.ZZFP_G5SH,
                self.ZZPK_A5: self.ZZFP_A5,
                self.ZZPK_A5SH: self.ZZFP_A5SH,
                self.ZZPK_B5: self.ZZFP_B5,
                self.ZZPK_C6: self.ZZFP_C6
            }

            # pressed dict
            self.pressed = {
                self.ZZPK_F4: False,
                self.ZZPK_F4SH: False,
                self.ZZPK_G4: False,
                self.ZZPK_G4SH: False,
                self.ZZPK_A4: False,
                self.ZZPK_A4SH: False,
                self.ZZPK_B4: False,
                self.ZZPK_C5: False,
                self.ZZPK_C5SH: False,
                self.ZZPK_D5: False,
                self.ZZPK_D5SH: False,
                self.ZZPK_E5: False,
                self.ZZPK_F5: False,
                self.ZZPK_F5SH: False,
                self.ZZPK_G5: False,
                self.ZZPK_G5SH: False,
                self.ZZPK_A5: False,
                self.ZZPK_A5SH: False,
                self.ZZPK_B5: False,
                self.ZZPK_C6: False
            }

            # overlay dict
            # NOTE: x and y are assumed to be relative to the top let of
            #   the piano_back image
            # (overlay image, x coord, y coord, width, height)
            #
            # NOTE: we have to do this because not every image is the same
            self.overlays = {
                self.ZZPK_F4: (Image(self.ZZPK_W_OVL_F4), 1, 2, 35, 210),
                self.ZZPK_F4SH: (Image(self.ZZPK_B_OVL_F4SH), 24, 2, 26, 149),
                self.ZZPK_G4: (Image(self.ZZPK_W_OVL_G4), 37, 2, 33, 210),
                self.ZZPK_G4SH: (Image(self.ZZPK_B_OVL_G4SH), 60, 2, 25, 149),
                self.ZZPK_A4: (Image(self.ZZPK_W_OVL_A4), 73, 2, 36, 210),
                self.ZZPK_A4SH: (Image(self.ZZPK_B_OVL_A4SH), 97, 2, 25, 149),
                self.ZZPK_B4: (Image(self.ZZPK_W_OVL_B4), 110, 2, 36, 210),
                self.ZZPK_C5: (Image(self.ZZPK_W_OVL_C5), 147, 2, 34, 210),
                self.ZZPK_C5SH: (Image(self.ZZPK_B_OVL_C5SH), 170, 2, 25, 149),
                self.ZZPK_D5: (Image(self.ZZPK_W_OVL_D5), 182, 2, 36, 210),
                self.ZZPK_D5SH: (Image(self.ZZPK_B_OVL_D5SH), 205, 2, 25, 149),
                self.ZZPK_E5: (Image(self.ZZPK_W_OVL_E5), 219, 2, 36, 210),
                self.ZZPK_F5: (Image(self.ZZPK_W_OVL_F5), 256, 2, 35, 210),
                self.ZZPK_F5SH: (Image(self.ZZPK_B_OVL_F5SH), 279, 2, 25, 149),
                self.ZZPK_G5: (Image(self.ZZPK_W_OVL_G5), 292, 2, 36, 210),
                self.ZZPK_G5SH: (Image(self.ZZPK_B_OVL_G5SH), 315, 2, 25, 149),
                self.ZZPK_A5: (Image(self.ZZPK_W_OVL_A5), 329, 2, 36, 210),
                self.ZZPK_A5SH: (Image(self.ZZPK_B_OVL_A5SH), 352, 2, 25, 149),
                self.ZZPK_B5: (Image(self.ZZPK_W_OVL_B5), 366, 2, 35, 210),
                self.ZZPK_C6: (Image(self.ZZPK_W_OVL_C6), 402, 2, 34, 210)
            }

            # your reality, note matching
            # NOTE: This works by peforming `in` matches of lists.
            self.pnm_yourreality = [
                PianoNoteMatch(
                    ("{cps=*2}~Everyday, I imagine a future where I can be " +
                    "with you~{/cps}{w=1.5}{nw}"),
                    [
                        self.ZZPK_G5,
                        self.ZZPK_G5,
                        self.ZZPK_G5,
                        self.ZZPK_G5,
                        self.ZZPK_F5,
                        self.ZZPK_E5,
                        self.ZZPK_E5,
                        self.ZZPK_F5,
                        self.ZZPK_G5,
                        self.ZZPK_E5,
                        self.ZZPK_D5,
                        self.ZZPK_C5,
                        self.ZZPK_D5,
                        self.ZZPK_E5,
                        self.ZZPK_C5,
                        self.ZZPK_G4
                    ],
                    express="1j"
                ),
            ]

            # list containing lists of matches. 
            # NOTE: highly recommend not adding too many detections
            self.pnm_list = [
                self.pnm_yourreality
            ]

            # list of notes we have played
            self.played = list()
            self.prev_time = 0

        def findnotematch(self, notes):
            #
            # Finds a PianoNoteMatch object that matches the given set of
            # notes.
            #
            # IN:
            #   notes - list of notes to match
            #
            # RETURNS:
            #   PianoNoteMatch object that matches, or None if no match

            # convert to string for ease of us
            notestr = "".join([chr(x) for x in notes])

            for pnm_s in self.pnm_list:
                for pnm in pnm_s:
                    if notestr in pnm.notestr:
                        return pnm

            return None

        def render(self, width, height, st, at):
            # renpy render function
            # NOTE: Displayables are EVENT-DRIVEN

            r = renpy.Render(width, height)

            # prepare piano back as render
            piano = renpy.render(self.piano_back, 1280, 720, st, at)

            # now prepare overlays to render
            overlays = list()
            for k in self.pressed:
                if self.pressed[k]:
                    overlays.append(
                        (
                            renpy.render(self.overlays[k][0], 1280, 720, st, at),
                            self.overlays[k][1],
                            self.overlays[k][2]
                        )
                    )

            # Draw the piano
            r.blit(
                piano, 
                (
                    self.ZZPK_IMG_BACK_X, 
                    self.ZZPK_IMG_BACK_Y
                )
            )

            # and now the overlays
            for ovl in overlays:
                r.blit(
                    ovl[0], 
                    (
                        self.ZZPK_IMG_BACK_X + ovl[1],
                        self.ZZPK_IMG_BACK_Y + ovl[2]
                    )
                )

# NOTE: we might be able to use this for debug, but it crahes when given
# an open bracket.
#            if len(self.played) > 0:
#                teee = Text("".join([chr(x) for x in self.played]))
#                testT = renpy.render(teee, 1280, 720, st, at)
#                r.blit(testT, (500,300))

            # check if we have enough played notes
            if len(self.played) >= zzpk.NOTE_SIZE:
                match = self.findnotematch(self.played)


                if match:
                    r.blit(
                        renpy.render(match.img, 1280, 720, st, at),
                        (0, 0)
                    )
                    renpy.say(m, match.say, interact=False)

            # rerender redrawing thing
            # renpy.redraw(self, 0)

            # and apparenly we return the render object
            return r

        def event(self, ev, x, y, st):
            # renpy event handler
            # NOTE: Renpy is EVENT-DRIVEN

            # when you press down a key, we launch a sound
            if ev.type == pygame.KEYDOWN:

                # we only care about keydown events regarding timeout
                if st-self.prev_time >= self.TIMEOUT:
                    self.played = list()

                # setup previous time thing
                self.prev_time = st

                # but first, check for quit ("Z")
                if ev.key == self.ZZPK_QUIT:
                    return "q" # quit this game
                else:

                    # only play a sound if we've lifted the finger
                    if not self.pressed.get(ev.key, True):

                        # add to played
                        self.played.append(ev.key)

                        # set appropriate value
                        self.pressed[ev.key] = True

                        # get a sound to play
                        renpy.play(self.pkeys[ev.key], channel="audio")

                        # now rerender
                        renpy.redraw(self, 0)

            # keyup, means we should stop render
            elif ev.type == pygame.KEYUP:

                # only do this if we keyup a key we care about
                if self.pressed.get(ev.key, False):

                    # set appropriate value
                    self.pressed[ev.key] = False

                    # now rerender
                    renpy.redraw(self,0)

            # the default so we can keep going
            raise renpy.IgnoreEvent()

