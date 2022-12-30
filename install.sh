#!/bin/bash
mkdir -p $HOME/.gdb/tvm-gdb-commands
curl -L https://raw.githubusercontent.com/anirudhsundar/tvm-gdb-commands/master/commands.py > $HOME/.gdb/tvm-gdb-commands/commands.py
touch $HOME/.gdbinit
echo "source $HOME/.gdb/tvm-gdb-commands/commands.py" >> $HOME/.gdbinit
