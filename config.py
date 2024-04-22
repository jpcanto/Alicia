from os import environ

config = {
    "DEBUG_LEVEL": environ.get("DEBUG_LEVEL", "INFO").upper(),
}
