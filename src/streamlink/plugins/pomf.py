import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import useragents
from streamlink.stream import HTTPStream
from streamlink.stream import HLSStream


log = logging.getLogger(__name__)


@pluginmatcher(re.compile(
    r'https?://pomf\.tv/stream/(?P<channel>[^/]+)'
))
class Pomf(Plugin):

    def _get_streams(self):
        channel = self.match.group("channel")
        self.session.http.headers.update({'User-Agent': useragents.CHROME, 'Referer': self.url})
        flv_url= "https://server2.pomf.tv/srs/live/{}.flv".format(channel)
        yield "live", HTTPStream(self.session, flv_url)
        p720_url = "https://server2.pomf.tv/hls-live/{}_hd720/index.m3u8".format(channel)
        yield "720p", HLSStream(self.session, p720_url)


__plugin__ = Pomf
