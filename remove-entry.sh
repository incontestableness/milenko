#!/usr/bin/env bash

# This is very inconvenient but it works for now and only takes a few minutes so, eh


read -p "Be sure you've stopped the bots with ./stop first. Press Enter to continue."

read -p "Please stop the running live-scrape instance, if any. Press Enter to continue."
tmux a -t live-scrape

# Delete the cathook plist file since I am NOT editing that binary crap from here
rm /opt/cathook/data/plist

# Remove the entry
cat catlist.nsv | grep -v $1 >catlist_new.nsv

# Update
mv catlist_new.nsv catlist.nsv
git add catlist.nsv
git commit -m "Remove an entry"

# Verify
git show
echo "Ready to push commit..."
