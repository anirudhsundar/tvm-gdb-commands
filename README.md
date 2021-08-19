## This is a small gdb extension that introduces a few gdb commands to be used in the [TVM Project](https://github.com/apache/tvm)

There are 4 commands introduced in this extension.

#### tvm_dump
**`tvm_dump`** - Calls `p tvm::Dump(<value>)` for a given value

Eg:
```c++
(gdb) tvm_dump index
(((j.outer*64) + (i*n)) + j.inner)
```

#### tvm_type

**`tvm_type`** - Prints the original object type of a given value. When a function gets a `PrimExpr` as argument, this commands prints which sub-class of `PrimExpr` the given value is. This is in same spirit to whatis command in gdb
For example, `AddNode` could be the underlying original type of the object, declared using it's parent `PrimExprNode`

Usage:
```c++
(gdb) whatis index
type = tvm::PrimExpr
(gdb) tvm_type index
tvm::tir::AddNode
```

#### tvm_attr
**`tvm_attr`** - This commmand extends the use of `tvm_type` and tries to access the underlying attributes/members of the original object.
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

#### tvm_fields
**`tvm_fields`** - This command prints the list of fields available in the given object/object.attributes. This can be called with either a single object, or the object.attr.attr syntax

> Note: The fields can also be directly found by <tab> completion when using the `tvm_attr` command, but there are some gotchas in that method, especially when trying completion more than once, so this command was written to help with that.

For example:
```c++
(gdb) tvm_fields index.a.a
tvm::PrimExprNode       a       b       _type_final     _type_child_slots
```

### Other Tips

I set the names for all these commands with tvm_* prefix even though it's not too convenient to type so that it won't collide with other gdb commands. One could potentially create a list of aliases for these to save some typing. I personally use the below set of aliases.

```c++
alias tvd = tvm_dump
alias tvt = tvm_type
alias tvat = tvm_attr
alias tvf = tvm_fields
```

### Installation

The simplest way to install the plugin is to source the commands.py file, either directly in your gdb session or adding the below line to your `.gdbinit`

`source /path/to/commands.py`

### Contributions

Always welcome.

### Acknowledgements

Thanks to [Lunderberg](https://github.com/Lunderberg/) for valuable feedback and whose [tvm-gdb-extension](https://github.com/Lunderberg/tvm-gdb-extension) was the inspiration to create this one

