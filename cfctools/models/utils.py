
from collections import namedtuple

def namedtuple_factory(tuple_name, fields, module=None):
    names = []
    defaults = []
    for name, default in fields.items():
        names.append(name)
        defaults.append(default)
    nt = namedtuple(tuple_name, field_names=names, defaults=defaults, module=module)
    return nt


def new_instance_of_slotted_dataclass(clazz, field_defns, **kwargs):
    attrs = {}
    for attr in clazz.__slots__:
        ftype, fdefault = field_defns[attr]
        attrs[attr] = kwargs.get(attr, fdefault)
        if ftype:
            attrs[attr] = ftype(attrs[attr])
    return clazz(**attrs)
