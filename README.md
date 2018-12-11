# μFragments security tests

<img src="https://frgs3.s3.amazonaws.com/logo_centered_small.jpg" alt="Banner" width="100" />

[![Build Status](https://travis-ci.com/frgprotocol/uFragments-security-tests.svg?token=xxNsLhLrTiyG3pc78i5v&branch=master)](https://travis-ci.com/frgprotocol/uFragments-security-tests)

[Manticore](https://github.com/trailofbits/manticore) and [Echidna](https://github.com/trailofbits/echidna) scripts for testing μFragments.

## Building and Running the Docker Container

We have included a Dockerfile to set up and install the necessary versions of Manticore, Echidna, Solidity, and their associated dependencies.

```
$ docker build -t fragments-test .
$ docker run -it fragments-test
```

## Running the Echidna Tests

```
fragments@e31e5c314e2b:~$ cd echidna/
fragments@e31e5c314e2b:~/echidna$ ./run_echidna.sh
```

## Running the Manticore Validations

```
fragments@895f6f8a5476:~$ cd manticore/
fragments@895f6f8a5476:~/manticore$ python3 add_and_remove_source.py
```

This script formally validates that there is no way for the whitelist to be corrupted.

There is also a script `gons_invariant.py` that can be run similarly that validates the invariant that `_gonsPerFragment` always equals `TOTAL_GONS.div(_totalSupply)`. An incompatibility in Manticore 0.2.2 means that this script will fail due to an out of gas error, however, this will hopefully be fixed in the forthcoming release of Manticore.
