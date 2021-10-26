from io import BytesIO
from pydub import AudioSegment


def create_clip_for(bytes, extension, start_in_sec, end_in_sec):
    original = AudioSegment.from_file(BytesIO(bytes), format=extension)
    # lets do first 5 seconds
    section = original[int(start_in_sec) * 1000:int(end_in_sec) * 1000]

    tempclip = section.export(format=extension)
    return tempclip.read()