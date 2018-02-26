## Abandon all hope, ye who enter here

This script is still in its infancy and is therefore subject to breaking or not doing what it's been intended to do.

## Introduction

Lemony is a simple batch file renaming script written in Python 3.6. Its goal is to allow users to rename their files using regular expressions.

## Getting Started

For now, clone / download the repo and run `lemony.py` with Python. As mentioned earlier, the script has been written targetting Python version 3.6.

### Usage

The following is an incomplete guide for using the script. Please refer to the [Wiki](https://github.com/JedBurke/Lemony/wiki) for more.

#### Basic

```
> lemony.py rename "path/to/files" --match "_+" --replace " "
```

What that does is rename all files in the specified directory, replacing the underscores (_) with a single space.

#### Dry run

It's a good idea to test your replacement before it happens. Use the `--dry-run` flag or its shortened form `-n` for this.

#### Multiple directories

To supply multiple directories, separate them with the semi-colon (;) character.

```
> lemony.py rename "path/to/directory;path/to/ecchi/pictures" -m "_" -r " "
```

#### Extensions & Exclusions

You have a directory with multiple file types and don't want to apply the replacement on all of them. Use the `--ext` option to include the file types to be renamed. To keep it simple, we're using the semi-colon to separate the files extensions. Notice the comma.

```
> lemony.py rename "path" --ext "txt;srt,ass"
```

In the case where you wish to allow all but exclude some, you'll use the `--blacklist` flag. All files will be processed except for those mention in the `--ext` argument.

#### Profiles

The main reason why the script exists as it does now is to be able to reuse for other renaming purposes.

"I may need to replace the underscores again, but I may need to replace other characters or do advanced text manipulation too." That was the thought I had and the reason why it is more than just a one-off script.

Simply put, profiles allow you to store and invoke commonly used operations. The profiles are contained in a JSON document under the name `profiles.json` in the main directory.

Here is an example of the profile structure:

```
{
    "_2s": {
        "match" : "_",
        "replace": " ",
        "whitelist": true
    }
}
```

The profile stated in the above section matches the replacement operation performed earlier.

Invoke as such:

```
> lemony.py rename "path/to/files" --profile _2s
```

You may also store a separate profile.json file in "~/.lemony" / "%HOMEPATH%\.lemony". The values from the local file will override those of the main one.

https://github.com/JedBurke/Lemony/wiki/Profiles

#### Need to know more?

At this point in time, the script itself is better friend in knowing how to use it.

```
> lemony.py --help
```


## Future

I originally wrote this script in Python because I wanted to get into Python having failed to see the appeal several times. Please keep in mind that it is shoddily written with below-novice proficiency in Python. Ideally, I'd like to fix the shoddy bits and make the script more robust.

Check issues with the ["Quality of Life"](https://github.com/JedBurke/Lemony/issues?q=is%3Aissue+is%3Aopen+label%3A%22quality+of+life%22) label for more.

## Bugs

While I am only able to test on Windows, I would appreciate any bug reports if it doesn't work as expected.

If you have any feature suggestions, please feel free to create an issue for one using the 'new feature' or 'enhancement' label.
