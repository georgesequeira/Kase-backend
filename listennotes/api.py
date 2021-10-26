import json
import listennotes.models
import requests
API_TOKEN = "f47ded04070047319e409132bb61409a"


def get_search_url_for(episode_name):
    return 'https://listen-api.listennotes.com/api/v2/search?'\
        'q="' + episode_name + '"'\
        '&sort_by_date=0&'\
        'type=episode'\
        '&only_in=title'


def get_episode_url_for(episode_id):
    return f'https://listen-api.listennotes.com/api/v2/episodes/{episode_id}?'


def retrieval(partial):
    headers = {
        'X-ListenAPI-Key': API_TOKEN,
    }
    search_url = get_search_url_for(partial)
    result = requests.request('GET', search_url, headers=headers)

    if result.status_code == 200:
        return json.loads(result.content)
    else:
        return dict(results=[])


def retrieve_episode_info(episode_id):
    result = get_episode_information(episode_id)
    second_result = requests.head(result['audio'])
    return dict(
        podcast_name=result['podcast']['title'],
        episode_name=result['title'],
        image_url=result['thumbnail'],
        audio_url=second_result.headers['Location'])


def try_fuzzy_retrieval(episode_partial_name):
    content = retrieval(episode_partial_name)
    if len(content['results']) > 0:
        return content
    else:
        split_by_space = episode_partial_name.split(' ')
        new_splits = split_by_space[:len(split_by_space)-1]
        new_partial = ' '.join(new_splits)

        content = retrieval(new_partial)
        if len(content['results']) > 0:
            return content
        else:
            new_splits = split_by_space[1:]
            new_partial = ' '.join(new_splits)
            content = retrieval(new_partial)
            if len(content['results']) > 0:
                return content
            else:
                new_splits = split_by_space[1:len(split_by_space) - 1]
                new_partial = ' '.join(new_splits)
                content = retrieval(new_partial)
                if len(content['results']) > 0:
                    return content



def get_podcast_info(episode_partial_name):
    episode = listennotes.models.ListenNotesEpisode()
    episode.partial_episode_name = episode_partial_name
    episode.found = False
    episode.error = False
    episode.episode_name = ""
    episode.podcast_name = ""
    episode.description = ""
    episode.audio_url = ""
    episode.audio_length_sec = 0
    episode.error_msg = ""
    episode.image_url = ""
    episode.id = ""


    content = try_fuzzy_retrieval(episode_partial_name)
    if content:
        episode_information = get_episode_information(content['results'][0]['id'])
        if episode_information:
            episode.id = episode_information['id']
            episode.episode_name = episode_information['title']
            episode.podcast_name = episode_information['podcast']['title']
            episode.description = episode_information['description']
            episode.audio_url = episode_information['audio']
            episode.audio_length_sec = episode_information['audio_length_sec']
            episode.image_url = episode_information['image']
            episode.found = True
        if content['results']:
            episode.audio_url = requests.head(content['results'][0]['audio']).headers['Location']
            episode.found = True
    else:
        episode.error = True
        episode.error_msg = "Issue finding by episode name."

    return episode


def get_episode_information(episode_id):
    headers = {
        'X-ListenAPI-Key': API_TOKEN,
    }
    result = requests.request('GET', get_episode_url_for(episode_id), headers=headers)

    if result.status_code == 200:
        return json.loads(result.content)
    else:
        return None
