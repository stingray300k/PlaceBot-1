# PlaceBot-vim

Draw a small vim logo ![](https://cdn.discordapp.com/attachments/959453006724747328/960102408577499136/placevim-7x7-orig.png) on www.reddit.com/r/place.

Uses https://github.com/goatgoose/PlaceBot to do the actual placing - thanks!!

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
