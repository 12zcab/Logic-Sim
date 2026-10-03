from Temp.Data import DataHandler

import copy
import importlib
import pkgutil
import logging
import types

from typing import *

logging.basicConfig(level=logging.INFO)


class Loader:

    @staticmethod
    def LoadModule(
        TargetNames: Union[
            List[str],
            str
        ]
    ):

        FoundItems = []

        if isinstance(TargetNames, str):
            TargetNames = [TargetNames]

        for Target in TargetNames:

            try:

                FoundItems.append(
                    importlib.import_module(Target)
                )

            except ImportError as e:

                print(
                    f"{Target} "
                    f"does not exist due to {e}"
                )

        return FoundItems

    @staticmethod
    def LoadFromPath(
        TargetPaths: str,
        prefix: str = ""
    ):

        FoundItems = []

        for _, modname, _ in pkgutil.iter_modules(
            [TargetPaths]
        ):

            Target = f"{prefix}{modname}"

            try:

                FoundItems.append(
                    importlib.import_module(Target)
                )

            except ImportError as e:

                print(
                    f"{Target} "
                    f"does not exist due to {e}"
                )

        return FoundItems

    @staticmethod
    def CloneImport(
        TargetImport,
        AssignName: str
    ):

        Imports = Loader.LoadModule(
            TargetImport
        )

        CloneImports = []

        for Import in Imports:

            CloneImport = types.ModuleType(
                AssignName
            )

            setattr(
                CloneImport,
                "__name__",
                AssignName
            )

            for key, value in Import.__dict__.items():

                if key not in (
                    "__name__",
                    "__loader__",
                    "__spec__"
                ):

                    try:

                        setattr(
                            CloneImport,
                            key,
                            copy.deepcopy(value)
                        )

                    except Exception:

                        setattr(
                            CloneImport,
                            key,
                            value
                        )

            CloneImports.append(
                CloneImport
            )

        return CloneImports


class Modifier:

    @staticmethod
    def ApplyAttr(
        TargetModule,
        Modinfo: Any
    ):

        try:

            Imports = Loader.LoadModule(
                TargetModule
            )

        except ImportError:

            print(
                "Import can not be found "
                "from ApplyMod"
            )

            return

        for Import in Imports:

            Name = getattr(
                Import,
                "__name__",
                "Unknown"
            )

            for ModPart, Mod in Modinfo:

                if callable(Mod):

                    setattr(
                        Import,
                        str(ModPart),
                        Mod
                    )

                    logging.info(
                        f"{ModPart} "
                        f"has been replaced"
                    )

                elif isinstance(Mod, str):

                    try:

                        Compiled = compile(
                            Mod,
                            "<dynamic>",
                            "exec"
                        )

                        exec(
                            Compiled,
                            Import.__dict__
                        )

                        logging.info(
                            f"{ModPart} "
                            f"has been compiled "
                            f"and attached to "
                            f"{Name}"
                        )

                    except Exception as e:

                        logging.info(
                            f"Compilation failed "
                            f"for {ModPart}: {e}"
                        )

                else:

                    setattr(
                        Import,
                        ModPart,
                        Mod
                    )

                    logging.info(
                        f"{ModPart} "
                        f"has been attached"
                    )

        return Imports

    @staticmethod
    def DeleteAttr(
        TargetImport,
        AttrNames
    ):

        try:

            Imports = Loader.LoadModule(
                TargetImport
            )

        except ImportError as e:

            logging.info(
                f"{e}"
            )

            return

        for Import in Imports:

            for AttrName in AttrNames:

                if hasattr(
                    Import,
                    AttrName
                ):

                    delattr(
                        Import,
                        AttrName
                    )

                    logging.info(
                        f"{AttrName} "
                        f"is deleted"
                    )

        return Imports


class Handler:

    print(
        "This is more automatic but "
        "u can still use manually "
        "if u are cool"
    )

    def __init__(self):

        self.Data = {}

    def Connect(
        self,
        TargetList
    ):

        for Target, Imports in TargetList:

            Found = Loader.LoadModule(
                Target
            )[0]

            for ImportName in Imports:

                if not hasattr(
                    Found,
                    ImportName
                ):

                    setattr(
                        Found,
                        ImportName,
                        Loader.LoadModule(
                            ImportName
                        )[0]
                    )

                else:

                    print(
                        "No need from Connect"
                    )

    def Disconnect(
        self,
        TargetList
    ):

        for Target, Imports in TargetList:

            Found = Loader.LoadModule(
                Target
            )[0]

            for ImportName in Imports:

                if hasattr(
                    Found,
                    ImportName
                ):

                    delattr(
                        Found,
                        ImportName
                    )

                else:

                    print(
                        "No need from Disconnect"
                    )

    def ApplyAttr(
        self,
        AttrInfos,
        TargetScripts=None
    ):

        CloneModules = []

        for ModuleName, AttrInfo in AttrInfos:

            if TargetScripts:

                Clone = Loader.CloneImport(
                    ModuleName,
                    f"Clone_{ModuleName}"
                )[0]

                CloneModules.append(
                    Clone
                )

                for Part, Value in AttrInfo:

                    OldValue = getattr(
                        Clone,
                        Part,
                        None
                    )

                    self.Data.setdefault(
                        ModuleName,
                        []
                    ).append(
                        (
                            Part,
                            OldValue
                        )
                    )

                    setattr(
                        Clone,
                        Part,
                        Value
                    )

                for Target in TargetScripts:

                    setattr(
                        Loader.LoadModule(
                            Target
                        )[0],
                        Clone.__name__,
                        Clone
                    )

            else:

                Module = Loader.LoadModule(
                    ModuleName
                )[0]

                self.Data.setdefault(
                    ModuleName,
                    []
                )

                for Part, Value in AttrInfo:

                    OldValue = getattr(
                        Module,
                        Part,
                        None
                    )

                    self.Data[
                        ModuleName
                    ].append(
                        (
                            Part,
                            OldValue
                        )
                    )

                Modifier.ApplyAttr(
                    ModuleName,
                    AttrInfo
                )

        return CloneModules

    def DeleteAttr(
        self,
        AttrInfos
    ):

        for ModuleName, AttrInfo in AttrInfos:

            Modifier.DeleteAttr(
                ModuleName,
                AttrInfo
            )

    def Revert(
        self,
        RevertInfo
    ):

        if not isinstance(
            RevertInfo,
            (dict, list, tuple)
        ):
            return

        if isinstance(
            RevertInfo,
            dict
        ):
            Items = RevertInfo.items()
        else:
            Items = RevertInfo

        for Target, ImportList in Items:

            TargetModule = (
                Loader.LoadModule(
                    Target
                )[0]
            )

            for ImportName in ImportList:

                CopyName = (
                    f"Clone_{ImportName}"
                )

                if hasattr(
                    TargetModule,
                    CopyName
                ):

                    delattr(
                        TargetModule,
                        CopyName
                    )

            if ImportName in self.Data:

                Module = Loader.LoadModule(
                    ImportName
                )[0]

                for (
                    AttrName,
                    OldValue
                ) in reversed(
                    self.Data[
                        ImportName
                    ]
                ):

                    if OldValue is None:

                        if hasattr(
                            Module,
                            AttrName
                        ):

                            delattr(
                                Module,
                                AttrName
                            )

                    else:

                        setattr(
                            Module,
                            AttrName,
                            OldValue
                        )

                self.Data[
                    ImportName
                ].clear()
