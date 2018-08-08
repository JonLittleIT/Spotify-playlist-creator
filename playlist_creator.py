import sys
import itertools
import spotipy
import time
import spotipy.util as util
from string import strip

MAX_PLAYLISTS = 3000
SONG_AMOUNT = 120
MAX_SONGS_PER_REQUEST = 100  # segun spotify
POPULARITY = 0.4
TRACKS_FILE = 'tracks.pkl'

scope = 'user-library-modify, playlist-read-private, playlist-modify-public, playlist-modify-private, playlist-read-collaborative'


def is_good_playlist(items):
    artists = set()
    albums = set()
    for item in items:
        track = item['track']
        if track:
            artists.add(track['artists'][0]['id'])
            albums.add(track['album']['id'])
    return len(artists) > 1 and len(albums) > 1


def process_playlist(playlist):
    tracks = data['tracks']

    print data['ntracks'], len(tracks), playlist['name']

    pid = playlist['id']
    uid = playlist['owner']['id']
    data['playlists'] += 1

    try:
        results = sp.user_playlist_tracks(uid, pid)

        if results and 'items' in results and is_good_playlist(results['items']):
            for item in results['items']:
                track = item['track']
                if track:
                    tid = track['id']
                    if tid not in tracks:
                        title = track['name']
                        artist = track['artists'][0]['name']
                        popularity = track['popularity']
                        # release_date = track['album']['release_date']
                        tracks[tid] = {
                            'title': title,
                            'artist': artist,
                            'count': 0,
                            'popularity': popularity,
                            # 'release_date': release_date,
                        }
                    tracks[tid]['count'] += 1
                    data['ntracks'] += 1
        # else:
        # print 'mono playlist skipped'
    except spotipy.SpotifyException:
        pass
        # print 'trouble, skipping'


def crawl_playlists():
    limit = 50
    playlists_per_query = MAX_PLAYLISTS / len(queries)
    for query in queries:
        # print 'Query:', query
        which = 0
        offset = 0 if data['offset'] < 0 else data['offset'] + limit
        results = sp.search(query, limit=limit, offset=offset, type='playlist')
        playlist = results['playlists']
        # total = playlist['total']
        while playlist and which < playlists_per_query:
            data['offset'] = playlist['offset'] + playlist['limit']
            for item in itertools.islice(playlist['items'], playlists_per_query):
                if which >= playlists_per_query:
                    break
                process_playlist(item)
                which += 1

            if playlist['next']:
                results = sp.next(playlist)
                playlist = results['playlists']
            else:
                playlist = None


def get_queries_from_description(description):
    return map(strip, description.split(':')[1].split(','))


def get_description(user, pid):
    results = sp.user_playlist(user, playlist_id=pid, fields=None)
    return results['description']


def sort_tracks():
    tracks = data['tracks']
    tracks = sorted(tracks, key=lambda k: (tracks[k]['count']*(1-POPULARITY) + tracks[k]['popularity']*POPULARITY), reverse=True)
    tracks = tracks[0:SONG_AMOUNT]
    return [x for x in tracks if x is not None]


def load():
    return {
            'playlists': 0,
            'ntracks': 0,
            'offset': -1,
            'tracks': {}
            }


def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in xrange(0, len(l), n)]


def save_and_clear(tracks_list):
    count = 0
    max_chunk_lists = chunks(tracks_list, MAX_SONGS_PER_REQUEST)
    sp.user_playlist_replace_tracks(username, pid2, max_chunk_lists[0])
    count += len(max_chunk_lists[0])
    for tracks_chunk in max_chunk_lists[1:]:
        sp.user_playlist_add_tracks(username, pid2, tracks_chunk)
        count += len(tracks_chunk)
    return count


def get_popularity(description):
    return float(description.split(':')[2])


if __name__ == '__main__':

    if len(sys.argv) > 2:
        username = sys.argv[1]
        pid2 = sys.argv[2]
    else:
        print "Usage: %s username playlist_id" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username,scope,client_id=‘xxxx’,client_secret=‘xxxx’,redirect_uri=‘xxxx’)

    if token:
        start_time = time.time()

        sp = spotipy.Spotify(auth=token)

        description = get_description(username, pid2)
        POPULARITY = get_popularity(description)
        queries = get_queries_from_description(description)
        data = load()
        crawl_playlists()
        n_songs_saved = save_and_clear(sort_tracks())

        elapsed_time = time.time() - start_time
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        print
        print "Successful run on playlist:", pid2, "for user:", username
        print n_songs_saved, "songs where saved.", MAX_PLAYLISTS, "playlists read with popularity set to", POPULARITY
        print "Total time elapsed:", elapsed_time
    else:
        print "Can't get token for", username
