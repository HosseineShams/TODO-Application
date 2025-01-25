from tasks.config import AppConfig

# Access the singleton instance
config = AppConfig()

# Retrieve a configuration value
print("Default Pagination Size:", config.default_pagination_size)
print("JWT Access Token Lifetime (minutes):", config.jwt_access_token_lifetime_minutes)

# Update a configuration
config.update_config('default_pagination_size', 20)
print("Updated Pagination Size:", config.default_pagination_size)

# Attempt to access a non-existent configuration
try:
    print(config.get_config('non_existent_key'))
except AttributeError as e:
    print(e)
