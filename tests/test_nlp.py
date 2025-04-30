"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
import datetime

import pytest

from app.schema.public import YoutubeVideo
from app.service.business.nlp import NlpBusinessService
from app.utils.text import TextUtils


@pytest.mark.asyncio
async def test_korean_wave():

    nlp = NlpBusinessService()

    videos = [
        YoutubeVideo(
            video_id="dfadf",
            published_at = datetime.datetime.now(),
            channel_id="dkjfkdsjf",
            title="\U0001f30e TITLE \ud2b8\ub7994 : \uc0ac\ub791\uc758\uc774\ub984\uc73c\ub85c! (feat. \uce74\ub9ac\ub098 of aespa) | \uc794\ub098\ube44 \uc815\uaddc 4\uc9d1 'Sound of Music pt.1'",
            description="\U0001f30e D-7\nGroup Sound Jannabi 4th Album\n'Sound of Music pt.1'\n\nTITLE\n\U0001f339 \ud2b8\ub7994: \uc0ac\ub791\uc758\uc774\ub984\uc73c\ub85c! (feat. \uce74\ub9ac\ub098 of aespa)\n\n\u201c\uad74\ud558\uc9c0 \uc54a\ub294 \ubbf8\uc18c\ub294 \uc6b0\ub9ac\uc758 \uc790\ub791\uc774\ub2c8\uae4c\u201d\n\n\u26a1\uadf8\ub8f9\uc0ac\uc6b4\ub4dc \uc794\ub098\ube44 \uc815\uaddc 4\uc9d1\nSound of Music pt.1\n\u27a3 2025.04.28 MON 6PM (KST)\n\n#\uc794\ub098\ube44 #jannabi #\uc0ac\ub791\uc758\uc774\ub984\uc73c\ub85c",
            channel_title="잔나비 JANNABI"
        ),
        YoutubeVideo(
            video_id="k9SLFDfhpQY",
            published_at=datetime.datetime.now(),
            channel_id="dkjfkdsjf2",
            title="Group Sound Jannabi 4th Album\u26a1\ufe0f",
            description="Group Sound Jannabi 4th Album\n\uadf8\ub8f9\uc0ac\uc6b4\ub4dc \uc794\ub098\ube44 \uc815\uaddc 4\uc9d1\n\n\u26a1\ufe0f2025.04.28 MON 6:00PM (KST)",
            channel_title="잔나비 JANNABI"
        ),
    ]

    result = await nlp.identify_korean_wave_for_video(videos)

    print(f"RESULT>>\n{result}")