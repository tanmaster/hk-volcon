# hk-volcon

Control your Windows PC Volume from you iOS Device's Control Center!

## Install as a Windows Service
- python3 is required, get it if you don't have it
- git clone project
- install requirements with `pip install -r requirements.txt`
- Download [nssm](https://nssm.cc/download) 
    - extract zip
- copy desired nssm.exe into project dir
- ```where python```
- You need a admin privileged cmd instance
```cmd
nssm.exe install hk-volcon "C:\Users\tan\PycharmProjects\hk-volcon\venv\Scripts\python.exe" "C:\Users\tan\PycharmProjects\hk-volcon\main.py"
nssm.exe set hk-volcon AppStdout "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe set hk-volcon AppStderr "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe start hk-volcon
```

## Uninstall
```cmd
nssm.exe stop hk-volcon
nssm.exe remove hk-volcon confirm
delete project directory
```

## Known issues
The volume slider will show up as a lightbulb in your controlcenter.
