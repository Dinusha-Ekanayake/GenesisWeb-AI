class GenesisException(Exception):
    """Base exception for Genesis Control Plane."""
    pass

class WorkspaceNotFoundError(GenesisException):
    pass

class ArtifactNotFoundError(GenesisException):
    pass

class GraphNotFoundError(GenesisException):
    pass

class WorkspaceSecurityError(GenesisException):
    def __init__(self, message: str, is_binary: bool = False):
        super().__init__(message)
        self.is_binary = is_binary

class CompilerTamperError(GenesisException):
    pass
