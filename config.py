from os import environ

config = {
    "DEBUG_LEVEL": environ.get("DEBUG_LEVEL", "INFO").upper(),
    "GMAIL_PASS": environ.get("GMAIL_PASSWORD", "password"),
    "GMAIL_USR": environ.get("GMAIL_USER", "email"),
    "PHONE_NUMBER": environ.get("PHONE_NUMBER", "whatsappnumber"),
    "LOCAL_APPDATA": environ.get("LOCALAPPDATA", ""),
}
