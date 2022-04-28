# hk-volcon

Control your computer's sound volume with HomeKit on Windows, macOS and Linux!

![Demonstration of hk-volcon](demo.gif)

If you experience any problems or instructions are unclear please open a new issue.

## Install
- python3 is required, [get it if you don't have it](https://www.python.org/downloads/)
- `git clone` the project into a directory where you don't mind it staying
- create a new virtual environment to install dependencies. from the project dir do:
  - windows (powershell): `python -m venv ./venv` and activate with `./venv/Scripts/Activate.ps1`
  - linux/mac: `virtualenv -p python3 venv` and activate with `source venv/bin/activate`
- install the correct dependencies for your machine's OS with one of:
  - `pip install -r requirements/windows.txt`
  - `pip install -r requirements/macos.txt`
  - `pip install -r requirements/linux-pulse.txt`
- you can try hk-volume out by running `python main.py` from within the virtual environment (see [Known Issues](#known-issues) in case of problems)
- in your home app, you will need to pair the new device. the pairing code can be found in `stdout-stderr.log`, generated in the project directory

### Windows Service
- Download [nssm](https://nssm.cc/download) 
    - extract zip
- copy nssm.exe into project dir
- get the path of the virtual environment's python with `(Get-Command python).source`
- You need a admin privileged cmd instance
- replace the below paths with the correct locations on your machine and execute them 
```cmd
nssm.exe install hk-volcon "C:\Users\tan\Desktop\hk-volcon\venv\Scripts\python.exe" "C:\Users\tan\Desktop\hk-volcon\main.py"
nssm.exe set hk-volcon AppStdout "C:\Users\tan\Desktop\hk-volcon\stdout_stderr.log"
nssm.exe set hk-volcon AppStderr "C:\Users\tan\Desktop\hk-volcon\stdout_stderr.log"
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

#### Uninstall
```bash
systemctl --user stop hk-volcon.service
systemctl --user disable hk-volcon.service
rm ~/.config/systemd/user/hk-volcon.service
# delete project directory
```

### extras
I use a dual-boot setup on a single machine between Windows and Ubuntu. Creating the server.json on one OS and using it on the other as well allows for adding a single device to the Home app while controlling the volume for both OS's.

## Program Arguments
- `-f` Override file name of the config json file. Defaults to `server.json`.
- `-n` Override display name of the device. Defaults to `hk-volcon` (can also be changed later in control center).
- `-p` Override TCP port to use. Defaults to 56565
- `-ip` Override IP address of local machine. Use this when the correct IP could not be detected.

## Known issues
- The volume slider will show up as a lightbulb in your control center.
- After booting the computer the iOS device may need some time (1-2 minutes) to connect to the homekit server
- If you use hk-volcon on more than one machine at the same time you may need to provide different names for either of the instances
- Sometimes it can be difficult to detect the correct IP address for your machine. A `-ip` flag allows for manually overriding your ip address.
