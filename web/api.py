HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
   <head>
      <title>Clip from {podcast_name} -- {episode_name}</title>
      <meta property="og:title" content= "{podcast_name} -- {episode_name}" />
      <meta property="og:image" content= "{episode_image}" />
      <meta property="og:url" content="{audio_url}.html"/>
      <meta property="og:type" content="music.song"/>
      <meta property="og:audio" content="{audio_url}"/>
      <meta property="music:duration" content="{duration}"/>
      <meta property="twitter:image" content="{episode_image}" />
      <meta property="twitter:title" content="{podcast_name} - {episode_name} " />
      <meta property="twitter:description" content="{podcast_name} - {episode_name} by Kinlet" />
      <meta property="twitter:player:height" content="584" />
      <meta property="twitter:player:width" content="504" />
      <meta property="twitter:card" content="player" />
      <meta property="twitter:player" content="{audio_url}-container.html" />
      <meta property="twitter:audio:artist_name" content="{podcast_name}" />
      <meta property="twitter:audio:source" content="{audio_url}" />
      <meta name="twitter:creator" content="@george_sequeira" />
      <meta name="twitter:site" content="@george_sequeira" />
   </head>
   <body>
      <p><strong>Podcast Name: </strong>{podcast_name}</p>
      <p><strong>Episode Name: </strong>{episode_name}</p>
      <p><strong>From: </strong> {start_ts} to {end_ts}</p>
      <img src="{episode_image}"/>
      <br/>
      <audio controls>
         <source src = "{audio_url}" type = "{audio_extension}">
      </audio>
   </body>
</html>
"""


def create_html_for(podcast_name, episode_name, episode_image, start_ts, end_ts, audio_url, audio_extension):
    start_min = start_ts // 60
    start_sec = start_ts % 60
    start_ts_str = "{:02d}:{:02d}".format(start_min, start_sec)

    end_min = end_ts // 60
    end_sec = end_ts % 60
    end_ts_str = "{:02d}:{:02d}".format(end_min, end_sec)
    duration = end_ts - start_ts
    return HTML_TEMPLATE.format(
        podcast_name=podcast_name,
        episode_name=episode_name,
        start_ts=start_ts_str,
        end_ts=end_ts_str,
        duration=duration,
        episode_image=episode_image,
        audio_url=audio_url,
        audio_extension=audio_extension
    )


def create_audio_container(audio_url, audio_extension):
    return PLAYER_HTML.replace("AUDIO_URL", audio_url).replace("AUDIO_EXT", audio_extension)


PLAYER_HTML = """
<!DOCTYPE html>
<html>
<body>
<audio controls>
  <source src = "AUDIO_URL" type = "AUDIO_EXT">
</audio>

</body>
</html>
"""