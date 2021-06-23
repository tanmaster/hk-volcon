# hk-volcon

Control your Windows PC Volume from you iOS Device's Control Center!

## to deploy as service
- python3 is required, get it if you don't have it
- install requirements with `pip install -r requirements.txt`
- git clone project
- Download [nssm](https://nssm.cc/download) 
    - extract zip
- copy desired nssm.exe into project dir
- ```where python```

```cmd
nssm.exe install hk-volcon "C:\Users\tan\PycharmProjects\hk-volcon\venv\Scripts\python.exe" "C:\Users\tan\PycharmProjects\hk-volcon\main.py"
nssm.exe set hk-volcon AppStdout "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe set hk-volcon AppStderr "C:\Users\tan\PycharmProjects\hk-volcon\stdout_stderr.log"
nssm.exe start hk-volcon
```
