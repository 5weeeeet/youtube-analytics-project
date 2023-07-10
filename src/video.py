import os
import json

from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY_YOUTUBE')
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

class Video:
    """Класс для ютуб-видео по id видео"""

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_response = YOUTUBE.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        self.__title = self.video_response['items'][0]['snippet']['title']
        self.__url = 'https://www.youtube.com/channel/' + self.video_id
        self.__viewCount = self.video_response['items'][0]['statistics']['viewCount']
        self.__likeCount = self.video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        return f'{self.__title}'

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def __view_count(self):
        return self.__view_count

    @property
    def __like_count(self):
        return self.__like_count


    def printj(self):
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))


class PLVideo(Video):
    def __init__(self, video_id: str, play_list_id: str):
        super().__init__(video_id)
        self.play_list_id = play_list_id
        self.video_response = YOUTUBE.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        self.__title = self.video_response['items'][0]['snippet']['title']
        self.__url = 'https://www.youtube.com/channel/' + self.video_id
        self.__viewCount = self.video_response['items'][0]['statistics']['viewCount']
        self.__likeCount = self.video_response['items'][0]['statistics']['likeCount']