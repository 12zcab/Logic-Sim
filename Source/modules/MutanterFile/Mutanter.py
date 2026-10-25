# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )
# I have used AI to help me check errors 
# Son, this thing can self destruct

import sys
import importlib
import importlib.util
import logging
import pkgutil
import types
from pathlib import Path
from typing import Any, Dict, List, Union, Optional

# Optional dependency fallback check
try:
    import Source.modules.MutanterFile.Transformer as Transformer
except ImportError:
    Transformer = None

try:
    from Data import DataHandler
except ImportError:  
    DataHandler = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ScriptEngine")


class Loader:
    @staticmethod
    def LoadModule(TargetName: Union[str, List[str]]) -> List[types.ModuleType]:
        FoundItems = [] 
        if TargetName == "All":
           TargetName = list(sys.builtin_module_names) + [mod.name for mod in pkgutil.iter_modules()]
 
        if isinstance(TargetName, str):
            TargetName = [TargetName]

        for Target in TargetName:
            try:
                Found = importlib.import_module(Target)
                FoundItems.append(Found)
            except ImportError as e:
                logger.error(f"'{Target}' does not exist due to: {e}")
                raise

        return FoundItems

    @staticmethod
    def LoadModuleFromPath(Targets: Union[str, List[str]], prefix: str = "") -> List[types.ModuleType]:
        FoundItems = []
        Paths = []
        if not isinstance(Targets, list):
            Targets = [Targets]

        for Folder in Targets:
            Paths.append(Path(Folder).resolve())

        for p in Paths:
            try:
                for _, modname, _ in pkgutil.iter_modules([str(p)]):
                    Target = f"{prefix}{modname}"
                    try:
                        found_mod = importlib.import_module(Target)
                        FoundItems.append(found_mod)
                    except ImportError as e:
                        logger.error(f"'{Target}' does not exist due to: {e}")
            except Exception as e:
                logger.error(f"Error iterating modules in path {p}: {e}")

        return FoundItems

    @staticmethod
    def CloneImport(TargetImport: Union[str, types.ModuleType], clone_name: Optional[str] = None) -> List[types.ModuleType]:
        Clones = []
        if isinstance(TargetImport, str):
            Imports = Loader.LoadModule(TargetImport)
        else:
            Imports = [TargetImport]

        for Import in Imports:
            if Import is None:
                continue

            mod_file = getattr(Import, "__file__", None)
            mod_name = getattr(Import, "__name__", "Module")
            new_name = clone_name if clone_name else f"Copy_{mod_name}"

            if mod_file and Path(mod_file).exists():
                try:
                    spec = importlib.util.spec_from_file_location(new_name, mod_file)
                    if spec and spec.loader:
                        CloneModule = importlib.util.module_from_spec(spec)
                        CloneModule.__name__ = new_name
                        sys.modules[new_name] = CloneModule
                        spec.loader.exec_module(CloneModule)
                        Clones.append(CloneModule)
                        continue
                except Exception as e:
                    logger.warning(f"Spec clone failed for {mod_name}, falling back to dynamic object: {e}")
                    if new_name in sys.modules:
                        del sys.modules[new_name]

            CloneModule = types.ModuleType(new_name)
            CloneModule.__name__ = new_name
            sys.modules[new_name] = CloneModule
            
            ignored_keys = {
                "__name__",
                "__loader__",
                "__spec__",
                "__file__",
                "__cached__",
                "__builtins__",
            }
            for key, value in Import.__dict__.items():
                if key not in ignored_keys:
                    setattr(CloneModule, key, value)
            Clones.append(CloneModule)

        return Clones


