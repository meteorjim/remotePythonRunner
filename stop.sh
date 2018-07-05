ps aux|grep 'python -u WebServer.py'|grep -v grep|awk '{print $2}'|xargs kill -9
