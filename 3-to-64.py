#!/usr/bin/env python3.8

# Lazy script to convert Steam ID3 to Steam64 ID

import os
import subprocess


print("This will take a few minutes, be patient.")

file = open("catlist.nsv", "r")
data = file.read()
file.close()

to_convert = data.split("\n")
to_convert.remove("")
converted = []
for index, id3 in enumerate(to_convert):
	output = subprocess.check_output(f"curl https://steamid.xyz/{id3} 2>&1 | grep Steam64 -A1", shell=True)
	output = output.decode("UTF-8")
	temp = output[output.find("value=\"") + 7:]
	id64 = temp[:temp.find("\">")]
	converted.append(id64)
	print(f"Converted {index + 1}/{len(to_convert)}...")

try: os.remove("catlist.nsv.64")
except: pass
file = open("catlist.nsv.64", "a")
for id64 in converted:
	print(id64)
	file.write(f"{id64}\n")
file.close()

print("Wrote converted list to catlist.nsv.64")
