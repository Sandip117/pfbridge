# This script describes by way of demonstration various explicit examples of
# how to interact with the pfbridge API using curl -s.
#
#   $ source \$PWD/workflow
#
# MAKE SURE ANY ENV VARIABLES SET BY THIS ARE WHAT YOU WANT!
#
#     * Feb-2023
#     Develop/deploy.
#

###############################################################################
#_____________________________________________________________________________#
# E N V                                                                       #
#_____________________________________________________________________________#
# Set the following variables appropriately for your local setup.             #
###############################################################################

#
# pfbridge service
#
# In some envs, this MUST be an IP address!
export pfbridge=http://localhost:33333
export pflink=http://localhost:8050

###############################################################################
#_____________________________________________________________________________#
# B U I L D                                                                   #
#_____________________________________________________________________________#
# Build the container image in a variety of difference contexts/use cases.    #
###############################################################################

build () {
# UID
# for fish:
# export UID=(id -u)
# for bash/zsh
export UID=$(id -u)
# Build (for fish shell syntax!)
docker build --build-arg UID=$UID -t local/pfbridge .
}

launch_quickndirty () {
# Quick 'n dirty run -- this is what you'll mostly do.
# Obviously change port mappings if needed (and in the Dockerfile)
docker run --rm -it                                                            \
        -p 33333:33333                                                         \
        local/pfbridge /start-reload.sh
}

launch_debug () {
# Run with support for source debugging
docker run --rm -it                                                            \
        -p 33333:33333                                                         \
        -v $PWD/pfbridge:/app:ro                                               \
        local/pfbridge /start-reload.sh
}

# To access the API swagger documentation, point a brower at:
export swaggerURL=":33333/docs"

randtime_generate () {
  range=$1
  shuf -i 1-$1 -n 1 | xargs -i% echo "scale = 4; %/1000"  | bc
}

###############################################################################
#_____________________________________________________________________________#
# R E L A Y  t e s t                                                          #
#_____________________________________________________________________________#
###############################################################################
# Relay and echo back to the test API endpoint of pflink                      #
###############################################################################
#

relayTest () {
  pflink="$1"
  curl -X 'POST' \
  '"$pfbridge"/api/v1/analyze/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "imageMeta": {
    "AccessionNumber": "",
    "PatientID": "",
    "PatientName": "",
    "PatientBirthDate": "",
    "PatientAge": "",
    "PatientSex": "",
    "StudyDate": "",
    "StudyDescription": "",
    "StudyInstanceUID": "12345678",
    "Modality": "",
    "ModalitiesInStudy": "",
    "PerformedStationAETitle": "",
    "NumberOfSeriesRelatedInstances": "",
    "InstanceNumber": "",
    "SeriesDate": "",
    "SeriesDescription": "",
    "SeriesInstanceUID": "12345678",
    "ProtocolName": "",
    "AcquisitionProtocolDescription": "",
    "AcquisitionProtocolName": ""
  },
  "analyzeFunction": "dylld"
}'
 | jq
}


#
# And we're done!
# _-30-_
#
