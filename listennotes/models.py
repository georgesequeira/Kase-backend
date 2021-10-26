from dataclasses import dataclass


class ListenNotesEpisode():
    partial_episode_name = str
    episode_name = str
    podcast_name = str
    description = str
    audio_url = str
    audio_length_sec = int
    found = bool
    error = bool
    error_msg = str
    image_url = str
    id = str


