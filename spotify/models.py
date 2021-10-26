from dataclasses import dataclass

@dataclass
class PodcastEpisode(object):
    imageUrl = str
    episodeName = str
    podcastName = str
    description = str
    spotifyPodcastUrl = str


