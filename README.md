etalpmet - a reverse template

# About

`etalpmet`, kurz `et` (this is the fist and last letter of the name), can calculate the mathematical inverse function of a template.

## Usage

- `et.py templatefile files..`
- If there are no files this prings the compiled template and gives return code 2
- If one of the files does not match the templatefile, the program stops and returs 1
- If all files are matching then the return code is 0

If you want to extract contents of a file, use the parantheses (`(...)`) in regexps.  These are written to stdout, line by line, in following format:
`File NumberOfMatch ValueMatched`

The template language is very simple:

- '{/regex/}' matches the given regex
- '{{}' is the escape for '{'.  Example: '{}' must be written as '{{}}'
- '{FN}' is for future use (special functions), however there are none yet

## Notes

- The input always is read line by line

- This is terribly incomplete

## License

This Works is placed under the terms of the Copyright Less License,
see file COPYRIGHT.CLL.  USE AT OWN RISK, ABSOLUTELY NO WARRANTY. 

Read:  This is free as in free beer, free speech and free man.
