# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )
# Son, this thing can self destruct

# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )
# Son, this thing can self destruct

import sys
import types
import importlib
import pkgutil
import logging
import ast
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, Tuple

from Source.modules.Data import DataHandler

logging.basicConfig(level=logging.INFO)


class Loader:
    @staticmethod
    def LoadModule(TargetName: Union[str, List[str]]) -> List[types.ModuleType]:
        """Loads modules by module name or a list of module names."""
        if isinstance(TargetName, str):
            TargetName = [TargetName]

        FoundItems = []
        for Target in TargetName:
            try:
                Found = importlib.import_module(Target)
                FoundItems.append(Found)
            except ImportError as e:
                logging.error(f"Module '{Target}' does not exist: {e}")

        return FoundItems

    @staticmethod
    def LoadModuleFromPath(Targets: Union[str, Path, List[Union[str, Path]]], prefix: str = "") -> List[types.ModuleType]:
        """Discovers and imports modules located within physical file system paths."""
        FoundItems = []
        if not isinstance(Targets, list):
            Targets = [Targets]

        ResolvedPaths = [str(Path(Folder).resolve()) for Folder in Targets]

        for path_str in ResolvedPaths:
            if path_str not in sys.path:
                sys.path.insert(0, path_str)

        for _, modname, _ in pkgutil.walk_packages(ResolvedPaths, prefix=prefix):
            try:
                mod = importlib.import_module(modname)
                FoundItems.append(mod)
            except ImportError as e:
                logging.error(f"Failed to import '{modname}' from path: {e}")

        return FoundItems

    @staticmethod
    def CloneImport(TargetImport: Union[str, List[str]], CustomPrefix: str = "Clone_") -> List[types.ModuleType]:
        """Creates shallow clones of loaded modules and registers them into sys.modules."""
        Clones = []
        Imports = Loader.LoadModule(TargetImport)

        SKIP_ATTRS = {"__name__", "__loader__", "__spec__", "__file__", "__cached__", "__path__"}

        for Import in Imports:
            if Import is None:
                continue

            clone_name = f"{CustomPrefix}{Import.__name__}"
            CloneImport = types.ModuleType(clone_name)  

            CloneImport.__spec__ = getattr(Import, "__spec__", None)
            CloneImport.__loader__ = getattr(Import, "__loader__", None)

            for key, value in Import.__dict__.items():
                if key not in SKIP_ATTRS:
                    setattr(CloneImport, key, value)

            sys.modules[clone_name] = CloneImport
            Clones.append(CloneImport)

        return Clones


class Modifier:
    @staticmethod
    def ApplyAttr(TargetModule: Union[str, types.ModuleType], Modinfo: Any) -> List[str]:
        """Applies attributes or dynamically compiled string code onto target modules."""
        SuccessChanges = []

        if isinstance(TargetModule, str):
            modules = Loader.LoadModule(TargetModule)
            if not modules:
                return SuccessChanges
            Import = modules[0]
        else:
            Import = TargetModule

        Name = getattr(Import, "__name__", "UnknownModule")

        # Normalize Modinfo inputs into iterable pairs
        if isinstance(Modinfo, dict):
            items = Modinfo.items()
        elif isinstance(Modinfo, list):
            items = Modinfo
        else:
            logging.error("Modinfo must be a dictionary or list of key-value pairs.")
            return SuccessChanges

        for ModPart, Mod in items:
            if isinstance(Mod, str):
                try:
                    ast.parse(Mod)
                    exec(compile(Mod, filename=f"<dynamic_{Name}>", mode="exec"), Import.__dict__)
                    logging.info(f"Dynamic code compiled and attached to {Name} for '{ModPart}'")
                    SuccessChanges.append(f"{ModPart}: dynamic code compiled")
                except Exception as e:
                    logging.error(f"Failed to compile dynamic code for '{ModPart}' on {Name}: {e}")
            else:
                setattr(Import, str(ModPart), Mod)
                logging.info(f"Attribute '{ModPart}' set on {Name}")
                SuccessChanges.append(f"{ModPart}: attribute updated")

        return SuccessChanges

    @staticmethod
    def DeleteAttr(TargetImport: Union[str, types.ModuleType], AttrNames: List[str]) -> Optional[types.ModuleType]:
        """Deletes specified attributes safely from a target module."""
        if isinstance(TargetImport, str):
            modules = Loader.LoadModule(TargetImport)
            if not modules:
                logging.error(f"Cannot delete attributes. Module '{TargetImport}' not found.")
                return None
            Import = modules[0]
        else:
            Import = TargetImport

        for AttrName in AttrNames:
            if hasattr(Import, AttrName):
                delattr(Import, AttrName)
                logging.info(f"Attribute '{AttrName}' deleted from {getattr(Import, '__name__', 'Module')}")

        return Import


