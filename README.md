# hk-volcon

Control your PC Volume from you iOS Device's Control Center!

## Install
- python3 is required, [get it if you don't have it](https://www.python.org/downloads/)
- `git clone ` to a directory where you don't mind it staying
- create a new virtual environment to install dependencies:
  - windows: `c:\>c:\Python35\python -m venv c:\path\to\myenv` and activate with `C:\> <venv>\Scripts\activate.bat` (path to python can be found with `where python`)
  - linux/mac: `virtualenv -p python3 venv` and activate with `source venv/bin/activate`
- install the correct dependencies for your machine's OS with one of:
  - `pip install -r requirements/windows.txt`
  - `pip install -r requirements/macos.txt`
  - `pip install -r requirements/linux-pulse.txt`

### Windows Service
- Download [nssm](https://nssm.cc/download) 
    - extract zip
- copy desired nssm.exe into project dir
- ```where python```
- You need a admin privileged cmd instance
- replace the below paths with the script locations on your machine and execute them 
```cmd
nssm.exe install hk-volcon "C:\Users\tan\PycharmProjects\hk-volcon\venv\Scripts\python.exe" "C:\Users\tan\PycharmProjects\hk-volcon\main.py"
nssm.exe set hk-volcon AppStdout "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe set hk-volcon AppStderr "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe start hk-volcon
```
- the pairing code is generated once with the initial start and can be found in the `stdout_stderr.log` or in `server.json`

#### Uninstall
```cmd
nssm.exe stop hk-volcon
nssm.exe remove hk-volcon confirm
delete project directory
```

### macOS user agent
- replace the paths in `org.hk-volcon.plist` with the script locations on your machine
- copy plist: `cp org.hk-volcon.plist ~/Library/LaunchAgents`
- load the agent `launchctl load ~/Library/LaunchAgents/org.hk-volcon.plist`
- the script should start automatically as agent
- the pairing code is generated once with the initial start and can be found in the `stdout_stderr.log` or in `server.json`

### linux systemd module
The script relies on ALSA, so it won't work if it is not installed
- replace the absolute paths in `hk-volcon.service` with the script locations on your machine
- create a directory `~/.config/systemd/user/` if it does not exist
- copy the hk-volcon.service: `cp hk-volcon.service ~/.config/systemd/user/`
- `systemctl --user enable hk-volcon.service`
- `systemctl --user start hk-volcon.service`
- the pairing code is generated once with the initial start and can be found in the `stdout_stderr.log` or in `server.json`


### extras
I use a dual-boot setup on a single machine between Windows and Ubuntu. Creating the server.json on one OS and using it on the other as well allows for adding a single device to the Home app while controlling the volume for both OS's.

## Known issues
- The volume slider will show up as a lightbulb in your controlcenter.
- If you use hk-volcon on more than one machine at the same time you may need to provide different names for either of the instances