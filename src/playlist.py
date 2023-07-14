import os
import json
import isodate

from datetime import datetime, timedelta
from src.video import Video

from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY_YOUTUBE')
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)


class PlayList:
    """Класс для ютуб-плейлиста по id видео"""

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist = YOUTUBE.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_videos = YOUTUBE.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"]
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        """Выводит общее время всех видео в плейлисте"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = YOUTUBE.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_duration = timedelta(0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = str(isodate.parse_duration(iso_8601_duration))
            date_time_duration = datetime.strptime(duration, '%H:%M:%S')
            timedelta_duration = timedelta(hours=date_time_duration.hour,
                                           minutes=date_time_duration.minute,
                                           seconds=date_time_duration.second)
            total_duration += timedelta_duration
        return total_duration

    def printj(self):
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    def show_best_video(self):
        """
        Возвращает видео с большим количеством лайком, по сравнению с другими
        """
        video_ids_list = [i['contentDetails']['videoId'] for i in self.playlist_videos['items']]
        best_video_url = {'url': '', 'likes': 0}
        for id_video in video_ids_list:
            video = Video(id_video)
            if video.like_count > best_video_url['likes']:
                best_video_url.update({'url': video.url, 'likes': video.like_count})
        return best_video_url['url']