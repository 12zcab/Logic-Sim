# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )
# I have used AI to help me check errors 
# Son, this thing can self destruct

import importlib
import importlib.util
import logging
import pkgutil
import types
from pathlib import Path
import Source.modules.MutanterFile.Transformer as Transformer

# Import your data handler dependency
from Temp.Data import DataHandler

logging.basicConfig(level=logging.INFO)


class Loader:
    @staticmethod
    def LoadModule(TargetName):
        # Return Tables
        FoundItems = []
        if isinstance(TargetName, str):
            TargetName = [TargetName]

        for Target in TargetName:
            try:
                Found = importlib.import_module(Target)
                FoundItems.append(Found)
            except ImportError as e:
                logging.error(f"'{Target}' does not exist due to: {e}")

        return FoundItems

    @staticmethod
    def LoadModuleFromPath(Targets, prefix=""):
        # Return Table
        FoundItems = []
        Paths = []
        if not isinstance(Targets, list):
            Targets = [Targets]

        for Folder in Targets:
            Paths.append(Path(Folder).resolve())

        str_paths = [str(p) for p in Paths]
        for p in Paths:
            for _, modname, _ in pkgutil.iter_importers(str_paths):
                Target = f"{prefix}{modname}"
                try:
                    FoundItems.append(importlib.import_module(Target))
                except ImportError as e:
                    logging.error(f"'{Target}' does not exist due to: {e}")

        return FoundItems

    @staticmethod
    def LoadFiles(Targets, prefix="", FileType=".py"):
        # Completed method implementation
        if not isinstance(Targets, list):
            Targets = [Targets]

        FoundItems = []
        for Folder in Targets:
            dir_path = Path(Folder).resolve()
            if not dir_path.is_dir():
                continue

            for file_path in dir_path.glob(f"*{FileType}"):
                if file_path.name.startswith("__"):
                    continue
                mod_name = f"{prefix}{file_path.stem}"
                try:
                    spec = importlib.util.spec_from_file_location(
                        mod_name, file_path
                    )
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        FoundItems.append(mod)
                except Exception as e:
                    logging.error(f"Failed to load file module {file_path}: {e}")

        return FoundItems

    @staticmethod
    def CloneImport(TargetImport, clone_name=None):
        # Return table with True Isolated Spec Reloading
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
                    # Isolated reload from spec for true memory separation
                    spec = importlib.util.spec_from_file_location(new_name, mod_file)
                    if spec and spec.loader:
                        CloneModule = importlib.util.module_from_spec(spec)
                        CloneModule.__name__ = new_name
                        spec.loader.exec_module(CloneModule)
                        Clones.append(CloneModule)
                        continue
                except Exception as e:
                    logging.warning(f"Spec clone failed for {mod_name}, falling back to dynamic object: {e}")

            # Fallback for dynamic/builtin modules without disk files
            CloneModule = types.ModuleType(new_name)
            CloneModule.__name__ = new_name
            ignored_keys = (
                "__name__",
                "__loader__",
                "__spec__",
                "__file__",
                "__cached__",
                "__builtins__",
            )
            for key, value in Import.__dict__.items():
                if key not in ignored_keys:
                    setattr(CloneModule, key, value)
            Clones.append(CloneModule)

        return Clones


class Modifier:
    @staticmethod
    def ApplyAttr(TargetModule, Modinfo):
        # One by one attribute application
        SuccessChanges = []

        if isinstance(TargetModule, str):
            try:
                modules = Loader.LoadModule(TargetModule)
                if not modules:
                    return SuccessChanges
                Import = modules[0]
            except Exception as e:
                logging.error(f"Error resolving target module '{TargetModule}': {e}")
                return SuccessChanges
        else:
            Import = TargetModule

        Name = getattr(Import, "__name__", str(Import))

        # Support both List of Tuples and Dictionary inputs
        items = Modinfo.items() if isinstance(Modinfo, dict) else Modinfo

        for ModPart, Mod in items:
            if not isinstance(Mod, str):
                setattr(Import, str(ModPart), Mod)
                logging.info(f"'{ModPart}' has been replaced on '{Name}'")
                SuccessChanges.append(str(ModPart))
            else:
                try:
                    Compile = compile(Mod, f"<string_{ModPart}>", "exec")
                    exec(Compile, Import.__dict__)
                    logging.info(
                        f"'{ModPart}' has been compiled and attached to '{Name}'"
                    )
                    SuccessChanges.append(str(ModPart))
                except Exception as e:
                    logging.error(f"Execution failed for '{ModPart}': {e}")

        return SuccessChanges

    @staticmethod
    def DeleteAttr(TargetImport, AttrNames):
        # One by one attribute deletion
        if isinstance(TargetImport, str):
            try:
                modules = Loader.LoadModule(TargetImport)
                if not modules:
                    return None
                Import = modules[0]
            except Exception as e:
                logging.error(
                    f"{e} appeared as '{TargetImport}' is not loaded."
                )
                return None
        else:
            Import = TargetImport

        for AttrName in AttrNames:
            if hasattr(Import, AttrName):
                delattr(Import, AttrName)
                logging.info(f"Attribute '{AttrName}' deleted from '{getattr(Import, '__name__', 'Module')}'")

        return Import


