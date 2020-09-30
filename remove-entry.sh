#!/usr/bin/env bash

# This is a bit inconvenient but it works for now and only takes a few minutes so, eh


read -p "Be sure you've stopped the bots with ./stop first. Press Enter to continue."

read -p "Please stop the running live-scrape instance, if any. Press Enter to continue."
tmux a -t live-scrape

# Delete all cathook logs so the entry doesn't get picked back up
pushd /tmp
rm cathook-*.log
popd

# Delete the cathook plist file since I am NOT editing that binary crap from here
# and we don't want bots to just load that entry back in, log it, and have it added to the list again
rm /opt/cathook/data/plist

# Remove the entry from the nsv file so bots don't load it from there, and so the playerlist doesn't include it
cat catlist.nsv | grep -v $1 >catlist_new.nsv

# Update database
mv catlist_new.nsv catlist.nsv
git add catlist.nsv
git commit -m "Remove an entry"

# Verify that the entry was removed from the database
git show

# Update the playerlist
./update.py --playerlist-only

# Verify that the entry was removed from the playerlist
git show
echo "Ready to push commits..."
