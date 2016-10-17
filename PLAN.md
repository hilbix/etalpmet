Planned features:

# Two-way templates

This will only be possible with a very limited set of templates for now.
Here is the catch:

- Only use `{VAR}` instead of `{/regex/}`.
- `VAR`s can be associated with following:
 - A literal value.  Then it is checked against this value.
 - A RegEx.  The RegEx then must match, such that the literal value of `VAR` is extracted.
 - An Input parameter.  The contents of `VAR` then is output as the input parameter
- Conditional use `{?VAR text}`.  Do not use other looping constructs.
  - This tries to match `VAR` on the input.  On a match the matched input is skipeed and `text` is processed.  Else nothing happens.
  - If `VAR` is a literal value, it must match the next input literally.
  - If `VAR` is a RegEx, the RegEx must match.

# Implement `te`

`te` is the forward function while `et` is the backward function
