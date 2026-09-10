import importlib
import pkgutil
import sys

package_name = __name__
package_path = __path__

__all__ = []

for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
    full_module_name = f"{package_name}.{module_name}"
    module = importlib.import_module(full_module_name)
    
    globals()[module_name] = module
    __all__.append(module_name)
    
    if is_pkg and hasattr(module, "__all__"):
        for attr in module.__all__:
            globals()[attr] = getattr(module, attr)
            if attr not in __all__:
                __all__.append(attr)
    elif is_pkg:
        for attr in dir(module):
            if not attr.startswith('_'):
                globals()[attr] = getattr(module, attr)
                if attr not in __all__:
                    __all__.append(attr)
