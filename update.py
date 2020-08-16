#!/usr/bin/env python3.8

import argparse
import json
import os
import pprint
from schema import Optional, Schema



parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true") # whether to open every entry in browser for viewing
args = parser.parse_args()

file = open("catlist.csv", "r")
catlist = file.read()
file.close()
catlist = catlist.split(",")
old_length = len(catlist) - 1 # since there's a trailing comma

# grab the latest log of bot steamids
os.system("cp /tmp/`ls -t /tmp | grep cathook.*[0-9]\\.log | head -n 1` log.txt")

file = open("log.txt", "r")
log = file.read()
file.close()

lines = log.split("\n")
while "" in lines:
	lines.remove("")

entries = []
for line in lines:
	try:
		entries.append(line.split("Bot steamid entry: ")[1])
	except: # not an entry log line
		pass
entries.remove("0")
print(f"Added {len(entries) - old_length} entries. There are now {len(entries)} entries.")

file = open("catlist.csv", "a")
if old_length > 0: # only write new entries
	for entry in entries[old_length - 1:]:
		if args.check:
			os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry},")
	file.close()
else: # write all
	for entry in entries:
		if args.check:
			os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry},")
	file.close()


basic_info = {
	"file_info": {
			"authors": ["milenko"],
			"description": "List of automatically detected cathook users",
			"title": "Milenko's cathook list",
			"update_url": ""
			}
}

catlist = []
for entry in entries:
	catlist.append({
			"steamid": f"{entry}",
			"attributes": ["cheater"],
			"last_seen": {
				"player_name": "",
				"time": 0
				}
			})

data = basic_info
data["players"] = catlist

s = Schema(data)
json_schema = s.json_schema("https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/schemas/v3/playerlist.schema.json")
pprint.pprint(json_schema, width=200)
file = open("milenko-list.json", "w")
file.write(json.dumps(json_schema))
file.close()
