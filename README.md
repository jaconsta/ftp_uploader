# FTP File uploader.

Designed to upload a complete folder to a remote FTP destination.

Coded fot FTPS but with 2 small changes works with FTP too.

## INSTRUCTIONS

**REMEMBER** unless specified your `PYTHON_HOME` is determined from the folder you execute the command.
That might affect your results.

## TEST BEFORE UPLOAD TO PRODUCTION

The test folder comes with two componens.

The `README` which contains quick instructions to create a test FTP server.

A folder `sourcedir` which contains the files to match default environment variable `SOURCEDIR`, 
and that are going to be uploaded by default.

The env var `USERNAME` by default contains the OS username, so be sure to set it before running the program.

To run it (and as a example of how the PYTHON_HOME is affected) run from this directory point.

```
# python src/main.py
```

If runs ok you would see, inside the FTP example server the following:

```
/
|-oh/
|---look/
|-----this/
|-------fifth/
|---------sixth.txt
|-------second/
|---------/...
|-------first.txt
```

**Note** the ´sourcedir´ folder is not uploaded by default, it should be defined on `WORKDIR`.

## CONTRIBUTIONS

Sure. Leave a PR or start a discussion thread.
