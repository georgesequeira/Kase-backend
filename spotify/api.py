from spotipy.oauth2 import SpotifyClientCredentials
import spotify.models
import spotipy


SPOTIPY_CLIENT_ID = "5fbfdfe65fb94814a2c3df7909404bfd"
SPOTIPY_CLIENT_SECRET = "f6db8fd58c1a4bea9aba5b7f2f74ff3c"


SPOTIFY = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))


def get_episode_information(episode_id):
    episode_result = SPOTIFY._get('episodes/' + episode_id, market='US')

    episode = spotify.models.PodcastEpisode()
    episode.imageUrl=_get_image_url(episode_result)
    episode.episodeName=_get_episode_name(episode_result)
    episode.podcastName=_get_podcast_name(episode_result)
    episode.description=_get_description(episode_result)
    episode.spotifyPodcastUrl=_get_spotify_url(episode_result)

    return episode


def _get_image_url(episode_result):
    max_size = -1
    # some square placeholder. we can host our own later.
    return_url = "https://dimensionmill.org/wp-content/uploads/2019/03/square-placeholder.jpg"
    for image in episode_result.get('images'):
        if image['height'] > max_size:
            return_url = image['url']
            max_size = image['height']

    return return_url


def _get_episode_name(episode_result):
    return episode_result.get('name', '').strip()


def _get_podcast_name(episode_result):
    return episode_result.get('show', {}).get('name', '')


def _get_description(episode_result):
    return episode_result.get('description', '').strip()


def _get_spotify_url(episode_result):
    return 'https://open.spotify.com/episode/' + episode_result['id']