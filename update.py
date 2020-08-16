#!/usr/bin/env python3.8

import argparse
import json
import os
import pprint



parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true") # whether to open every entry in browser for viewing
parser.add_argument("--push", action="store_true") # whether to automatically push the changes after updating
args = parser.parse_args()

file = open("catlist.nsv", "r")
catlist = file.read()
file.close()
catlist = catlist.split("\n")
catlist.remove("")
old_length = len(catlist)

# grab the latest log of bot steamids
os.system("cp /tmp/`ls -t /tmp | grep cathook.*[0-9]\\.log | head -n 1` log.txt")

file = open("log.txt", "r")
log = file.read()
file.close()

lines = log.split("\n")

entries = []
for line in lines:
	try:
		entries.append(line.split("Bot steamid entry: ")[1])
	except: # not an entry log line
		pass
entries.remove("0")
entries.sort()
message = f"Added {len(entries) - old_length} entries. There are now {len(entries)} entries."
print(message)

file = open("catlist.csv", "a")
if old_length > 0: # only write new entries
	for entry in entries[old_length:]:
		if args.check:
			os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry}\n")
	file.close()
else: # write all
	for entry in entries:
		if args.check:
			os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry}\n")
	file.close()


data = {"$schema": "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/schemas/v3/playerlist.schema.json"}
data["file_info"] = {
                     "authors": ["milenko"],
                     "description": "List of automatically detected cathook users",
                     "title": "Milenko's cathook list",
                     "update_url": "https://incontestableness.github.io/catlist/milenko-list.json"
}

catlist = []
for entry in entries:
	catlist.append({
			"steamid": f"[U:1:{entry}]",
			"attributes": ["cheater"],
			})

data["players"] = catlist

file = open("milenko-list.json", "w")
file.write(json.dumps(data, indent=4))
file.close()


if args.push: 
	os.system("git add catlist.csv milenko-list.json")
	os.system(f"git commit -m \"{message}\"")
	os.system("git push")
