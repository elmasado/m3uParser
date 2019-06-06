
import argparse
import vlc
import time

class track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path

def isValid(url):
    # define VLC instance
    instance = vlc.Instance('--input-repeat=-1')

    # Define VLC player
    player = instance.media_player_new()

    # Define VLC media
    media = instance.media_new(url)

    # Set player media
    player.set_media(media)

    # Play the media
    player.play()

    # Sleep for 5 sec for VLC to complete retries.
    time.sleep(3)
    # Get current state.
    state = str(player.get_state())

    # Find out if stream is working.
    if state == "vlc.State.Error" or state == "State.Error" or state == "State.Ended":
        print('Stream is dead. Current state = {}'.format(state))
        player.stop()
        return False
    else:
        print('Stream is working. Current state = {}'.format(state))
        player.stop()
        return True

def parsem3u(infile, keys):
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        infile = open(infile, 'r')

    """
        All M3U files start with #EXTM3U.
        If the first line doesn't start with this, we're either
        not working with an M3U or the file we got is corrupted.
    """
    line = infile.readline()
    # if not line.startswith('#EXTM3U') and not line.startswith('﻿#EXTM3U') and not:
    #     print("Error")
    #     return

    # initialize playlist variables before reading file
    playlist=[]
    song = track(None,None,None)
    validUrl = None
    for line in infile:
        line_str=line.strip()
        if line_str.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            length,title = line_str.split('#EXTINF:')[1].split(',', 1)
            title = title.lower()
            if len(keys) == 0:
                validUrl = line
            else:
                for key in keys:
                    if key.lower() in title:
                        validUrl=line

            song = track(length, title, None)
        elif (len(line) != 0 and validUrl!=None):
            if isValid(line.replace('\n', '')):
                with open("output.m3u", "a") as ofile:
                    ofile.write(validUrl)
                    ofile.write(line)
                    validUrl=None
            # pull song path from all other, non-blank lines
            song.path=line
            playlist.append(song)
            # reset the song variable so it doesn't use the same EXTINF more than once
            song=track(None,None,None)
    infile.close()
    return playlist

# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="Input m3u file")
    ap.add_argument("-k", "--key", required=False, help="Input keys channels")
    args = vars(ap.parse_args())

    m3ufile=args["file"]
    keys=[]
    if(args["key"] is not None):
        keys=args["key"].split(',')
    playlist = parsem3u(m3ufile, keys)
    # for track in playlist:
    #     print (track.title,"#", track.length, "#", track.path)
    #     print("---------------------------");

if __name__ == '__main__':
    main()
