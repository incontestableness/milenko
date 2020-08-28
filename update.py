#!/usr/bin/env python3.8

import argparse
import json
import os
import pprint



parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true") # whether to open every entry in browser for viewing
parser.add_argument("--push", action="store_true") # whether to automatically push the changes after updating
args = parser.parse_args()


# get old size for counting new entries
try:
	file = open("catlist.nsv", "r")
	catlist = file.read()
	file.close()
	catlist = catlist.split("\n")
	catlist.remove("")
	old_length = len(catlist)
except FileNotFoundError:
	old_length = 0

# grab the latest log of bot steamids
os.system("cp /tmp/`ls -t /tmp | grep cathook.*[0-9]\\.log | head -n 1` log.txt")

# generate entry list
file = open("log.txt", "r")
log = file.read()
file.close()

lines = log.split("\n")
entries = []
for line in lines:
	try:
		entry = line.split("Bot steamid entry: ")[1]
		if entry not in entries:
			entries.append(entry)
	except: # not an entry log line
		pass
entries.remove("0")
entries.sort()
message = f"Added {len(entries) - old_length} entries. There are now {len(entries)} entries."
print(message)

# write entries to nsv file
try:
	os.remove("catlist.nsv")
except FileNotFoundError:
	pass
file = open("catlist.nsv", "a")
for entry in entries:
	file.write(f"{entry}\n")
file.close()

# check new steamids
if args.check:
	for entry in entries[old_length:]:
		os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")


# compile the json
data = {"$schema": "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/schemas/v3/playerlist.schema.json"}
data["file_info"] = {
                     "authors": ["milenko"],
                     "description": "List of automatically detected cathook users",
                     "title": "Milenko's cathook list",
                     "update_url": "https://incontestableness.github.io/milenko/playerlist.milenko-list.json"
}

catlist = []
for entry in entries:
	catlist.append({
			"steamid": f"[U:1:{entry}]",
			"attributes": ["cheater"],
			})

data["players"] = catlist

# write the json
file = open("playerlist.milenko-list.json", "w")
file.write(json.dumps(data, indent=4))
file.close()


# update the repo
if args.push: 
	os.system("git add catlist.nsv playerlist.milenko-list.json")
	os.system(f"git commit -m \"{message}\"")
	os.system("git push")
