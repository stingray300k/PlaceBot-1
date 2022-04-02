import os
from place_bot import Placer, Color
import random
import requests
from time import sleep

username = os.environ["REDDIT_USER"]
password = os.environ["REDDIT_PW"]
cfg_url = "https://raw.githubusercontent.com/stingray300k/placebot/vim/out.cfg"

placer = Placer()
while True:
    pixels_cfg = requests.get(cfg_url).json()["pixels"]
    pixel_cfg = random.choice(pixels_cfg)
    place_tile_kwargs = {
        "x": pixel_cfg["x"],
        "y": pixel_cfg["y"],
        "color": Color(pixel_cfg["color_index"]),
    }
    placer.login(username, password)
    placer.place_tile(**place_tile_kwargs)
    sleep(20 * 60)
