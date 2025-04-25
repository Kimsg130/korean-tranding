"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from app.schema.public import YoutubeVideo
from app.utils.text import TextUtils


class NlpBusinessService:

    def __init__(self):

        self._chat = ChatOllama(
            base_url="http://43.201.175.225:11434",
            temperature=0.5,
            model="gemma3:12b"
        )


    async def identify_korean_wave_for_video(self, video: YoutubeVideo):
        template = """
        You are a content analyst specialized in identifying whether a YouTube video belongs to the “Korean Wave” (한류) phenomenon.  
        Note: “한류” (Hallyu) refers to the global popularity of South Korean culture, including K-pop, 드라마, 영화, 음악, 패션, 음식 등.
        
        Below is the video metadata:
        
        Title: {title}
        Description: {description}
        Channel Title: {channel}
        
        Based only on this information, produce a JSON object with exactly two keys:
        1. "korean_wave_yn": a string, either "Y" or "N", indicating whether this video is related to Hallyu.
        2. "reason": a string giving your concise rationale in Korean.
        
        **Output must be valid JSON and nothing else.**
        
        
        Example of the exact format: 
        {{
            "korean_wave_yn": "Y",
            "reason": "여기에 이유를 적어주세요"
        }}
        
        *** 단, 모든 답변에 "text": "```json 또는 json 이라는 답변은 절대로 넣지 말 것.
        """

        prompt = PromptTemplate(
            input_variables=["title", "description", "channel"],
            template=template
        )

        chain = prompt | self._chat

        result = await chain.ainvoke({
            "title": TextUtils.unescape_control_chars(video.title),
            "description": TextUtils.unescape_control_chars(video.description),
            "channel": video.channel_title
        })
        return result.content