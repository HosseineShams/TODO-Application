class AppConfig:
    """Singleton class for managing application-level configurations."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize default configurations."""
        self.default_pagination_size = 10
        self.jwt_access_token_lifetime_minutes = 30
        self.jwt_refresh_token_lifetime_days = 1
        self.default_task_priority = 'medium'

    def update_config(self, key: str, value):
        """Update a configuration dynamically."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"Configuration '{key}' does not exist.")

    def get_config(self, key: str):
        """Retrieve a configuration value."""
        if hasattr(self, key):
            return getattr(self, key)
        raise AttributeError(f"Configuration '{key}' does not exist.")
