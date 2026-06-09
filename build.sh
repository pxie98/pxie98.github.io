#!/usr/bin/env sh
set -eu

python3 jemdoc.py index.jemdoc
python3 jemdoc.py research.jemdoc
python3 jemdoc.py publication.jemdoc
python3 jemdoc.py talks.jemdoc
python3 jemdoc.py mentorship.jemdoc
python3 jemdoc.py codes.jemdoc
python3 jemdoc.py blog.jemdoc
python3 jemdoc.py album.jemdoc
