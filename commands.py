import gdb
import re

def get_object_access_str(arg_list):
    object = arg_list[0]
    attr_list = arg_list[1:]
    object_access_str = object
    for attr in attr_list:
        type = gdb.execute('tvm_type '+object, to_string=True).strip()
        if 'GDB Error' in type or len(type) == 0:
            print("GDB Error: Could not extract type")
        else:
            object_access_str = "(("+type+"*)"+object+")."+attr
            object = object_access_str
    return object_access_str

def get_attribute_fields(arg_list):
    if len(arg_list) == 1:
        object_access_str = arg_list[0]
    object_access_str = get_object_access_str(arg_list)
    try:
        attribute_type = gdb.execute('tvm_type '+object_access_str, to_string=True).strip()
        if attribute_type in ['tvm::tir::AddNode', 'tvm::tir::SubNode', 'tvm::tir::MulNode']:
            attribute_type = 'tvm::tir::BinaryOpNode<'+attribute_type+'>'
        attribute_type = gdb.lookup_type(attribute_type)
        attribute_fields = attribute_type.fields()
        attribute_fields = [x.name for x in attribute_fields]
        return attribute_fields
    except gdb.error:
        return []

class TVMDump(gdb.Command):
    """Call tvm::Dump on the passed argument for easy printing"""

    def __init__(self):
        super(TVMDump, self).__init__(
            "tvm_dump", gdb.COMMAND_USER
        )

    def invoke(self, args, from_tty):
        arg_list = gdb.string_to_argv(args)
        for arg in arg_list:
            gdb.execute('print tvm::Dump('+arg+')')

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

class TVMGetDerivedType(gdb.Command):
    """
Extract the original type stored of the object
This command will try to access the deleter from ObjectRefs using value.get().deleter_ and from Objects using value.deleter_. If it both fails it throws an error

    Note: The way this is done currently involves a hack to extract the type present as part of the Object's Deleter_

    """

    def __init__(self):
        super(TVMGetDerivedType, self).__init__(
            "tvm_type", gdb.COMMAND_USER
        )

    def invoke(self, args, from_tty):
        arg_list = gdb.string_to_argv(args)
        extract_type_re = re.compile(".*tvm::runtime::.*Handler<(.*)>::Deleter_.*")
        for arg in arg_list:
            deleter_typestring = ""
            try:
                deleter_typestring = gdb.execute('print *'+arg+'.get().deleter_', to_string=True)
            except gdb.error:
                try:
                    deleter_typestring = gdb.execute('print *'+arg+'.deleter_', to_string=True)
                except gdb.error:
                    print("GDB Error: could not extract type")
            type_match = extract_type_re.match(deleter_typestring)
            types = type_match.groups()
            if len(types) == 0:
                print("GDB Error: Could not extract type")
            else:
                for type in types:
                    print(type)
    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

class TVMAccessRuntimeAttr(gdb.Command):
    """Try to access the attributes of the Object by casting to the correct type. This command can be used as 'tvm_type <object>.<attributes>' and it tries to access the <attributes> from the <object> recursively by finding the types for each object
    Example usage (when accessing 'index' attribute of 'op' object which is of type 'LoadNode'):
        tvm_attr op index

    Output:
        access string '((tvm::tir::LoadNode*)op).index'
        ((i*xsize) + k)

    Example usage for recursive attributes
        tvm_attr op index.a.b

    Output:
        access string '((tvm::tir::LoadNode*)op).index.a.b'
        ((i*xsize) + k)
    """

    def __init__(self):
        super(TVMAccessRuntimeAttr, self).__init__(
            "tvm_attr", gdb.COMMAND_USER
        )

    def invoke(self, args, from_tty):
        arg_list = args.split('.')
        if len(arg_list) < 2:
            print("GDB Error: Please pass an <object> and list of attributes separated by '.' See 'help tvm_attr' for more details")
        object_access_str = get_object_access_str(arg_list)
        print("access string '"+object_access_str+"'")
        try:
            attribute_type = gdb.execute('tvm_type '+object_access_str, to_string=True).strip()
            print("Type of object: '"+attribute_type+"'")
        except:
            pass # this try-except is technically not needed, but I found some problems with different versions of gdb
        try:
            gdb.execute('tvm_dump '+object_access_str, to_string=True)
        except gdb.error:
            gdb.execute('print '+object_access_str)

    def complete(self, text, word):
        if text[-1] == ".":
            text = text[:-1]
        arg_list = text.split('.')
        return get_attribute_fields(arg_list)

class TVMFields(gdb.Command):
    """Print the available fields of the passed in object.
    Example usage:
        tvm_fields index.a

    Output:
        tvm::PrimExprNode       a       b       _type_final     _type_child_slots

    """

    def __init__(self):
        super(TVMFields, self).__init__(
            "tvm_fields", gdb.COMMAND_USER
        )

    def invoke(self, args, from_tty):
        arg_list = args.split('.')
        print(get_attribute_fields(arg_list))

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

TVMDump()
TVMGetDerivedType()
TVMAccessRuntimeAttr()
TVMFields()