class Handler:
    def __init__(self):
        self.DataHandler = DataHandler.Handler() if hasattr(DataHandler, "Handler") else None
        self.ConLog: Dict[str, List[str]] = {}
        self.ChangeLog: Dict[str, List[Any]] = {}
        self.CloneLog: List[str] = []

    def Connect(self, Info: List[Tuple[str, List[str]]]) -> None:
        """Connects sub-modules or attributes dynamically across targets."""
        for Target, Imports in Info:
            target_mods = Loader.LoadModule(Target)
            if not target_mods:
                continue
            Found = target_mods[0]

            for Import in Imports:
                if not hasattr(Found, Import):
                    imported_sub = Loader.LoadModule(Import)
                    if imported_sub:
                        setattr(Found, Import, imported_sub[0])

                        target_key = Found.__name__
                        if target_key not in self.ConLog:
                            self.ConLog[target_key] = []
                        self.ConLog[target_key].append(Import)

                        self._log_changes(self.ConLog, Import, key=target_key)
                else:
                    logging.info(f"Connection '{Import}' already exists on '{Found.__name__}'.")

    def Disconnect(self, ListInfo: List[Tuple[str, List[str]]]) -> None:
        """Removes linked sub-modules from target modules."""
        for Target, Imports in ListInfo:
            target_mods = Loader.LoadModule(Target)
            if not target_mods:
                continue
            Found = target_mods[0]

            for Import in Imports:
                if hasattr(Found, Import):
                    delattr(Found, Import)
                    if Found.__name__ in self.ConLog and Import in self.ConLog[Found.__name__]:
                        self.ConLog[Found.__name__].remove(Import)
                else:
                    logging.info(f"Disconnect skipped for '{Import}'; not found on '{Found.__name__}'.")

    def ApplyAttr(self, AttrInfos: List[Tuple[str, Any]], TargetScripts: Optional[List[str]] = None) -> None:
        """Applies dynamic modifications directly or via isolated module clones."""
        for ModuleName, AttrInfo in AttrInfos:
            if TargetScripts is not None:
                clones = Loader.CloneImport(ModuleName, CustomPrefix="Clone_")
                if not clones:
                    continue
                Clone = clones[0]

                SuccessChanges = Modifier.ApplyAttr(Clone, AttrInfo)

                self._log_changes(self.CloneLog, Clone.__name__)
                self._log_changes(self.ChangeLog, SuccessChanges, key=Clone.__name__)

                for Target in TargetScripts:
                    target_mods = Loader.LoadModule(Target)
                    if target_mods:
                        Found = target_mods[0]
                        setattr(Found, Clone.__name__, Clone)
                        self._log_changes(self.ConLog, Clone.__name__, key=Found.__name__)
            else:
                SuccessChanges = Modifier.ApplyAttr(ModuleName, AttrInfo)
                self._log_changes(self.ChangeLog, SuccessChanges, key=ModuleName)

    def DeleteAttr(self, AttrInfos: List[Tuple[str, List[str]]]) -> None:
        """Deletes targeted attributes and updates operational logs."""
        for ModuleName, AttrInfo in AttrInfos:
            Modifier.DeleteAttr(ModuleName, AttrInfo)
            self._log_changes(self.ChangeLog, f"Deleted: {AttrInfo}", key=ModuleName)

    def Revert(self, RevertInfo: Dict[str, List[str]]) -> None:
        """Reverts active clones attached to target modules."""
        for Target, ImportList in RevertInfo.items():
            target_mods = Loader.LoadModule(Target)
            if not target_mods:
                continue
            TargetModule = target_mods[0]

            for ImportName in ImportList:
                CopyName = f"Clone_{ImportName}"
                if hasattr(TargetModule, CopyName):
                    delattr(TargetModule, CopyName)
                    logging.info(f"Reverted {CopyName} on {TargetModule.__name__}")

    def GarbageCollect(self) -> None:
        """Removes unreferenced module clones from sys.modules."""
        Unattached = []
        for CloneName in self.CloneLog:
            is_attached = any(
                CloneName in connections 
                for connections in self.ConLog.values()
            )
            if not is_attached:
                Unattached.append(CloneName)

        for CloneName in Unattached:
            if CloneName in sys.modules:
                del sys.modules[CloneName]
            if CloneName in self.CloneLog:
                self.CloneLog.remove(CloneName)
            logging.info(f"Garbage collected module: {CloneName}")

    def _log_changes(self, Table: Union[Dict, List], Value: Any, key: Optional[str] = None) -> None:
        """Helper to log modifications into memory state and DataHandler persistence."""
        if Value is None:
            logging.warning("Logging skipped because Value is None.")
            return

        if isinstance(Table, dict):
            if key is None:
                logging.error("Key is required when logging to a dictionary.")
                return
            if key not in Table:
                Table[key] = []
            Table[key].append(Value)

            if self.DataHandler:
                try:
                    if hasattr(self.DataHandler, "Backet"):
                        self.DataHandler.Backet(Table)
                    if hasattr(self.DataHandler, "Store"):
                        store_target = "ConLog" if Table is self.ConLog else "ChangeLog"
                        self.DataHandler.Store(store_target)
                except Exception as e:
                    logging.error(f"Failed persistence store operation: {e}")

        elif isinstance(Table, list):
            if Value not in Table:
                Table.append(Value)
                if self.DataHandler:
                    try:
                        if hasattr(self.DataHandler, "Backet"):
                            self.DataHandler.Backet(Table)
                        if hasattr(self.DataHandler, "Store"):
                            self.DataHandler.Store("CloneLog")
                    except Exception as e:
                        logging.error(f"Failed persistence list store operation: {e}")