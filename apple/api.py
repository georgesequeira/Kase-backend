import bs4
import json
import requests
import spotify.models

def parse_response(podcast_string_info):
    dict_response = json.loads(podcast_string_info)['results'][0]
    episode = spotify.models.PodcastEpisode()

    episode.imageUrl=dict_response['artworkUrl60']
    episode.podcastName=dict_response['trackName']
    episode.description=dict_response['collectionName']

    return episode


def get_podcast_title(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return soup.find_all('span', class_='product-header__title')[0].text.strip()


def get_episode_information(url):
    # parse id from the url
    # something like this: https://podcasts.apple.com/us/podcast/wtf-with-marc-maron-podcast/id12345?i=1000467187328
    podcastID = url.split("/id")[1].split("?")[0]

    # then create a url with it to help with
    # https://itunes.apple.com/lookup?id={ID_HERE}&entity=podcast
    infoUrl = "https://itunes.apple.com/lookup?id={ID_HERE}&entity=podcast".format(ID_HERE=podcastID)
    episode_result = requests.get(infoUrl)
    episode = parse_response(episode_result.content)
    title = get_podcast_title(url)
    episode.episodeName = title
    episode.spotifyPodcastUrl = url
    return episode