class Handler:
    print(
        "This is more automatic but u can still use manually if u are cool"
    )

    def __init__(self):
        self.DataHandler = DataHandler.Handler()
        self.ConLog = {}
        self.ChangeLog = {}
        self.CloneLog = []

    def Connect(self, Info):
        for Target, Imports in Info:
            for Import in Imports:
                FoundList = Loader.LoadModule(Target)
                if not FoundList:
                    continue
                Found = FoundList[0]

                if not hasattr(Found, Import):
                    imported_mods = Loader.LoadModule(Import)
                    if imported_mods:
                        setattr(Found, Import, imported_mods[0])
                        found_name = getattr(Found, "__name__", str(Target))
                        self.ConLog.setdefault(found_name, []).append(Import)
                else:
                    print(f"No need to connect '{Import}' to '{Target}'")

    def Disconnect(self, ListInfo):
        for Target, Imports in ListInfo:
            for Import in Imports:
                FoundList = Loader.LoadModule(Target)
                if not FoundList:
                    continue
                Found = FoundList[0]

                if hasattr(Found, Import):
                    delattr(Found, Import)
                    found_name = getattr(Found, "__name__", str(Target))
                    if (
                        found_name in self.ConLog
                        and Import in self.ConLog[found_name]
                    ):
                        self.ConLog[found_name].remove(Import)
                else:
                    print(f"No need to disconnect '{Import}' from '{Target}'")

    def ApplyAttr(self, AttrInfos, TargetScripts=None):
        for ModuleName, AttrInfo in AttrInfos:
            if TargetScripts is not None:
                clones = Loader.CloneImport(
                    ModuleName, clone_name=f"Clone_{ModuleName}"
                )
                if not clones:
                    continue
                Clone = clones[0]

                SuccessChanges = Modifier.ApplyAttr(Clone, AttrInfo)

                self.LogChanges(self.CloneLog, Clone)
                self.LogChanges(
                    self.ChangeLog,
                    SuccessChanges,
                    key=getattr(Clone, "__name__", "Clone"),
                )

                for Target in TargetScripts:
                    targets = Loader.LoadModule(Target)
                    if targets:
                        Found = targets[0]
                        setattr(Found, Clone.__name__, Clone)
                        self.LogChanges(
                            self.ConLog,
                            Clone.__name__,
                            key=getattr(Found, "__name__", Target),
                        )
            else:
                SuccessChanges = Modifier.ApplyAttr(ModuleName, AttrInfo)
                self.LogChanges(
                    self.ChangeLog, SuccessChanges, key=ModuleName
                )

    def DeleteAttr(self, AttrInfos):
        for ModuleName, AttrInfo in AttrInfos:
            SuccessChange = Modifier.DeleteAttr(ModuleName, AttrInfo)
            self.LogChanges(self.ChangeLog, SuccessChange, key=ModuleName)

    def Revert(self, RevertInfo):
        items = RevertInfo.items() if isinstance(RevertInfo, dict) else RevertInfo

        for Target, ImportList in items:
            targets = Loader.LoadModule(Target)
            if not targets:
                continue
            TargetMod = targets[0]

            for ImportName in ImportList:
                CopyName = f"Clone_{ImportName}" if not ImportName.startswith("Clone_") else ImportName
                if hasattr(TargetMod, CopyName):
                    delattr(TargetMod, CopyName)
                    logging.info(f"Reverted '{CopyName}' from '{Target}'")
                else:
                    print(f"Revert is not required for '{CopyName}'")

    def GarbageCollect(self):
        # Collect all attached module names from ConLog values
        attached_names = set()
        for parent, cons in self.ConLog.items():
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
                logging.info(f"Garbage collected unattached clone: '{getattr(Clone, '__name__', Clone)}'")

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
                    Table[key].extend(Value)
                else:
                    Table[key].append(Value)

            self.DataHandler.Backet(Table)

            if Table is self.ChangeLog:
                self.DataHandler.Store("ChangeLog")
            else:
                self.DataHandler.Store("ConLog")

        elif Table is self.CloneLog:
            if Value not in Table:
                Table.append(Value)
                self.DataHandler.Backet(Table)
                self.DataHandler.Store("CloneLog")