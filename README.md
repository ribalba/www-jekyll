# HotCarbon website

The [HotCarbon website](https://hotcarbon.org) is a static site built with [Jekyll](https://jekyllrb.com/).
It uses its own small layouts and one plain CSS file. There is no theme, no JavaScript and no web font.

## Where things live

```
_config.yml              current_edition: the year shown on the home page
_data/editions.yml       one entry per year: dates, location, deadlines, chairs, contact, committee, links
_data/program/yYYYY.yml  sessions, keynotes and papers of one year
_data/people.yml         steering committee and publicity chair
_posts/                  news items, shown on the home page and on /news/
YYYY/index.md            /YYYY/        overview and program of that year
YYYY/cfp.md              /YYYY/cfp/    call for papers of that year
YYYY/attend.md           /YYYY/attend/ registration and venue of that year
pages/                   organizers, past editions, news, redirects for old URLs
_layouts/, _includes/    HTML templates
assets/css/hotcarbon.css all styling
```

Every year gets its own URLs, so nothing is overwritten. The main navigation always points to the newest call for papers, program and attend page.
The old URLs `/cfp`, `/program`, `/register` and `/orga` redirect there.

## Starting a new edition

1. Add an entry for the new year at the top of `_data/editions.yml` and set `current_edition` in `_config.yml`.
2. Create the folder `YYYY/` by copying the previous year. Set `edition: YYYY` in the front matter of each file and update the text of `cfp.md` and `attend.md`.
3. When the program is ready, add `_data/program/yYYYY.yml`. The program shows up on `/YYYY/` automatically.

## Build locally

```
bundle install
bundle exec jekyll serve
```
