#!/usr/bin/env python3.8

import argparse
import json
import os
import pprint



parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true") # whether to open every entry in browser for viewing
parser.add_argument("--commit", action="store_true") # whether to automatically commit the changes after updating
parser.add_argument("--push", action="store_true") # whether to automatically push the changes after updating
args = parser.parse_args()


# Load current database
file = open("catlist.nsv", "r")
catlist = file.read()
file.close()
catlist = catlist.split("\n")
catlist.remove("")
old_length = len(catlist)

# Load exclusion database
file = open("excludes.nsv", "r")
excludes = file.read()
file.close()
excludes = excludes.split("\n")
excludes.remove("")

# Grab the latest log of bot steamids
os.system("cp /tmp/`ls -t /tmp | grep -E cathook-[a-z]{4}-[0-9]*.log | head -n 1` log.txt")
file = open("log.txt", "r")
log = file.read()
file.close()

# Add new entries to the database from the log's plist dump
lines = log.split("\n")
new_entries = []
for line in lines:
	try:
		entry = line.split("Bot steamid entry: ")[1]
		if entry == "0": # invalid steamid
			continue
		if entry not in catlist and entry not in excludes:
			catlist.append(entry)
			new_entries.append(entry)
	except: # not an entry log line
		pass
catlist.sort()
message = f"Added {len(new_entries)} entries. There are now {len(catlist)} entries."
print(message)

# Write updated database to file
os.remove("catlist.nsv")
file = open("catlist.nsv", "a")
for entry in catlist:
	file.write(f"{entry}\n")
file.close()

# Check new steamids
if args.check:
	for entry in new_entries:
		os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")


# Compile the json
data = {"$schema": "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/schemas/v3/playerlist.schema.json"}
data["file_info"] = {
                     "authors": ["The Great Milenko"],
                     "description": "List of automatically detected cathook users",
                     "title": "Milenko's cathook list",
                     "update_url": "https://incontestableness.github.io/milenko/playerlist.milenko-list.json"
}

playerlist = []
for entry in catlist:
	playerlist.append({
			"steamid": f"[U:1:{entry}]",
			"attributes": ["cheater"],
			})

data["players"] = playerlist


# Write the json
file = open("playerlist.milenko-list.json", "w")
file.write(json.dumps(data, indent=4))
file.close()


# Update the repo
if args.commit:
	os.system("git add catlist.nsv playerlist.milenko-list.json")
	os.system(f"git commit -m \"{message}\"")
if args.push:
	os.system("git push")
