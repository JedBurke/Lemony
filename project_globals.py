class Globals:    
    # The name of the project.
    PRODUCT = "Lemony"

    # The possessive name of the project.
    PRODUCT_POSS = "Lemony's"

    # The project's current version.
    VERSION = "0.7.1"

    # Todo: Use for separating the file types as well.
    PATH_SEPARATOR = ";"

    EXTENSION_SEPARATOR = ","

    PROFILES_FILE_NAME = "profiles.json"

    USER_DATA_DIR_NAME = ".lemony"

    SYSTEM_DATA_DIR_NAME = "settings"

    def get_version_str():
        return Globals.PRODUCT + " " + Globals.VERSION

