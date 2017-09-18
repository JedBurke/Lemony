## Abandon all hope, ye who enter here

This script is still in its infancy and is therefore subject to breaking or not doing what it's been designed to do.

## Introduction

Rename-py is a simple batch file renaming script written in Python 3.6. Its goal is to allow users to rename their files using regular expressions.

### Usage

The following is an incomplete usage guide in using the script.

#### Basic

```
> rename.py "path/to/files" --match "_+" --replace " "
```

What that does is rename all files in the specified directory, replacing the underscores (_) with a single space.

#### Dry run

It's a good idea to test your replacement before it happens. Use the `--dry-run` flag for this.

#### Multiple directories

To supply multiple directories, separate them with the semi-colon (;) character.

```
> rename.py "path/to/directory;path/to/ecchi/pictures" -m "_" -r " "
```

#### Extensions & Exclusions

You have a directory with multiple file types and don't want to apply the replacement on all of them. Use the `--ext` option to include the file types to be renamed. To keep it simple, we're using the semi-colon to separate the files extensions.

```
> rename "path" --ext "*.txt;*.srt,*.ass"
```

In the case where you wish to allow all but exclude some, you'll use the `--blacklist` flag. All files will be processed except for those mention in the `--ext` argument.

#### Profiles

The main reason why the script exists as it does now is to be able to reuse for other renaming purposes.

"I may need to replace the underscores again, but I may need to replace other characters or do advanced text manipulation too."

Simply put, profiles allow you to store and invoke commonly used operations. The profiles are contained in a JSON document under the name `profiles.json` in the main directory.

Here is an example of the profile structure:

```
{
    "_2s": {
        "match" : "_",
        "replace": " ",
        "ext": "*",
        "whitelist": true
    }
}
```

The profile stated in the above section matches the replacement operation performed earlier.

Invoke as such:

```
> rename.py "path/to/files" --profile _2s
```

#### Need to know more?

At this point in time, the script itself is your best friend in knowing how to use it.

```
> rename.py --help
```

## Future

The script was shoddily written with below-novice proficiency in Python. Ideally, I'd like to fix the shoddy bits and make the script more robust.

* Fix shoddy bits
* Check coding conventions
* Further document code
* Migrate to OOP
* Employ unit testing
* Employ passive logging

**Features**

* Allow pattern matching for the file names instead of relying on the extensions to filter the files

## Bugs

I would appreciate any bug reports if it doesn't work as expected.