class Modifier:
    @staticmethod
    def ApplyAttr(TargetModule: Union[str, types.ModuleType], Modinfo: Union[dict, list]) -> List[str]:
        SuccessChanges = []

        if isinstance(TargetModule, str):
            try:
                modules = Loader.LoadModule(TargetModule)
                if not modules:
                    return SuccessChanges
                Import = modules[0]
            except Exception as e:
                logger.error(f"Error resolving target module '{TargetModule}': {e}")
                raise
        else:
            Import = TargetModule

        Name = getattr(Import, "__name__", str(Import))
        items = Modinfo.items() if isinstance(Modinfo, dict) else Modinfo

        for ModPart, Mod in items:
            try:
                if not isinstance(Mod, str):
                    setattr(Import, str(ModPart), Mod)
                    logger.info(f"'{ModPart}' has been replaced on '{Name}'")
                    SuccessChanges.append(str(ModPart))
                else:
                    Compile = compile(Mod, f"<string_{ModPart}>", "exec")
                    exec(Compile, Import.__dict__)
                    logger.info(f"'{ModPart}' has been compiled and attached to '{Name}'")
                    SuccessChanges.append(str(ModPart))
            except Exception as e:
                logger.error(f"Execution failed for '{ModPart}' on '{Name}': {e}")
                raise RuntimeError(f"Modification failed for '{ModPart}': {e}") from e

        return SuccessChanges

    @staticmethod
    def DeleteAttr(TargetImport: Union[str, types.ModuleType], AttrNames: List[str]) -> Optional[types.ModuleType]:
        if isinstance(TargetImport, str):
            try:
                modules = Loader.LoadModule(TargetImport)
                if not modules:
                    return None
                Import = modules[0]
            except Exception as e:
                logger.error(f"{e} appeared as '{TargetImport}' is not loaded.")
                return None
        else:
            Import = TargetImport

        for AttrName in AttrNames:
            if hasattr(Import, AttrName):
                delattr(Import, AttrName)
                logger.info(f"Attribute '{AttrName}' deleted from '{getattr(Import, '__name__', 'Module')}'")
            else:
                logger.warning(f"Attribute '{AttrName}' not found for deletion.")

        return Import


