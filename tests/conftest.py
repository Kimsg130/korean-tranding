"""
Configuration for YouTube router tests
Author: sg.kim
Date: 2025-04-24
"""
import pytest
import os

# Automatically set environment variables for all tests
@pytest.fixture(scope="session", autouse=True)
def setup_env_vars():
    os.environ["YOUTUBE_API_KEY"] = "testkey"
    os.environ["YOUTUBE_API_BASE_URL"] = "https://youtube.googleapis.com/youtube/v3"
    yield
    os.environ.pop("YOUTUBE_API_KEY", None)
    os.environ.pop("YOUTUBE_API_BASE_URL", None)
