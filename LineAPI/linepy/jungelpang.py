# -*- coding: utf-8 -*-
from datetime import datetime
from .channel import Channel

import json, time, base64

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isSupportJungelpang:
            if args[0].isLogin:
                return func(*args, **kwargs)
            else:
                args[0].callback.other('You want to call the function, you must login to LINE')
        else:
            args[0].callback.other('Your LINE account is not support Jungelpang')
    return checkLogin

class Jungelpang(Channel):
    isSupportJungelpang = False

    def __init__(self):
        try:
            self.isSupportJungelpang = True
            Channel.__init__(self, self.channel, self.server.CHANNEL_ID['JUNGEL_PANG'], False)
            self.jp = self.getChannelResult()
            self.__loginJungelpang()
        except:
            self.isSupportJungelpang = False
            self.log('Your LINE account is not support Jungelpang')

    def __loginJungelpang(self):
        self.server.setJungelpangHeadersWithDict({
            'Content-Type': 'application/json',
            'User-Agent': self.server.USER_AGENT,
        })
        self.profileDetail = self.getProfileDetail()

    """Jungelpang"""

    @loggedIn
    def postJungelpang(self, to, messages={}):
        data = {
            "cc": self.jp.token,
            "to": to,
            "messages": [messages]
        }
        data = json.dumps(data)
        sendPost = self.server.postContent(self.server.LINE_JUNGEL_PANG, data=data, headers=self.server.JungelpangHeaders)
        return sendPost.json()