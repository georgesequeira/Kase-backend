from flask import request, abort
from google.cloud import storage


import apple.api
import audio.clipper
import flask
import json
import gc
import hashlib
import random
import requests
import spotify.api
import listennotes.api
import web.api

app = flask.Flask(__name__)

images = [
  "https://images.unsplash.com/photo-1494253109108-2e30c049369b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80",
  "https://pbs.twimg.com/profile_images/1186876544263872512/MA8AZsIV_400x400.jpg",
  "https://chordify.net/pages/wp-content/uploads/2019/08/random-chiasso-1024x683.png"
]

def create_response_v2(episode_name, podcast_name):
    listennotes_info = listennotes.api.get_podcast_info(episode_name)
    return listennotes_info.__dict__


@app.route('/v0/api/episodeInformation', methods=['GET'])
def home():
  episode_name = request.args.get('episodeName')
  podcast_name = request.args.get('podcastName')
  return create_response_v2(episode_name, podcast_name)


@app.route('/v0/api/clip', methods=['POST'])
def create_clip():
    if request.method != 'POST':
        abort(400)

    episode_id = request.form.get('episodeId')
    start_ts = request.form.get('startTs')
    end_ts = request.form.get('endTs')

    target_key = hashlib.md5(f"{episode_id}-{start_ts}-{end_ts}".encode("utf-8")).hexdigest()
    episode_info = listennotes.api.retrieve_episode_info(episode_id)

    podcast_name = episode_info['podcast_name']
    episode_name = episode_info['episode_name']
    image_url = episode_info['image_url']
    audio_url = episode_info['audio_url']

    result = requests.get(audio_url, stream=True)
    web_extension = result.headers['Content-Type'] or result.headers['Content-Type']
    if not web_extension:
        audio_extension = audio_url.split('.')[-1]
    else:
        audio_extension = web_extension.split('/')[-1]

    storage_client = storage.Client()
    bucket = storage_client.bucket("kinlet-clips")

    blob = bucket.blob(target_key)
    audio_bytes = audio.clipper.create_clip_for(result.content, audio_extension, int(start_ts), int(end_ts))
    try:
        blob.upload_from_string(audio_bytes, content_type=web_extension)
        ## success!
        ## lets create a webpage that points to that blob.
        audio_url = bucket.blob(target_key).public_url
        web_content = web.api.create_html_for(
            podcast_name,
            episode_name,
            image_url,
            int(start_ts),
            int(end_ts),
            audio_url,
            web_extension)

        html_blob = bucket.blob(target_key + ".html")
        html_blob.content_disposition = "text/html"
        html_blob.contentDisposition = "text/html"
        html_blob.upload_from_string(web_content, content_type='text/html')

        container = web.api.create_audio_container(audio_url, web_extension)
        audio_container_blob = bucket.blob(target_key + "-container.html")
        audio_container_blob.content_disposition = "text/html"
        audio_container_blob.contentDisposition = "text/html"
        audio_container_blob.upload_from_string(container, content_type='text/html')

        return html_blob.public_url

    except Exception as e:
        print("another issue")
        import traceback
        traceback.print_exc()
        abort(500)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
