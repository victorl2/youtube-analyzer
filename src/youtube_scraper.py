import re
from concurrent.futures import ProcessPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup


class Scrapper():
    def __init__(self, video_id):
        self.video_id = video_id
        request = requests.get('https://www.youtube.com/watch?v=' + video_id)
        self.html = BeautifulSoup(request.content, 'html.parser')
        self.html_str = str(self.html)

        self.tags = self.get_tags()
        self.thumbnail = 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(
            video_id)
        self.title = self.get_title()
        self.description = 'ND'
        self.views = int(self.get_value_between('\\"viewCount\\":\\"', '\\",'))
        self.published = self.get_value_between('\\"publishDate\\":\\"', '\\')

        value = self.get_value_between('likeCount\\":', ',')
        self.like = int(value) if value != 'ND' else 'ND'

        value = self.get_value_between('dislikeCount\\":', ',')
        self.dislike = int(value) if value != 'ND' else 'ND'
        self.category = self.get_value_between('category\\":\\"', '\\')
        self.comments = 'ND'
        self.language = 'ND'
        self.channel_id = self.get_value_between('channelId\\":\\"', '\\')

    def to_list(self):
        return [self.video_id, self.title, self.views, self.like, self.dislike, self.comments, self.thumbnail, self.published, self.category, self.language, self.channel_id, self.tags]

    def get_tags(self):
        tags_text = ''
        for tag in self.html.findAll('meta', {'property': 'og:video:tag'}):
            tags_text += tag['content'] + ','
        return tags_text

    def get_value_between(self, start, end):
        try:
            return (self.html_str.split(start))[1].split(end)[0]
        except Exception:
            return 'ND'

    def get_title(self):
        return self.html.find('meta', {'property': 'og:title'})['content']

    def get_description(self):
        return self.html.find('meta', {'property': 'og:description'})['content']


def parse_video(video_id, thread_id):
    return Scrapper(video_id).to_list()


if __name__ == '__main__':
    ids = ['FCfxwnoMnIA', 'iqItfoEgOyI', 'v8jHgPHL1_w', 'v2xo_B2ucAs']
    with ProcessPoolExecutor(max_workers=4) as executor:
        videos = executor.map(parse_video, ids, range(2))
    print([v for v in videos])
