# PlaceBot-vim

Draws vim logo to www.reddit.com/r/place.

Forked from https://github.com/goatgoose/PlaceBot - thanks!!

Re-downloads desired target pixel data from
https://github.com/stingray300k/placebot/blob/vim/out.cfg before each
attempt to place a tile.

Open an issue/PR or let us know in our
[Reddit thread](https://www.reddit.com/r/vim/comments/ttrhtk/opportunity_for_vim_logo_on_rplace/)
if you have any suggestions.


Installation & usage (probably best done from within a temporary virtualenv):

```bash
pip3 install git+https://github.com/stingray300k/PlaceBot-vim
REDDIT_USER="your_username" REDDIT_PW="your_password" place-vim
```

Because it can still crash due to bugs (which are often resolved by simply
starting it again), it might make sense to put this into an infinite loop once
you've made sure that it works once:

```bash
while true; do REDDIT_USER="your_username" REDDIT_PW="your_password" place-vim; done
```
