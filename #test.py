#test
from Interface import interface
from ffxiv_info_grabber import ffxiv_grabber
spiff=ffxiv_grabber("https://na.finalfantasyxiv.com/lodestone/playguide/db/gathering/?page=1", "https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=1")
splach=interface()
splach.autorun_grabber(spiff, True, 2)