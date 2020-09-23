#!/usr/bin/env bash

tmux new -ds "live-scrape" "./update.py --live-scrape --commit --push"
