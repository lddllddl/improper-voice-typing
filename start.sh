#nix-shell --run 'watchexec -r -w main.py -- python3.9 main.py'
nix-shell --run 'watchexec --signal SIGKILL -r -w main.py -- kitty python3.9 main.py'
