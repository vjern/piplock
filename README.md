# piplock

Takes a python requirements file in input. Outputs the file as is in addition to frozen versions for the unlocked requirements found in the file, eg:

requirements.txt

```
requests
pytest==5.0.0
```
with
```
piplock requiremenst.txt > requirements.lock
```
becomes
```
requests==2.9.2
pytest==5.0.0
```
