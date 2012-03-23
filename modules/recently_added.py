from flask import Flask, render_template, send_file
import jsonrpclib
import urllib

from Maraschino import app
from settings import *
from maraschino.noneditable import *
from maraschino.tools import *

@app.route('/xhr/recently_added')
@requires_auth
def xhr_recently_added():
    return render_recently_added_episodes()


@app.route('/xhr/recently_added_movies')
@requires_auth
def xhr_recently_added_movies():
    return render_recently_added_movies()


@app.route('/xhr/recently_added_albums')
@requires_auth
def xhr_recently_added_albums():
    return render_recently_added_albums()


@app.route('/xhr/recently_added/<int:episode_offset>')
@requires_auth
def xhr_recently_added_episodes_offset(episode_offset):
    return render_recently_added_episodes(episode_offset)


@app.route('/xhr/recently_added_movies/<int:movie_offset>')
@requires_auth
def xhr_recently_added_movies_offset(movie_offset):
    return render_recently_added_movies(movie_offset)


@app.route('/xhr/recently_added_albums/<int:album_offset>')
@requires_auth
def xhr_recently_added_albums_offset(album_offset):
    return render_recently_added_albums(album_offset)


@app.route('/xhr/vfs_proxy/<path:url>')
def xhr_vfs_proxy(url):
    import StringIO

    try:
        vfs_url = '%s/vfs/' % (server_address())
    except:
        vfs_url = None

    vfs_url += urllib.unquote(url)

    img = StringIO.StringIO(urllib.urlopen(vfs_url).read())
    return send_file(img, mimetype='image/jpeg')

def render_recently_added_episodes(episode_offset=0):
    compact_view = get_setting_value('recently_added_compact') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_episodes = get_recently_added_episodes(xbmc, episode_offset)
        vfs_url = '/xhr/vfs_proxy/'

    except:
        recently_added_episodes = []
        vfs_url = None

    return render_template('recently_added.html',
        recently_added_episodes = recently_added_episodes,
        vfs_url = vfs_url,
        episode_offset = episode_offset,
        compact_view = compact_view,
    )


def render_recently_added_movies(movie_offset=0):
    compact_view = get_setting_value('recently_added_movies_compact') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_movies = get_recently_added_movies(xbmc, movie_offset)
        vfs_url = '/xhr/vfs_proxy/'

    except:
        recently_added_movies = []
        vfs_url = None

    return render_template('recently_added_movies.html',
        recently_added_movies = recently_added_movies,
        vfs_url = vfs_url,
        movie_offset = movie_offset,
        compact_view = compact_view,
    )


def render_recently_added_albums(album_offset=0):
    compact_view = get_setting_value('recently_added_albums_compact') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_albums = get_recently_added_albums(xbmc, album_offset)
        vfs_url = '/xhr/vfs_proxy/'

    except:
        recently_added_albums = []
        vfs_url = None

    return render_template('recently_added_albums.html',
        recently_added_albums = recently_added_albums,
        vfs_url = vfs_url,
        album_offset = album_offset,
        compact_view = compact_view,
    )


def get_num_recent_episodes():
    try:
        return int(get_setting_value('num_recent_episodes'))

    except:
        return 3

def get_num_recent_movies():
    try:
        return int(get_setting_value('num_recent_movies'))

    except:
        return 3


def get_num_recent_albums():
    try:
        return int(get_setting_value('num_recent_albums'))

    except:
        return 3


def get_recently_added_episodes(xbmc, episode_offset=0):
    num_recent_videos = get_num_recent_episodes()

    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(properties = ['title', 'season', 'episode', 'showtitle', 'playcount', 'thumbnail'])

        recently_added_episodes = recently_added_episodes['episodes'][episode_offset:num_recent_videos + episode_offset]

        for cur_ep in recently_added_episodes:
            cur_ep['safe_thumbnail'] = urllib.quote(cur_ep['thumbnail'], '')

    except:
        recently_added_episodes = []

    return recently_added_episodes


def get_recently_added_movies(xbmc, movie_offset=0):
    num_recent_videos = get_num_recent_movies()

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(properties = ['title', 'year', 'rating', 'playcount', 'thumbnail'])

        recently_added_movies = recently_added_movies['movies'][movie_offset:num_recent_videos + movie_offset]

        for cur_movie in recently_added_movies:
            cur_movie['safe_thumbnail'] = urllib.quote(cur_movie['thumbnail'], '')

    except:
        recently_added_movies = []

    return recently_added_movies

def get_recently_added_albums(xbmc, album_offset=0):
    num_recent_albums = get_num_recent_albums()

    try:
        recently_added_albums = xbmc.AudioLibrary.GetRecentlyAddedAlbums(properties = ['title', 'year', 'rating', 'artist', 'thumbnail'])

        recently_added_albums = recently_added_albums['albums'][album_offset:num_recent_albums + album_offset]

        for cur_album in recently_added_albums:
            cur_album['safe_thumbnail'] = urllib.quote(cur_album['thumbnail'], '')

    except:
        recently_added_albums = []

    return recently_added_albums
