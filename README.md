# wifi-bf
> \[LINUX ONLY\] A (completely native) python3 wifi brute-force attack using the 100k most common passwords (2021)

<br />

_This script is purely for educational use. Any consequenses or damages arising from the usage of it in an illegal or unethical way are purely the fault of the end-user, and in no way is the developer responsible for it._

<br />

### Usage
#### Starting
Via python (direct)
```bash
$ cd path/to/wifi-bg/src
$ python3 __main__.py
```

#### Commands
wifi-bf has som optional flags/commands that change change its default behaviours. Below is the list given by ``__main__.py --help``:
```
optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The url that contains the list of passwords
  -f FILE, --file FILE  The file that contains the list of passwords
  -b BSSID, --bssid BSSID  The target BSSID
  -v, --verbose         Optional: Use to show all passwords attempted, rather than just the successful one.
```

#### Attacking/Screenshots
After starting the program, a menu will appear containing all available nearby networks.
![Start Menu](https://i.imgur.com/RWAIroT.png)

From there, just enter the number network to attack, and a menu like below will appear. 
![Running Output](https://i.imgur.com/wNEu8Ya.png)

The colors output by the program mean the following:
**Color Code Information**
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `Password Failed, Unhandled Error`
- ![#00af87](https://via.placeholder.com/15/00af87/000000?text=+) `Password Cracked`
- ![#5f00ff](https://via.placeholder.com/15/5f00ff/000000?text=+) `Testing (password)`

#### Credits
Wordlist: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt

<br />

### License
```
Copyright 2021 Finn Lancaster

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
