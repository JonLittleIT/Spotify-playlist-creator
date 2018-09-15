# Intro

This is a command line implementation of the [The Playlist Miner from plamere](https://github.com/plamere/playlistminer).

The playlist is created by counting the amount of appearances of songs in other playlists and then selecting the most counted songs. These other playlists are searched using specified keywords in the description of you playlist

# Requirements

Spotipy is required. Follow the [repositories](https://github.com/plamere/spotipy) steps for installation and setup.

I'm using Python 2.7.10 haven't tried on Python 3.

# Usage

## My Personal Implementation

1. Create a playlist using the GUI/APP

2. Edit it's description in such way that the keywords used are comma separated values after the first appearance of ':', a value between 0 and 1 must be provided after the second ':'(I will explain what this number is latter) and an integer grater than 0 must be given after the second ':'.

  Example: `This is an automatic playlist generated by my cool program using the following keywords bla bla bla : dance, electronic music, house, pop: 0.05: 5000`

3. The amount of playlists to be analysed is defined by the last number in the above example: `5000`.

  The total amount of playlists to be searched is divided by the amount of key words chosen. So if the keywords are : "rock, John Lennon" and you've chosen to read from 100 playlists, the program will search for 50 playlists with the word "rock" and 50 with the word "John Lennon".
  
  Of course, the bigger the number, the longer your program should run and the more precise the result should be. Currently, set to 7000 playlists, my computer takes between 10 to 20 minutes to complete the task. Now, if your connection is not the best, longer runs will end up in Spotify server cutting your connection, so play with this number.

#### The "magic number"

The number between 0 and 1 after the second ':' represents the level importance the program gives to the songs' popularity; Spotify places a number between 0 and 100 that represents the popularity of the song (being 100 the most popular), based on current count of daily reproductions, etc. This number is updated every couple of days.

So my "magic number" represents how important Spotify's popularity rate is to your playlist creation. For example: if we want a playlist with old classic rock songs we would generally give a "magic number" lower than 0.3 to the playlist, as we are not interested in the current popular rock songs on the market.

Now if we want a Pop playlist, we would use values above 0.5 so as to assure that the songs are currently popular.

#### Threads

I'm using a simple thread pool to make the process faster. It is currently running a pool of 3 threads. I have found, after a couple of try and error, that 5 threads will produce the fastest outcome when running on 1 playlist creation. Never the less, when running on multiple playlists, making to many requests will end up on Spotify cutting your connection.


## This steps must be done

Everything is explained in detail on [Spotipy](https://github.com/plamere/spotipy) in the [Documentation](https://github.com/plamere/spotipy#documentation) section, this is a simple explanation.

Playlist id can be found in the Spotify app by clicking on Share->Spotify Uri.

Run the program and your internet explorer will open requesting a login which must be done to generate the permission token which will be saved locally in your machine as `.cache-username-...` for future api connections.

You must first must edit `playlist_creator.py` and add your `client_id`, `client_secret` and `redirect_url` which are generated in online on the Spotify Developer page. Again, all this is explained on the [Spotipy Documentation](https://github.com/plamere/spotipy#documentation) page. 

## Run

`python playlist_creator.py username playlist:pid`

or

`python playlist_creator.py username` 

The second cmd will pick up any playlists whose name contains PLAYLIST_NAMES and will refresh it with a new round of songs.

I've posted and example of a bash script that would run several playlists. Never the less, the .py code could be edited to receive a list of playlist uri from cmd.

## Currently learning

Please suggest changes and edit the code to your desire. I'm in the learning process and help is welcomed.

