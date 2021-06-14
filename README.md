# Chat App

## 0. Create an Environment <EnvironmentName>

```
python3 -m pip install --user virtualenv
python3 -m venv <EnvironmentName>
source <EnvironmentName>/bin/activate
deactivate
```

## 1. Run Server

In one terminal
(This keeps running)
```
python run-server.py
```

## 2. Run Web App on port  <portNo>

In another one
(This keeps running)
```
export FLASK_APP=main.py
flask run --port=<portNo>
```