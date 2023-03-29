# PersonalPlayGround

There's three files in the repo:

1.  makinggil_github.py - Handles the connections network side, this is what runs on the VPS I have setup which should get us the data we need
2.  connecttoftp.py - What we run local side that handles downloading and extracting the files from the FTP server running on the VPS
3.  gilmaking.py  - What we run local side, a WIP to try and use said data to get the best items to sell
All the files have a variable called parent_directory  which you change accordingly.

Yesterday I broke something in gilmaking.py  where the multiprocessing dict isn't updated with the functions, no idea why haven't looked into it yet, but we got some time since we can't transfer to differnt servers rn anyways, but would be nice if we can get this working by the time the maintainance is over
