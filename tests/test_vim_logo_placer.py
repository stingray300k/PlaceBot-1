import os
from time import sleep
from unittest.mock import create_autospec, patch

import pytest
import requests

from place_bot import Color, Placer
from place_vim import VimLogoPlacer, cfg_url, check_for_new_version


@pytest.fixture()
def fake_reddit_credentials_env():
    os.environ["REDDIT_USER"] = "fakeuser"
    os.environ["REDDIT_PW"] = "fakepw"
    yield
    del os.environ["REDDIT_USER"]
    del os.environ["REDDIT_PW"]


@pytest.fixture()
def mocked_sleep():
    with patch("place_vim.sleep", create_autospec(sleep)) as mocked_sleep:
        yield mocked_sleep


@pytest.fixture()
def mocked_requests():
    with patch(
        "place_vim.requests", create_autospec(requests)
    ) as mocked_requests:
        yield mocked_requests


@pytest.fixture()
def mocked_version_check():
    with patch(
        "place_vim.check_for_new_version",
        create_autospec(check_for_new_version),
    ) as mocked_version_check:
        yield mocked_version_check

@pytest.fixture()
def mocked_placer_cls():
    with patch(
        "place_vim.Placer",
        create_autospec(Placer),
    ) as mocked_placer_cls:
        yield mocked_placer_cls

class RaiseAfterIterations:
    def __init__(self, n):
        self.it = range(n).__iter__()

    def __call__(self, *args, **kwargs):
        self.it.__next__()


def test_loop_without_errors(
    fake_reddit_credentials_env,
    mocked_sleep,
    mocked_requests,
    mocked_version_check,
    mocked_placer_cls
):
    # hack to stop infinite loop (TODO implement condition instead)
    mocked_version_check.side_effect = RaiseAfterIterations(5)

    mocked_response = create_autospec(requests.Response)
    mocked_response.json.return_value = {
        "pixels": [{"x": 1, "y": 2, "color_index": 15}]
    }
    mocked_requests.get.return_value = mocked_response

    mocked_version_check.side_effect = RaiseAfterIterations(5)

    vlp = VimLogoPlacer()

    with pytest.raises(StopIteration):
        vlp.run_loop()

    assert mocked_sleep.call_count == 5
    mocked_sleep.assert_called_with(20 * 60 + 10)

    assert mocked_requests.get.call_count == 5
    mocked_requests.get.assert_called_with(cfg_url)

    assert vlp.placer.place_tile.call_count == 5
    vlp.placer.place_tile.assert_called_with(x=1, y=2, color=Color.from_id(15))


def test_loop_with_expected_errors(
    fake_reddit_credentials_env,
    mocked_sleep,
    mocked_requests,
    mocked_version_check,
    mocked_placer_cls
):
    # hack to stop infinite loop (TODO implement condition instead)
    mocked_version_check.side_effect = RaiseAfterIterations(1)

    vlp = VimLogoPlacer()
    vlp.placer.place_tile.side_effect = AssertionError

    with pytest.raises(StopIteration):
        vlp.run_loop()

    assert mocked_placer_cls.call_count == 3  # TODO should be 2, minor bug
    assert vlp.placer.place_tile.call_count == 6
