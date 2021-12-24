socket, currency server assignment
# Usage
There are 2 servers and 2 clients (console and gui) which are can well pair with each other.

Before start running:

- Replace IP address in those files with your IP address.
- Replace `from util.loop import Loop` to `from util.loop_window import Loop` if you run server on Windows

On your server machine:

`python3 ./server_gui.py`

On your client machine(s) (at least at the same network with server):

`python3 ./client_gui.py`
