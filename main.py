from os.path import exists
import re

colors = {
    "okay": '\033[94m',
    "fail": '\033[91m',
    "end": '\033[0m',
    "success": '\033[92m',
    "info": '\033[96m',
    "prompt": '\033[95m'
}

f = input(f'{colors["prompt"]}Enter playlist location \n {colors["end"]}')
reg = re.compile(r'"(.+)"')
found = reg.findall(f)
f = found[0] if len(found) > 0 else f

while not exists(f):
    print()
    f = input(f'{colors["fail"]}Error: Playlist not found. {colors["end"]}  Please enter a valid playlist location {colors["info"]}\nHint: On Windows you can right-click on the playlist while holding SHIFT then select "copy as path". Paste the path into with CTRL-SHIFT-V.{colors["end"]} \nType "exit" to exit  \n')
    
    if f.lower() == "exit":
        exit()

    reg = re.compile(r'"(.+)"')
    found = reg.findall(f)
    
    f = found[0] if len(found) > 0 else f

extRgx = re.compile(r"\.(\w+)$")
ext = extRgx.findall(f)[0]
nameRgx = re.compile(r"(.+)\.\w+$")
filename = nameRgx.findall(f)[0]

mode = ""

while mode.lower() != "y" and mode.lower() != "n":
    mode = input(f'{colors["prompt"]}Would you like to remove duplicates as well? (y/n) {colors["end"]}\n')
    if mode.lower() == "exit":
        exit()

files = []

if mode.lower() == "y":
    files = set()
    with open(f) as file:
        for line in file:
            line = line.replace('\n', '')
            if exists(line):
                files.add(line) 

else:
    with open(f) as file:
        for line in file:
            line = line.replace('\n', '')
            if exists(line):
                files.append(line)

newname = f"{filename} - CLEANED.{ext}"

with open(newname, 'w', encoding='UTF8') as newFile:
    for item in files:
        newFile.write(item + '\n')

print(f"{colors['success']}Playlist cleaned. Output stored at {newname} {colors['end']}")