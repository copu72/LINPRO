"""ModuleName — excepciones personalizadas."""


class ModuleNameError(Exception):
    """Base exception for all ModuleName errors."""


class SpecificError(ModuleNameError):
    """Descripción del error específico."""
