#!/usr/bin/env python3.8

import os


file = open("catlist.csv", "r")
catlist = file.read()
file.close()
catlist = catlist.split(",")
old_length = len(catlist)

file = open("log.txt", "r")
log = file.read()
file.close()

lines = log.split("\n")
while "" in lines: 
	lines.remove("")

entries = []
for line in lines: 
	entries.append(line.split(": ")[1])
entries.remove("0")

file = open("catlist.csv", "a")
if old_length > 0: # only write new entries
	for entry in entries[old_length - 1:]: 
		os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry},")
	file.close()
else: # write all
	for entry in entries: 
		os.system(f"~/Desktop/Firefox-Developer-Edition/firefox https://steamid.xyz/{entry}")
		file.write(f"{entry},")
	file.close()
