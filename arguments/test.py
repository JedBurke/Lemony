# The test argument is intended to allow users to test their profiles
# and configuration against mock files and directories.

# Why not use `-n` or `--dry-run`?
# Dry run does everything except perform the action. It uses the live
# directory. `test` is a sandbox area with arbitrary files, 
# filenames, and, structures. 

# To get this fully functional, the `rename` code must be
# modularized to the point where mock functions may be inserted for
# the real ones.


# The following command stores the actual structure of <dir> in a
# file and names it based on the value specified by `--name`.
# > lemony test collect <dir> --name goldenboy

# Performs the rename action against a stored directory with the
# profile specified by `-p`.
# > lemony test -p goldenboy --collected_dir goldenboy

# Runs the same test as above, however it usese a live directory.
# > lemony test -p goldenboy --dir <dir>

# These tests perform the action, but nothing is touched in the
# filesystem.
