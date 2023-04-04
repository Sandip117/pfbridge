# `pfbridge`

[![Build](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml)

*a rather simple relay bridge between a typical clinical program and a workflow coordinator*

## Abstract

`pfbridge` was developed to "bridge" communication between one service to another. More specifically, the core origin point is a program or service that has some basic metadata that defines a "function" to apply to some "data". More concretely, the "data" in this case is typically some medical image data defined by a set of DICOM tags, and the "function" to apply is the name of a set of operations that are ultimately managed by CUBE. Controlling CUBE and shepherding its progress is a controller service called `pflink`. The `pflink` API requires more verbose data that is not really relevant to the original service -- for example a typical `pflink` payload contains information about several other services that are of no concern or interest to the originator.

Thus, `pfbridge` was conceived as a intermediary to buffer the originator from implementation details of concern. It accepts a much reduced http POST body, and then repackages this body into the more detailed `pflink` body. Then, `pfbridge` transmits (or relays) this to `pflink` and simply returns the response it received to the caller.


## Getting and using

### Build

Build the latest docker image

```bash
# Pull repo...
gh repo clone FNNDSC/pfbridge
# Enter the repo...
cd pfbridge

# Set some vars
set UID (id -u) # THIS IF FOR FISH SHELLs
# export UID=$(id -u)  # THIS IS FOR BASH SHELLs
export PROXY="http://10.41.13.4:3128"

# Here we build an image called local/pfbridge
# Using --no-cache is a good idea to force the image to build all from scratch
docker build --no-cache --build-arg http_proxy=$PROXY --build-arg UID=$UID -t local/pfbridge .

# If you're not behind a proxy, then
docker build --no-cache --build-arg UID=$UID -t local/pfbridge .
```

## Deploy as background process

```bash
docker run --name pfbridge  --rm -it -d                                            \
        -p 33333:33333                                                          \
        local/pfbridge /start-reload.sh
```

### "Hello, `pfbridge`, you're looking good"

Using [httpie](https://httpie.org/), let's ask `pfbridge` about itself


```bash
http :33333/api/v1/about/
```

and say `hello` with some info about the system on which `pfbridge` is running:

```bash
http :33333/api/v1/hello/ echoBack=="Hello, World!"
```

For full exemplar documented examples, see `pfbridge/workflow.sh` in this repository as well as `HOWTORUN`. Also consult the `pfbridge/pfbridge.sh` script for more details.

### API swagger

Full API swagger is available. Once you have started `pfbridge`, and assuming that the machine hosting the container is `localhost`, navigate to [http://localhost:33333/docs](http://localhost:33333/docs) .


## Development

To debug code within `pfbridge` from a containerized instance, perform volume mappings in an interactive session:

```bash
# Run with support for source debugging
docker run --name pfbridge  --rm -it                                              	\
        -p 33333:33333 	                                                        \
        -v $PWD/pfbridge:/app:ro                                                  	\
        local/pfbridge /start-reload.sh
```

## Test

Coming soon!

_-30-_
