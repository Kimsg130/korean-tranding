"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from app.schema.public import YoutubeVideo, YoutubeComment
from app.utils.text import TextUtils


class NlpBusinessService:

    def __init__(self):

        self._chat = ChatOllama(
            base_url="http://43.201.175.225:11434",
            temperature=0.5,
            model="gemma3:12b"
        )


    async def identify_korean_wave_for_video(self, videos: list[YoutubeVideo]):
        template = """
        You are a content analyst specialized in identifying whether YouTube videos belong to the "Korean Wave" (한류) phenomenon.
        Note: "한류" (Hallyu) refers to the global popularity of South Korean culture, including K-pop, 드라마, 영화, 음악, 패션, 음식 등.
        
        Below is the metadata for multiple videos. Please analyze each video and determine if it belongs to the Korean Wave.
        
        {videos_data}
        
        > **Respond with a JSON array only. Do NOT include any markdown (```), tags like "json", or extra text**.
        > The response **must** start with `[` and end with `]`, with each item being a JSON object containing exactly these three keys:
        1. `"video_id"`: The ID of the video being analyzed.
        2. `"korean_wave_yn"`: `"Y"` or `"N"`.
        3. `"reason"`: concise rationale in Korean.
        
        Example output (nothing else):
        [
            {{
                "video_id": "abc123",
                "korean_wave_yn": "Y",
                "reason": "여기에 이유를 적어주세요"
            }},
            {{
                "video_id": "def456",
                "korean_wave_yn": "N", 
                "reason": "한국 문화와 관련이 없는 콘텐츠입니다"
            }}
        ]
        """

        # Prepare the videos data for batch processing
        videos_data = ""
        for i, video in enumerate(videos):
            videos_data += f"""
            ===========================================================
            Video ID: {video.video_id}
            Title: {TextUtils.unescape_control_chars(video.title)}
            Description: {TextUtils.unescape_control_chars(video.description)}
            Channel Title: {video.channel_title}
            ===========================================================
            """

        prompt = PromptTemplate(
            input_variables=["videos_data"],
            template=template
        )

        chain = prompt | self._chat

        result = await chain.ainvoke({
            "videos_data": videos_data
        })

        return TextUtils.parse_response_with_regex(result.content)

    async def identify_sentiment_for_comments(self, comments: list[YoutubeComment]):
        """
        Analyze each comment to classify sentiment (긍정/부정/중립) and extract normalized keywords.
        Keywords should be returned as a comma-separated string without brackets (e.g., "music,kpop").
        Return a list of dicts:
        {
            'comment_id': str,
            'sentiment': 'positive'|'negative'|'neutral',
            'keywords': str  # comma-separated keywords
        }.
        """
        # Build clearly separated comment blocks
        comment_blocks = []
        for idx, comment in enumerate(comments, start=1):
            block = (
                f"=============== Comment #{idx} ================\n"
                f"Comment ID: {comment.comment_id}\n"
                f"Like Count: {comment.like_count}\n"
                f"Text: {TextUtils.unescape_control_chars(comment.text_display or '')}\n"
                f"============================================"
            )
            comment_blocks.append(block)
        comments_data = "\n".join(comment_blocks)

        template = """
        You are a sentiment and keyword extraction assistant specialized for YouTube comment data.
        For each comment block below, classify sentiment and extract keywords.
        Keywords should be output as a comma-separated string without brackets, all lowercase.
        
        {comments_data}
        
        > **Respond with a JSON array only. Do NOT include any markdown, tags, or extra text.**
        > The response **must** start with '[' and end with ']'.
        > Each array item must be a JSON object with exactly three keys:
        > 1. "comment_id": the ID of the comment.
        > 2. "sentiment": one of "긍정", "부정", or "중립".
        > 3. "keywords": a comma-separated string of keywords (e.g., "music,kpop").
        
        Example output (nothing else):
        [
            {{"comment_id":"cmt123","sentiment":"긍정","keywords":"music,kpop"}},
            {{"comment_id":"cmt456","sentiment":"중립","keywords":"travel,vlog"}}
        ]
        """
        prompt = PromptTemplate(
            input_variables=["comments_data"],
            template=template
        )
        chain = prompt | self._chat
        result = await chain.ainvoke({"comments_data": comments_data})
        # parse_response should extract pure JSON
        return TextUtils.parse_response_with_regex(result.content)