
import config
import re

# clean_output(text, context)
# This utility function accepts a text string and "context" tag indicating what the string represents, and
# applies rules to clean it up for return.
def clean_output(text, context=False):
  stripped = text.strip(" ")

  # an empty dates range, "( - )", return nothing
  if stripped == "( - )":
    return ""

  # any date string leading with @
  if context == "date":
    return re.sub('@.+@', '', text).strip(" ")

  return stripped

# return_empty(value)
def return_empty(value):
  if value is None:
    return ""
  stripped = value.strip(" ")
  return stripped

# return id from an id_xref element
def get_id(obj):
  (first, s, last) = obj.xref_id.split("@")
  prefix = s[0].lower()
  n = int(s[1:])
  id = f"{prefix}{n:05d}"
  return id


# open an iXXXXX.md or fXXXXX.md file in the specified mode and return the file pointer
def open_md(id, mode):
  # open a file at {opath}/{id}.md
  path = f"{config.opath}{id}.md"

  # if mode is 'w' or 'r' open the file and return
  if mode in "wr":
    f = open(path, mode)
    return f

  # if mode is 'a' make sure we rewind one line!
  if mode == "a":
    f = open(path, "r")
    lines = f.readlines()
    lines = lines[:-1]
    f = open(path, "w")
    for line in lines:
      f.write(line)
    return f
