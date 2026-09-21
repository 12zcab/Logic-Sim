import importlib
import pkgutil
from types import ModuleType

package_name = __name__
package_path = __path__

__all__ = []

for _, _mod_name, _is_pkg in pkgutil.iter_modules(package_path):
    _full_mod_name = f"{package_name}.{_mod_name}"
    _imported_mod = importlib.import_module(_full_mod_name)
    
    globals()[_mod_name] = _imported_mod
    if _mod_name not in __all__:
        __all__.append(_mod_name)
    
    if hasattr(_imported_mod, "__all__"):
        _attrs = _imported_mod.__all__
    else:
        _attrs = [a for a in dir(_imported_mod) if not a.startswith('_')]
    for _attr in _attrs:
        if hasattr(_imported_mod, _attr):
            _obj = getattr(_imported_mod, _attr)
            if isinstance(_obj, ModuleType):
                continue
                
            globals()[_attr] = _obj
            if _attr not in __all__:
                __all__.append(_attr)