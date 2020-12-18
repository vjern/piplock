# piplock

Takes a python requirements file in input.

Fills in all missing version locks (defaults to latest pypi release).

With `requirements.txt` containing:
```
requests
pytest==5.0.0
```
this:
```
piplock requiremenst.txt > requirements.lock
```
results in:
```
requests==2.9.2
pytest==5.0.0
```

## Other options

Options always come after the `file` argument.

* `-c` can be used to produce a compact version (No comments or empty lines).
* `-v` enables verbose mode for debugging purposes.