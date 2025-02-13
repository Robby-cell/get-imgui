#!/usr/bin/env python3

import urllib.request
from sys import argv
import os

if len(argv) < 2:
    raise Exception("Invalid args supplied. supply a backend")

branch = "master"

backends = []

get_branch = False
for arg in argv[1:]:
    if get_branch:
        branch = arg
        get_branch = False
    else:
        if arg == "--tag" or arg == "-t":
            get_branch = True
        else:
            backends.append(arg)

if branch == "master":
    root = f"raw/refs/heads/master"
else:
    root = f"raw/refs/tags/{branch}"

base_link= f"https://github.com/ocornut/imgui/{root}"

def fetch(link: str, output: str | None):
    res = urllib.request.urlretrieve(link, output)
    return res[0]

if not os.path.exists("backends"):
    os.makedirs("backends")

for backend in backends:
    base, file_name = f"{base_link}/backends/", f"imgui_impl_{backend}"
    cpp_file = file_name + ".cpp"
    h_file = file_name + ".h"
    
    fetch(base + cpp_file, f"backends/{cpp_file}")
    fetch(base + h_file, f"backends/{h_file}")

sources = ("imconfig.h",
    "imgui.cpp",
    "imgui.h",
    "imgui_demo.cpp",
    "imgui_draw.cpp",
    "imgui_internal.h",
    "imgui_tables.cpp",
    "imgui_widgets.cpp",
    "imstb_rectpack.h",
    "imstb_textedit.h",
    "imstb_truetype.h")

for source in sources:
    link = f"{base_link}/{source}"

    fetch(link, source)
