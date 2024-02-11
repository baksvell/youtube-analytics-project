from googleapiclient.discovery import build
import json
import os

from dotenv import load_dotenv

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = self.get_service().channels().list(
            id=self.channel_id,
            part='snippet, statistics').execute()
        snippet = channel["items"][0]["snippet"]
        statistics = channel["items"][0]["statistics"]
        self.title = snippet["title"]
        self.description = snippet["description"]
        self.url = f'https://youtube.com/{snippet["customUrl"]}'
        self.subscribers_count = int(statistics["subscriberCount"])
        self.video_count = int(statistics["videoCount"])
        self.view_count = int(statistics["viewCount"])

    def __str__(self) -> str:
        """Возвращает название канала и ссылку."""
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """Возвращает общее количество подписчиков."""
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other) -> int:
        """Возвращает разность количества подписчиков."""
        return self.subscribers_count - other.subscribers_count

    def __gt__(self, other):
        """Возвращает буллв тип при операции сравнения Больше"""
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other):
        """Возвращает буллв тип при операции сравнения Больше или Равно"""
        return self.subscribers_count >= other.subscribers_count

    def __lt__(self, other):
        """Возвращает буллв тип при операции сравнения Меньше"""
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        """Возвращает буллв тип при операции сравнения Меньше или Равно"""
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other):
        """Возвращает буллв тип при операции сравнения Равенства"""
        return self.subscribers_count == other.subscribers_count


    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscribers_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = (youtube.channels().list(id=self.channel_id, part='snippet,statistics'))
        response = channel.execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))
