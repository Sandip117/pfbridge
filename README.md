# `pfbridge`

[![Build](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/pfbridge/actions/workflows/build.yml)

*a rather simple relay bridge between two communicating entities -- intended as a translator within the ChRIS ecosystem between a clinical service and a CUBE controlling service*

## Abstract

`pfbridge` was developed to "bridge" communication between one service to another. One one side, an origin point is a program or service that has some basic metadata that defines a "function" to apply to some "data". The "data" in this case is typically some medical image data defined by a set of DICOM tags, and the "function" to apply is the name of a set of operations that are ultimately managed by CUBE. Controlling CUBE and shepherding its progress is a controller service called `pflink`. The `pflink` API requires more verbose data that is not really relevant to the original service -- for example a typical `pflink` payload contains information about several other services that are of no concern or interest to the originator.

Thus, `pfbridge` was conceived as a intermediary to buffer the originator from implementation details of concern. It accepts a much reduced `http` `POST` body, and repackages this body into the more detailed `pflink` body. Then, `pfbridge` transmits (or relays) this to `pflink` and captures the `pflink` response. Before returning this response to the original caller, `pfbridge` simplifies the response to return only success and status (and possible error) information.

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
# Set the workflow and testing URLs of the pflink instance
# to which we are bridging
export PRODURL=http://localhost:8050/workflow
export TESTURL=http://localhost:8050/testing

# For daemon, or background mode:
docker run --env PRODURL=$PRODURL --env TESTURL=$TESTURL                        \
               --name pfbridge  --rm -it                                        \
               -p 33333:33333                                                   \
               -v $PWD/pfbridge:/app:ro                                         \
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
# Set the workflow and testing URLs of the pflink instance
# to which we are bridging
export PRODURL=http://localhost:8050/workflow
export TESTURL=http://localhost:8050/testing

# Run with support for source debugging
docker run --name pfbridge  --rm -it                                              	\
        -p 33333:33333 	                                                                \
        -v $PWD/pfbridge:/app:ro                                                  	\
        local/pfbridge /start-reload.sh
```

## Using the helper `workflow.sh` script commands

The `workflow.sh` script can be sourced in `bash`/`zsh` to provide full CLI helper functions for complete access to the API.

```bash
cd pfbridge/pfbridge
# Assuming bash/zsh:
source workflow.sh
```
The following commands are defined:

* `pflinkURLs_get`: Get the `pflink` links.
* `testURL_set <URL>`: Set the `pflink` test URL.
* `prodURL_set <URL>`: Set the `pflink` production URL.
* `analysis_get`: Get the `analysis` relevant data.
* `analysis_set <key> <value>`: Set `analysis` relevant data.
* `relay <type> <StudyInstanceUID> <SeriesInstanceUID>`: Relay an analysis to perform.

## Tests

Proper tests coming soon. For now you can use the `workflow.sh` script to do some rudimentary testing. Successive calls to `relay test <study> <series>` will return to the caller all the major states through which `pflink` transits. Assuming you have fired up an instance of `pfbridge`:

```bash

# You can check how the `pflink` URLs are currently configured with:
❯ pflinkURLs_get
{
  "productionURL": "http://localhost:8050/workflow/",
  "testingURL": "http://localhost:8050/testing/"
}

# This assumes of course that you have a `pflink` instance running on `localhost:8050`.
# Let's assume not and try and hit the `testing` URL:
# Here we use two numeric arguments that correspond to the
# StudyInstanceUID and SeriesInstanceUID of a dummy test:

❯ relay test 1234567 1234567
{
  "Status": "Comms failure",
  "Progress": "n/a",
  "ErrorWorkflow": "n/a",
  "ErrorComms": {
    "error": "All connection attempts failed",
    "URL": "http://localhost:8050/testing/",
    "help": "Please check that the pflink URL is correct"
  }
}

# If we in fact get `pflink` properly up, we can test the testing URL:
❯ relay test 1234567 1234567
{
  "Status": "Initializing workflow",
  "Progress": "0%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}

❯ relay test 1234567 1234567
{
  "Status": "Pulling image for analysis",
  "Progress": "25%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}

❯ relay test 1234567 1234567
{
  "Status": "Pulling image for analysis",
  "Progress": "50%",
  "ErrorWorkflow": "",
  "ErrorComms": {
    "error": "",
    "URL": "",
    "help": ""
  }
}


```

_-30-_
