#!/usr/bin/env python3
from dataclasses import dataclass
import os
from place_bot import Placer, Color
from pprint import pprint
import random
import requests
from time import sleep
from traceback import print_exc


class LoginError(Exception):
    pass


class PlaceError(Exception):
    pass


@dataclass
class RedditCredentials:
    username: str
    password: str


# contains pixel data for desired image:
cfg_url = "https://raw.githubusercontent.com/stingray300k/placebot/vim/out.cfg"
# for checking for updates (don't worry, will never update automatically):
setup_py_url = (
    "https://raw.githubusercontent.com/stingray300k/PlaceBot-vim/vim/setup.py"
)


def get_installed_version():
    import pkg_resources

    return pkg_resources.require("PlaceBot-vim")[0].version


def get_latest_version():
    r = requests.get(setup_py_url)
    stripped_lines = [line.strip() for line in r.text.splitlines()]
    version = [
        line.split("=")[1].strip("'\",")
        for line in stripped_lines
        if line.startswith("version")
    ][0]
    return version


def check_for_new_version():
    print("checking for new script version... ", end="")
    try:
        installed_version = get_installed_version()
        latest_version = get_latest_version()
        if installed_version != latest_version:
            print(
                f"\nnew version available: "
                f"{latest_version} (you have {installed_version})\n"
                "consider updating via:\n"
                "pip3 install -U "
                "git+https://github.com/stingray300k/PlaceBot-vim"
            )
        else:
            print("up to date")
    except Exception:
        print("")
        print_exc()
        print("checking for new version failed (see error message above)")


def login(placer: Placer, credentials: RedditCredentials):
    print("logging in... ", end="")
    try:
        placer.login(credentials.username, credentials.password)
    except Exception as e:
        raise LoginError("error while logging in") from e
    print("done")


def download_target_image_cfg():
    print("downloading target image config... ", end="")
    pixels_cfg = requests.get(cfg_url).json()["pixels"]
    print("done")
    return pixels_cfg


def place_tile(placer, **place_tile_kwargs):
    print("placing tile... ", end="")
    try:
        placer.place_tile(**place_tile_kwargs)
    except Exception as e:
        raise PlaceError("error while placing tile") from e
    print("done")


class VimLogoPlacer:
    def __init__(self):
        self.placer = Placer()
        self.credentials = RedditCredentials(
            username=os.environ["REDDIT_USER"],
            password=os.environ["REDDIT_PW"],
        )

    def place_tile_with_retries(self, **place_tile_kwargs):
        for i in range(2):  # retries with new login attempts
            for j in range(3):  # retries without new login attempts
                try:
                    place_tile(self.placer, **place_tile_kwargs)
                    return
                except PlaceError:
                    print("error trying to place tile, retrying in 5 seconds")
                    sleep(5)
            try:
                print("trying to log in again before next retry")
                self.placer = Placer()
                login(self.placer, self.credentials)
            except LoginError:
                pass  # just retry later if login fails at this point
        print("giving up")

    def run_loop(self):
        # run these once at the start without retry logic
        login(self.placer, self.credentials)
        pixels_cfg = None

        while True:
            check_for_new_version()

            try:
                pixels_cfg = download_target_image_cfg()
            except Exception:
                if pixels_cfg is not None:
                    print("downloading target image failed, reusing old one")
                else:
                    raise

            pixel_cfg = random.choice(pixels_cfg)
            place_tile_kwargs = {
                "x": pixel_cfg["x"],
                "y": pixel_cfg["y"],
                "color": Color.from_id(pixel_cfg["color_index"]),
            }
            print("will try to draw tile:")
            pprint(pixel_cfg)

            self.place_tile_with_retries(**place_tile_kwargs)

            print("sleeping for 5 minutes and 10 seconds")
            sleep(5 * 60 + 10)


def main():
    vim_logo_placer = VimLogoPlacer()
    vim_logo_placer.run_loop()


if __name__ == "__main__":
    main()
