# BaiskoafuDown

[BaiskoafuDown](https://github.com/MuffenBug/BaiskoafuDown.git) is a simple program to download songs, movies, series from [Baiskoafu](https://baiskoafu.com).
### Installation
Simply clone the repo from git.
```sh
$ git clone https://github.com/MuffenBug/BaiskoafuDown.git
```
### config.py
Login details are required
```python
username = "your email here"    # email
password = "your password here" # password
media_quality(quality='medium') # set quality['high', 'low', 'medium']
ASK_BEFORE_DOWNLOAD = True      # set 'False' to download without prompt
IS_PRIMARY_DEVICE   = True      # set 'True' only if you have premium subscription
```
### Usage
This script requires Python 3.6 or later and the python3 requests module to work. To install this module, run this in your terminal: "python3 -m pip install requests"
```sh
$ python3 -m pip install requests
```

Additionally, you need to have ffmpeg installed on your system. You can install ffmpeg using the following commands:

For Ubuntu/Debian:
```sh
$ sudo apt-get update
$ sudo apt-get install ffmpeg
```

For CentOS/RHEL:
```sh
$ sudo yum install epel-release
$ sudo yum install ffmpeg
```

For macOS with Homebrew:
```sh
$ brew install ffmpeg
```

For Windows:
You can download ffmpeg from ffmpeg.org(https://ffmpeg.org) and add it to your system's PATH.

### Run program
```sh
$ cd BaiskoafuDown
$ python3 baiskoafuDown.py
```
### with an argument
```sh
$ python3 baiskoafuDown.py "name of a song or movie"
```
This is an updated version of the script by proxygod, originally created by R00t173.

### Previous Versions

Version 1.0 by [R00t173](https://github.com/R00t173/BaiskoafuDown) 

Version 2.0 by [proxygod](https://github.com/proxygod/BaiskoafuDown)

Version 3.0 by [MuffenBug](https://github.com/MuffenBug/BaiskoafuDown)