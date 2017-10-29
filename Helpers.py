import re

class FileHelpers():
  """ Converts a string of directories to a list using pre-defined delimiters 
      without checking the existence of said directories. """
  def parse_directories(directory_str, pattern=None):
    # Todo: Use the code from parse_extensions.
    return


  """ Converts a string of extensions to a list 
      using pre-defined delimiters. """
  def parse_extensions(extension_str, pattern=None):
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


class PatternHelpers:
  """ Compiles a regex pattern from string with options. """
  def parse_regex(pattern, enable_delimiter = True):
    capture = r"^(?!<\/)/(?P<pattern>.*)/(?P<flags>.*)?$"
    parsed_pattern = ""
    parsed_flags = 0

    if enable_delimiter:
      m = re.match(capture, pattern)

      if m != None:
        if m.groups("pattern"):
          parsed_pattern = m["pattern"]

        if m.groups("flags"):
          for flag in m["flags"]:
            flag = flag.casefold()
            
            if flag == "a":
              parsed_flags |= re.ASCII 

            elif flag == "i":
              parsed_flags |= re.IGNORECASE 

            elif flag == "l":
              parsed_flags |= re.LOCALE

            elif flag == "m":
              parsed_flags |= re.MULTILINE

            elif flag == "s":
              parsed_flags |= re.DOTALL

            elif flag == "x":
              parsed_flags |= re.VERBOSE

            else:
              return None


      else:
        parsed_pattern = pattern

    else:
      parsed_pattern = pattern


    if parsed_pattern.startswith("\/"):
      parsed_pattern = parsed_pattern[1:]

    return re.compile(parsed_pattern, parsed_flags)
