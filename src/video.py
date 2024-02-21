import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id
        self.youtube = self.get_service()
        video_data = self.get_video_info()
        self.video_title = video_data['items'][0]['snippet']['title']
        self.video_url = f"https://www.youtube.com/{video_id}"
        self.view_count = video_data['items'][0]['statistics']['viewCount']
        self.like_count = video_data['items'][0]['statistics']['likeCount']

    def get_video_info(self):
        """Выводит информацию о видео."""
        video_data = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=self.__video_id).execute()
        return video_data

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=os.getenv('API_KEY'))

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    """Экземпляр инициализируется id видео и id плейлиста. Данные наследуются от класса Video"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id