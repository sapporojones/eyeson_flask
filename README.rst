

******
eyeson
******

A tool to view at-a-glance info about an arbitrary solar system in EVE Online.

Description
###########

One day I was on a roam in EVE Online, my ye olde pastime of feeding aggressively ships I can't afford.
I found myself near a system that seemed like it was heavily trafficked by hostiles, and
I wanted a fast way to get information about that solar system from several sources at once.

The next day I woke up and started on this as a personal project but decided to put it up in the hopes
someone might find it useful.

Installation
############

* Clone this repo via git clone.
* `cd` in to the directory you cloned the repo to and then `cd` to the `eyeson_flask` directory.
* run `pytest` if you need confirmation of your faith in my abilities
* run `flask run` then navigate your browser to `http://127.0.0.1:5000`

Usage
#####

The search bar accepts partial system names and just pulls the closest match.  If there are 500 errors it's because ccp not me I swearsies.