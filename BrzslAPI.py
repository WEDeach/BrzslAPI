"""
Version: v1.0.0
Author: YinMo0913 (WEDeach)
DateTime: 2022-04-23
"""

import json
import re
import requests

class BrzslAPI(object):
    URL_B23_VIDEO_ID_REGEX = re.compile(r"b23.tv\/([^\?]+)\??")
    URL_VIDEO_ID_REGEX = re.compile(r"video\/([^\?]+)\??")

    VIDEO_INFO_REGEX = re.compile(r"<script>window.__playinfo__=(.*?)<\/script>")
    VIDEO_INITIAL_STATE_REGEX = re.compile(r"<script>window.__INITIAL_STATE__=(.*?);.*?<\/script>")

    def __init__(self):
        self._session = requests.Session()
        self._sessionCookies = {}
    
    def getVideoInfo(self, video_id: str):
        path = f"/video/{video_id}"
        html_raw = self.read("GET", path).text
        info = re.findall(self.VIDEO_INFO_REGEX, html_raw)[0]
        initial_state = re.findall(self.VIDEO_INITIAL_STATE_REGEX, html_raw)[0]
        return json.loads(info), json.loads(initial_state)
    
    def getVideoIdWithB23(self, b23_id: str):
        b23_id = re.findall(self.URL_B23_VIDEO_ID_REGEX, b23_id)[0]
        print(b23_id)

        url = f"https://b23.tv/{b23_id}"
        raw = self._session.request("GET", url, cookies=self._sessionCookies)
        real_url = raw.url
        video_id = re.findall(self.URL_VIDEO_ID_REGEX, real_url)[0]
        return video_id
    
    def read(self, method: str, path: str):
        url = f"https://www.bilibili.com{path}"
        return self._session.request(method, url, cookies=self._sessionCookies)

if __name__ == '__main__':
    cl = BilibiliClient()

    video_id = cl.getVideoIdWithB23('http://b23.tv/S3sR1j0')

    video_info, video_initial_state = cl.getVideoInfo(video_id)
    print(video_initial_state['videoData']['title'])
    print(video_initial_state['videoData']['desc'])
    print(video_initial_state['videoData']['pic'])
    print(video_info['data']['video_codecid'])
    print(video_info['data']['dash']['video'][0])