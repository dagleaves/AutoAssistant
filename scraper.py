from typing import List, Tuple

# pip install youtube-search-python
from youtubesearchpython import Playlist, playlist_from_channel_id

# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi


def get_channel_videos(channel: str) -> List[dict]:
    """
    Returns Playlist of videos from a YouTube channel
    """
    ret = Playlist(playlist_from_channel_id(channel))
    print(f'Videos Retrieved: {len(ret.videos)}')

    while ret.hasMoreVideos:
        ret.getNextVideos()
        print(f'Videos Retrieved: {len(ret.videos)}')

    return ret.videos


def get_youtube_video_transcript(video_id: str) -> str:
    """"
    Returns transcript of the given video id
    """
    try:
        ts = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en-US', 'en']
        )
        utterances = [p['text'] for p in ts]
        return ' '.join(utterances)

    except:
        pass


def get_videos_and_transcriptions(channel_ids: List[str]=None) -> Tuple[List[str], List[dict]]:
    """
    Returns the video titles and citation metadata for the vector store
    """
    if channel_ids is None:
        channel_ids = ['UCes1EvRjcKU4sY_UEavndBw', 'UC_q-UNDJeEBSHqKzAP_8x_A', 'UCVvE8kQTuZEykvMFZBVzftg']

    videos = []
    for channel_id in channel_ids:
        videos += get_channel_videos(channel_id)
        break

    titles = []
    metadata = []
    for i, video in enumerate(videos):
        print(f'Retrieving video ({i}/{len(videos)})')
        transcript = get_youtube_video_transcript(video['id'])
        if not transcript:
            continue

        titles.append(video['title'])
        metadata.append({
            'link': video['link'],
            'channel': video['channel']['name'],
            'channel_link': 'https://www.youtube.com' + video['channel']['link'],
            'transcript': transcript
        })

    return titles, metadata
