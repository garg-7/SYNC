# SYNC

A tool for music synchronization across devices on a local network.  
There are two versions for this tool as mentioned below. The command-line version is the one that is a little ahead, some features are yet to be adapted to the GUI-version.  


## Dependencies 
The libraries needed are - `pygame` and `PyQt5`. They can be installed via pip.
```bash
python -m pip install pygame==2.0.0
python -m pip install pyqt==5.15.1
```
(Note: The versions used at the time of development are specified above.)


## Managing the music files
The music that needs to be played must be present under the `music` folder (which has been createdunder both GUI and CLI implementation folders but is empty for now) whether the node is acting as a client or a server.

## Command line utility

1. Go to the `CLI` folder.
```bash
cd CLI
```
2. Run `main.py`

```bash
py main.py
```

This is followed by some self explanatory queries for the communication.  
Note: In this implementation, the server will query for the file from the clients if it does not have it. It will then verify whether all the clients have the file to be played. Then it will start operation.

## GUI-based utility

1. Go to the `GUI` folder
```bash
cd GUI
```
2. run `main.py`
```bash
py main.py
```

This is followed by some self-explanatory on-screen prompts for the user to continue operation.  
Note: In this implementation, the server needs to have any file that is to be played. It will only verify whether all the clients have the file to be played or not. If the file is not present on some client, it will send the file to that client before beginning any operation.
