#!/bin/sh
''''exec "$(dirname "$0")/env/bin/python" "$0" "$@" # '''
# lines above let this be executed as a script but run with the virtual env! :D

###
## turns a markdown file into a preaching script (see the `template.typ` file for specifics)
###

import os
import json
import subprocess
import sys

USAGE = "usage: render.py [--web] [--config <config.json>] <file.md>"
def fail(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)

web = False
filepath = None
configpath = None

args = sys.argv[1:]
while args:
    arg = args.pop(0)
    if arg == "--web":
        web = True
    elif arg == "--config":
        if not args:
            fail(USAGE)
        configpath = args.pop(0)
    elif arg.startswith("--"):
        fail(f"unknown option: {arg}\n{USAGE}")
    elif filepath is None:
        filepath = arg
    else:
        fail(USAGE)

if filepath is None:
    fail(USAGE)

filepath = os.path.abspath(filepath)
if not os.path.exists(filepath):
    fail(f"no such file: {filepath}")

if configpath is not None:
    configpath = os.path.abspath(configpath)
    if not os.path.exists(configpath):
        fail(f"no such config file: {configpath}")
else:
    local_conf = os.path.abspath("config.json")
    if os.path.exists(local_conf):
        configpath = local_conf


script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)


def load_settings():
    def_path = os.path.join(script_directory, "defaults.json")
    if not os.path.exists(def_path):
        fail(f"missing defaults file!!!")
    settings = json.load(open(def_path))
    if configpath is None:
        return settings

    conf = json.load(open(configpath))

    # reject unknown settings
    for section_name, section_values in conf.items():
        if section_name not in settings:
            fail(f"{configpath}: unknown section {section_name}")
        for setting_name, value in section_values.items():
            if setting_name not in settings[section_name]:
                fail(f"{configpath}: unknown setting {section_name}.{setting_name}")
            settings[section_name][setting_name] = value

    return settings

def to_pandoc_vars(settings):
    arguments = []
    for name, value in settings.items():
        if value is False:
            continue # just omit false bools; that's how oandoc rolls
        if value is True:
            value = "true"
        arguments += ["--variable", f"{name}={value}"]
    return arguments

settings = load_settings()

base = os.path.splitext(os.path.basename(filepath))[0]
fdir = os.path.dirname(filepath)

if web:
    extension = "html"
    opts = [
        "--to", "html",
        "--standalone",
        "--embed-resources",
        "--template", "./template.html",
        *to_pandoc_vars(settings["web"]),
    ]
else:
    extension = "pdf"
    opts = [
        "--to", "pdf",
        "--pdf-engine", "typst",
        "--template", "./template.typ",
        *to_pandoc_vars(settings["pdf"]),
    ]

cmd = [
    "pandoc",
    "--from", "markdown",
    *opts,
    "-o", os.path.join(fdir, f"{base}.{extension}"),
    filepath
]

subprocess.check_call(cmd)
