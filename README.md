## 1. TVM specific GDB commands

This extension adds 4 new commands to gdb that improve the experience of debugging the [Apache TVM](https://tvm.apache.org/) code. The commands are explained below with examples.

### 1.1 Installation

 - Run the below command

    ```bash
    bash < <(curl -s https://raw.githubusercontent.com/anirudhsundar/tvm-gdb-commands/master/install.sh)
    ```

 - Alternatively, download the `commands.py` to some location and source the `commands.py` file, either directly in your gdb session or add the below line to your `.gdbinit`:

    ```bash
    source /path/to/commands.py
    ```

### 1.2 Commands Explained

 - **`tvm_dump` / `tvd`** 

    Calls `p tvm::Dump(<value>)` for a given value

    > `tvd` is an alias to `tvm_dump`

    Eg:
    ```c++
    (gdb) tvd index
    (((j.outer*64) + (i*n)) + j.inner)
    ```

 - **`tvm_type` / `tvt`**

    Prints the original object type of a given value. When a function gets a `PrimExpr` as argument, this commands prints which sub-class of `PrimExpr` the given value is. This is in same spirit to whatis command in gdb

    > `tvt` is an alias to `tvm_type`

    For example, `AddNode` could be the underlying original type of the object, declared using it's parent `PrimExprNode`

    Usage:
    ```c++
    (gdb) whatis index
    type = tvm::PrimExpr
    (gdb) tvt index
    tvm::tir::AddNode
    ```

 - **`tvm_attr` / `tvat`**

    This commmand extends the use of `tvm_type` and tries to access the underlying attributes/members of the original object.

    > `tvat` is an alias to `tvm_attr`

    For example, AddNode has the members `a` and `b`, so this allows us to access those members.

    This prints out 3 lines, where the first line shows the access string used to access the member, second line shows the type of the object, and the last line prints a dump of the object

    ```c++
    (gdb) tvat index.a
    access string '((tvm::tir::AddNode*)index).a'
    Type of object: 'tvm::tir::AddNode'
    ((j.outer*64) + (i*n))
    ```

    This command can also take attributes recursively
    For example:
    ```c++
    (gdb) tvat index.a.a.b
    access string '((tvm::tir::MulNode*)((tvm::tir::AddNode*)((tvm::tir::AddNode*)index).a).a).b'
    Type of object: 'tvm::IntImmNode'
    64
    ```

 - **`tvm_fields` / `tvf`**

    This command prints the list of fields available in the given object/object.attributes. This can be called with either a single object, or the object.attr.attr syntax

    > `tvf` is an alias to `tvm_fields`

    > Note: The fields can also be directly found by <tab> completion when using the `tvm_attr` command, but there are some gotchas in that method, especially when trying completion more than once, so this command was written to help with that.

    For example:
    ```c++
    (gdb) tvf index.a.a
    tvm::PrimExprNode       a       b       _type_final     _type_child_slots
    ```

### 1.3 Other Tips

 - There are 4 aliases (as shown below) defined in the code and if you wish to remove them in favor of others one might like, please comment out the last 4 lines in `commands.py`

    ```c++
    alias tvd = tvm_dump
    alias tvt = tvm_type
    alias tvat = tvm_attr
    alias tvf = tvm_fields
    ```

## 2. Hybrid Python + C++ Debugging with LLDB in VSCode​

The `.vscode/launch.json` configuration enables hybrid debugging of TVM's Python frontend (Python debugger) and C++ backend (LLDB) in VSCode.

> [!WARNING]
> Our current configuration only supports LLDB debugging. Please ensure you have LLDB installed on your system. We will subsequently provide some LLDB command scripts to assist with debugging.

### 2.1 Required VSCode Extensions

Before using this configuration to debug TVM, we should install the following extensions for VSCode:

 - [CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb): Search`vadimcn.vscode-lldb` in VSCode extension marketplace.
 - [​Python C++ Debugger​​](https://marketplace.visualstudio.com/items?itemName=benjamin-simmonds.pythoncpp-debug): Search `benjamin-simmonds.pythoncpp-debug` in VSCode extension marketplace.

After installing the extensions, we should copy the `.vscode/launch.json` file to the root directory of your own project. And the next steps will explain some details that you should modify in the `launch.json` file.

### 2.2 Debugging Modes​ and Usage

The current configuration supports two debugging modes:

 - Hybrid Python Frontend + C++ Backend Debugging for TVM
 - Pure C++ Backend Debugging for TVM

As the fowllowing image shows, we can choose the debugging mode in graphical interface. Ther are four choices:
 - `Full Auto Debug (Python+C++)` is the entry for Hybrid Python Frontend + C++ Backend Debugging.
    - `Python: TVM Frontend` is responsible for the debugging of the Python Frontend.
    - `C++: TVM Backend` is responsible for the debugging of the C++ Backend.
 - `Pure C++ Debug (C++)` is the entry for Pure C++ Backend Debugging.

![Image](https://github.com/user-attachments/assets/3c344bed-6acd-4e83-86e8-4569199c8084)

#### 2.2.1 Hybrid Python + C++ Debugging for TVM

This is a hybrid debugging approach, and requires users to first launch the Python script, after which the C++ process will be automatically attached.

> [!IMPORTANT]  
> Customize the `"program"` entry in `.vscode/launch.json` to point to your Python virtual environment executable.  
> Example path:
> `"program": "/opt/homebrew/Caskroom/miniconda/base/envs/tvm-build-venv/bin/python"`

Example:

![Hybrid Debugging Example](https://github.com/user-attachments/assets/e56d69fa-2c45-4463-9bb5-527261213eae)

#### 2.2.2 Pure C++ Debugging

This is a pure C++ debugging approach, where users can debug C++ components without Python scripts.

> [!IMPORTANT]  
> Customize the `"program"` entry in `.vscode/launch.json` to your C++ executable path.
> Example path:  
> `"program": "${workspaceFolder}/get_started/tutorials/a.out"`

Example:

![Image](https://github.com/user-attachments/assets/ae2f4fce-3ccb-4ec6-94cf-5c26d158223e)

You can also check `.vscode/launch.json` for debugging mode details - we've added extensive comments there.

## Contributions

Always welcome.

## Acknowledgements

Thanks to [Lunderberg](https://github.com/Lunderberg/) for valuable feedback and whose [tvm-gdb-extension](https://github.com/Lunderberg/tvm-gdb-extension) was the inspiration to create this one

