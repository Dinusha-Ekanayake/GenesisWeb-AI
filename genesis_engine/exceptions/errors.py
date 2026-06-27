class GenesisEngineError(Exception):
    """Base exception for all Genesis Engine errors."""
    pass

class PluginRegistrationError(GenesisEngineError):
    pass

class EngineInitializationError(GenesisEngineError):
    pass