class Handler:
    def __init__(self, data_handler: Optional[Any] = None):
        print("This is more automatic but u can still use manually if u are cool")
        if data_handler is not None:
            self.DataHandler = data_handler
        elif DataHandler is not None:
            self.DataHandler = DataHandler.Handler()
        else:
            self.DataHandler = None

        self.ConLog = {} 
        self.ChangeLog = {}
        self.CloneLog = [] 

    def Connect(self, Infos: dict):
        FoundList = Loader.LoadModule(Infos["Targets"])
        Found = FoundList[0]
        ImportList = Loader.LoadModule(Infos["Imports"])
        Imports = ImportList[0]

        for Target in Found:
            for Import in Imports:
                Name = Infos["Names"].get(Import.__name__, False)
                if Name is False:
                    Name = Import.__name__
                setattr(Target, Name, Import)

    def Disconnect(self, ListInfo: List[tuple]):
        for Target, Imports in ListInfo:
            for Import in Imports:
                try:
                    FoundList = Loader.LoadModule(Target)
                    if not FoundList:
                        continue
                    Found = FoundList[0]

                    if hasattr(Found, Import):
                        delattr(Found, Import)  
                        found_name = getattr(Found, "__name__", str(Target))
                        if found_name in self.ConLog and Import in self.ConLog[found_name]:
                            self.ConLog[found_name].remove(Import)
                    else:
                        print(f"No need to disconnect '{Import}' from '{Target}'")
                except Exception as e:
                    logger.error(f"Error during disconnect of '{Import}' from '{Target}': {e}")

    def ApplyAttr(self, AttrInfos: List[tuple], TargetScripts: Optional[List[str]] = None):
        try:
            for ModuleName, AttrInfo in AttrInfos:
                if TargetScripts is not None:
                    clones = Loader.CloneImport(ModuleName, clone_name=f"Clone_{ModuleName}")
                    if not clones:
                        continue
                    Clone = clones[0]

                    if Clone not in self.CloneLog:
                        self.CloneLog.append(Clone)

                    SuccessChanges = Modifier.ApplyAttr(Clone, AttrInfo)

                    self.LogChanges(self.CloneLog, Clone)
                    self.LogChanges(self.ChangeLog, SuccessChanges, key=getattr(Clone, "__name__", "Clone"))

                    for Target in TargetScripts:
                        targets = Loader.LoadModule(Target)
                        if targets:
                            Found = targets[0]
                            setattr(Found, Clone.__name__, Clone)
                            self.LogChanges(self.ConLog, Clone.__name__, key=getattr(Found, "__name__", Target))
                else:
                    SuccessChanges = Modifier.ApplyAttr(ModuleName, AttrInfo)
                    self.LogChanges(self.ChangeLog, SuccessChanges, key=ModuleName)   
        except Exception as e:
            logger.error(f"Failed in Handler.ApplyAttr transaction: {e}")  
            raise  
  
    def DeleteAttr(self, AttrInfos: List[tuple], TargetScripts: Optional[List[str]] = None):
        for ModuleName, AttrInfo in AttrInfos:
            if TargetScripts is not None:
                clones = Loader.CloneImport(ModuleName, clone_name=f"Clone_{ModuleName}")  
                if not clones:
                    continue
                Clone = clones[0]
                if Clone not in self.CloneLog:
                    self.CloneLog.append(Clone)

            SuccessChange = Modifier.DeleteAttr(Clone if TargetScripts else ModuleName, AttrInfo)
            if SuccessChange:
                self.LogChanges(self.ChangeLog, AttrInfo, key=ModuleName)

    def Revert(self, RevertInfo: Union[dict, list]):
        items = RevertInfo.items() if isinstance(RevertInfo, dict) else RevertInfo

        for Target, ImportList in items:
            try:
                targets = Loader.LoadModule(Target) 
                if not targets:
                    continue
                TargetMod = targets[0]

                for ImportName in ImportList:
                    CopyName = f"Clone_{ImportName}" if not ImportName.startswith("Clone_") else ImportName
                    if hasattr(TargetMod, CopyName):
                        delattr(TargetMod, CopyName)
                        logger.info(f"Reverted '{CopyName}' from '{Target}'")

                        mod_load = Loader.LoadModule(ImportName)
                        if mod_load and mod_load[0]:      
                            setattr(TargetMod, ImportName, mod_load[0])

                        self.GarbageCollect()
                    else:
                        print(f"Revert is not required for '{CopyName}'")
            except Exception as e:
                logger.error(f"Error during revert on target '{Target}': {e}")

    def GarbageCollect(self):
        attached_names = set()
        for _, cons in self.ConLog.items():
            for c in cons:
                attached_names.add(str(c))

        NotAttach = []
        for Clone in self.CloneLog:
            clone_name = getattr(Clone, "__name__", str(Clone))
            if clone_name not in attached_names:
                NotAttach.append(Clone)

        for Clone in NotAttach:
            if Clone in self.CloneLog:
                self.CloneLog.remove(Clone)
                clone_name = getattr(Clone, "__name__", str(Clone))
                if clone_name in sys.modules:
                    del sys.modules[clone_name]
                logger.info(f"Garbage collected unattached clone: '{clone_name}'")

    def LogChanges(self, Table, Value, key=None):
        if isinstance(Table, dict) and key is None:
            print("Key is required for dict logs")
            return

        if Value is None:
            print("Changes may have failed: Value is None")
            return

        if Table is self.ConLog or Table is self.ChangeLog:
            if key not in Table:
                Table[key] = [Value] if not isinstance(Value, list) else Value
            else:
                if isinstance(Value, list):
                    Table[key].extend([v for v in Value if v not in Table[key]])
                else:
                    if Value not in Table[key]:
                        Table[key].append(Value)

            if self.DataHandler:
                try:
                    self.DataHandler.Backet(Table)
                    if Table is self.ChangeLog:
                        self.DataHandler.Store("ChangeLog")
                    else:
                        self.DataHandler.Store("ConLog")
                except Exception as e:
                    logger.warning(f"DataHandler storage failed: {e}")

        elif Table is self.CloneLog:
            if Value not in Table:
                Table.append(Value)
                if self.DataHandler:
                    try:
                        self.DataHandler.Backet(Table)
                        self.DataHandler.Store("CloneLog")
                    except Exception as e:
                        logger.warning(f"DataHandler storage failed: {e}")
