import re

class FileHelpers():
  """ Convert a string of extensions to a list using pre-defined delimiters. """
  def parse_extensions(extension_str, pattern = None):
    WHITESPACE_SEPARATOR_REGEX = "\s?"
    PATH_SEPARATOR = ";"
    EXTENSION_SEPARATOR = ","

    pattern = f"[{PATH_SEPARATOR}{EXTENSION_SEPARATOR}{WHITESPACE_SEPARATOR_REGEX}]"
    strip_regex = re.compile("^\s?$")

    if pattern != None:
      ext_pattern = pattern

    ext_list = re.split(ext_pattern, extension_str)
    
    for ext in ext_list:      
      if strip_regex.search(ext) != None:
        ext_list.remove(ext)

    # Todo: Remove duplicates.

    strip_regex = None

    return ext_list

print(FileHelpers.parse_extensions("mkv, ass, srt"))