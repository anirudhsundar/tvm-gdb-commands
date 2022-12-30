## TVM specific GDB commands

This extension adds 4 new commands to gdb that improve the experience of debugging the [Apache TVM](https://tvm.apache.org/) code. The commands are explained below with examples.

### Installation

Run the below command

```bash
bash < <(curl -s https://raw.githubusercontent.com/anirudhsundar/tvm-gdb-commands/master/install.sh)
```

Alternatively, download the `commands.py` to some location and source the `commands.py` file, either directly in your gdb session or add the below line to your `.gdbinit`

`source /path/to/commands.py`

### Commands Explained

#### tvm_dump (tvd)
**`tvm_dump` / `tvd`** - Calls `p tvm::Dump(<value>)` for a given value

> `tvd` is an alias to `tvm_dump`

Eg:
```c++
(gdb) tvm_dump index
(((j.outer*64) + (i*n)) + j.inner)
```

#### tvm_type (tvt)

**`tvm_type` / `tvt`** - Prints the original object type of a given value. When a function gets a `PrimExpr` as argument, this commands prints which sub-class of `PrimExpr` the given value is. This is in same spirit to whatis command in gdb

> `tvt` is an alias to `tvm_type`

For example, `AddNode` could be the underlying original type of the object, declared using it's parent `PrimExprNode`

Usage:
```c++
(gdb) whatis index
type = tvm::PrimExpr
(gdb) tvm_type index
tvm::tir::AddNode
```

#### tvm_attr (tvat)
**`tvm_attr` / `tvat`** - This commmand extends the use of `tvm_type` and tries to access the underlying attributes/members of the original object.

> `tvat` is an alias to `tvm_attr`

For example, AddNode has the members `a` and `b`, so this allows us to access those members.

This prints out 3 lines, where the first line shows the access string used to access the member, second line shows the type of the object, and the last line prints a dump of the object

```c++
(gdb) tvm_attr index.a
access string '((tvm::tir::AddNode*)index).a'
Type of object: 'tvm::tir::AddNode'
((j.outer*64) + (i*n))
```

This command can also take attributes recursively
For example:
```c++
(gdb) tvm_attr index.a.a.b
access string '((tvm::tir::MulNode*)((tvm::tir::AddNode*)((tvm::tir::AddNode*)index).a).a).b'
Type of object: 'tvm::IntImmNode'
64
```

#### tvm_fields (tvf)
**`tvm_fields` / `tvf`** - This command prints the list of fields available in the given object/object.attributes. This can be called with either a single object, or the object.attr.attr syntax

> `tvf` is an alias to `tvm_fields`

> Note: The fields can also be directly found by <tab> completion when using the `tvm_attr` command, but there are some gotchas in that method, especially when trying completion more than once, so this command was written to help with that.

For example:
```c++
(gdb) tvm_fields index.a.a
tvm::PrimExprNode       a       b       _type_final     _type_child_slots
```

### Other Tips

There are 4 aliases (as shown below) defined in the code and if you wish to remove them in favor of others one might like, please comment out the last 4 lines in `commands.py`

```c++
alias tvd = tvm_dump
alias tvt = tvm_type
alias tvat = tvm_attr
alias tvf = tvm_fields
```

### Contributions

Always welcome.

### Acknowledgements

Thanks to [Lunderberg](https://github.com/Lunderberg/) for valuable feedback and whose [tvm-gdb-extension](https://github.com/Lunderberg/tvm-gdb-extension) was the inspiration to create this one

