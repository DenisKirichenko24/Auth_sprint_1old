from dataclasses import dataclass
import aiohttp
import pytest
import redis
import requests
from multidict import CIMultiDictProxy
from requests.structures import CaseInsensitiveDict

from .settings import TestSettings

settings = TestSettings()


@dataclass
class HTTPResponse:
    body: dict
    headers: any
    status: int


@pytest.fixture
def make_get_request():
    def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = settings.base_api + method
        # async with session.get(url, params=params) as response:
        #     return HTTPResponse(
        #         body=await response.json(),
        #         headers=response.headers,
        #         status=response.status,
        #     )
        response = requests.get(url, params=params)
        return HTTPResponse(
            body=response.json(),
            headers=response.headers,
            status=response.status_code
        )

    return inner


@pytest.fixture
def make_post_request():
    def inner(method: str, params: dict = None,
              data: dict = None, headers: dict = None) -> HTTPResponse:
        params = params or {}
        url = settings.base_api + method
        # async with session.get(url, params=params) as response:
        #     return HTTPResponse(
        #         body=await response.json(),
        #         headers=response.headers,
        #         status=response.status,
        #     )
        response = requests.post(url, params=params, data=data, headers=headers)
        print(response.json())
        # return HTTPResponse(
        #     body=response.json(),
        #     headers=response.headers,
        #     status=response.status_code
        # )
        return response

    return inner


@pytest.fixture(scope="session")
def redis_client():
    return redis.Redis(
        settings.redis_host, settings.redis_port
    )  # type: ignore
