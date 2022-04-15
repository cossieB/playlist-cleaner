from os.path import exists
import re
from random import randint

colors = {
    "okay": '\033[94m',
    "fail": '\033[91m',
    "end": '\033[0m',
    "success": '\033[92m',
    "info": '\033[96m',
    "prompt": '\033[95m'
}

def remove_quotes(inp):   
    reg = re.compile(r'"(.+)"')
    found = reg.findall(inp)
    return found[0] if len(found) > 0 else inp

f = input(f'{colors["prompt"]}Enter playlist location {colors["end"]}\n{colors["info"]}Supported formats: m3u, pls, asx {colors["end"]}\n')
f = remove_quotes(f)

while not exists(f):
    print()
    f = input(f'{colors["fail"]}Error: Playlist not found. {colors["end"]}  Please enter a valid playlist location {colors["info"]}\nHint: On Windows you can right-click on the playlist while holding SHIFT then select "copy as path". Paste the path into the terminal with CTRL-SHIFT-V.{colors["end"]} \nType "exit" to exit  \n')
    
    if f.lower() == "exit":
        exit()

    f = remove_quotes(f)

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

def get_filenames(regexPattern, searchString):
    rgx = re.compile(regexPattern)
    found = rgx.findall(searchString)
    return found[0] if len(found) > 0 else ""

with open(f) as file:
    for line in file:
        line = line.replace('\n', '')

        if ext == "pls":
            line = get_filenames(r"\=(.+)", line)
        
        if ext == "asx":
            line = get_filenames(r'= "(.+)"', line)

        if exists(line):
            if line in files and mode.lower() == "y":
                continue
            files.append(line)


newname = f"{filename} - CLEANED {randint(100, 9999)}.{ext}"

with open(newname, 'w', encoding='UTF8') as newFile:
    if (ext == "m3u"):
        for item in files:
            newFile.write(item + '\n')
    
    elif (ext == "pls"):
        newFile.write("[playlist]\n")
        for  idx in range(len(files)):
            newFile.write(f"File{idx+1}={files[idx]}\n")
        newFile.write(f'NumberOfEntries={len(files)}\nVersion=2')

    elif (ext == "asx"):
        newFile.write('<ASX version = "3.0">\n')
        for item in files:
            newFile.write(f'<Entry><Ref href = "{item}"/></Entry>\n')
        newFile.write('</ASX>')

print(f"{colors['success']}Playlist cleaned. Output stored at {newname} {colors['end']}")