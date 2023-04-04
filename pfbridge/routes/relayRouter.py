str_description = """
    This route module handles logic pertaining to associating
    routes to actual logic in the controller module. For the
    most part, this module mostly has route method defintions
    and UI swagger for documentation.

    In most methods, the actual logic is simply a call out
    to the real method in the controller module that performs
    the application logic.
"""


from    fastapi             import  APIRouter, Query, HTTPException, BackgroundTasks, Request
from    fastapi.encoders    import  jsonable_encoder
from    typing              import  List, Dict

from    models              import  relayModel
from    controllers         import  relayController

from    datetime            import datetime, timezone
import  pudb

router          = APIRouter()
router.tags     = ['Relay services']

# @router.put(
#     "/log/{logObj}/",
#     response_model  = logModel.logInit,
#     summary         = "PUT information to a (possibly new) pftel object"
# )
# async def logSetup_put(
#     logObj          : str,
#     logSetupData    : logModel.logCore
# ) -> logModel.logInit:
#     """
#     Description
#     -----------
#     PUT an entire object. If the object already exists, overwrite.
#     If it does not exist, append to the space of available objects.
#     """
#     return logController.internalObject_initOrUpdate(
#         logObj, logSetupData
#     )

# @router.post(
#     '/relay/',
#     response_model  = logModel.logResponse,
#     summary         = '''
#     Use this API route to POST a simple log payload to the
#     logger.
#     '''
# )
# async def slog_write(
#     logPayload      : logModel.logSimple,
#     request         : Request,
#     logObject       : str   = 'default',
#     logCollection   : str   = 'slog',
#     logEvent        : str   = 'log'
# ) -> logModel.logResponse:
#     """
#     Description
#     -----------

#     Use this API entry point to simply record some log string.
#     `slog` entries are by default logged to `default/slog/<count>-log`
#     but this can be overriden with appropriate query parameters.

#     ```
#     {
#         log  : str   = ""
#     }
#     ```

#     Internally, they are mapped to a complete *telemetry* model for
#     consistent processing.

#     """
#     # pudb.set_trace()
#     d_ret:logModel.logResponse = logController.slog_save(
#         logPayload,
#         request,
#         object      = logObject,
#         collection  = logCollection,
#         event       = logEvent)
#     return d_ret


@router.post(
    '/analyze/',
    response_model  = relayModel.pflinkResponseSchema,
    summary         = '''
    POST an image and analysis directive that is relayed (after some
    internal processing) to a remote service.
    '''
)
async def workflow_do(
    relayPayload    : relayModel.clientPayload,
    request         : Request
) -> relayModel.pflinkResponseSchema:
    """
    Description
    -----------

    Main API entry-point that controls an analysis on an image
    data set and immediately returns a status update to the
    caller. Multiple calls with the same payload return current
    status of the workflow (or its completion).

    ```
    class clientPayload(BaseModel):
        imageMeta:dict                  = PACSqueryCore()
        analyzeFunction:str             = ''
    ```

    where imageMeta defines the DICOM tags specifying the image to
    analyze and the `analyzeFunction` the analysis to perform by
    the ChRIS system.

    ```
    class PACSqueryCore(BaseModel):
        AccessionNumber                     : str   = ""
        PatientID                           : str   = ""
        PatientName                         : str   = ""
        PatientBirthDate                    : str   = ""
        PatientAge                          : str   = ""
        PatientSex                          : str   = ""
        StudyDate                           : str   = ""
        StudyDescription                    : str   = ""
        StudyInstanceUID                    : str   = ""
        Modality                            : str   = ""
        ModalitiesInStudy                   : str   = ""
        PerformedStationAETitle             : str   = ""
        NumberOfSeriesRelatedInstances      : str   = ""
        InstanceNumber                      : str   = ""
        SeriesDate                          : str   = ""
        SeriesDescription                   : str   = ""
        SeriesInstanceUID                   : str   = ""
        ProtocolName                        : str   = ""
        AcquisitionProtocolDescription      : str   = ""
        AcquisitionProtocolName             : str   = ""
    ```

    A response on the status of the workflow is immediately returned

    """
    # pudb.set_trace()
    d_ret:relayModel.pflinkResponseSchema = relayController.relayAndReply(
            relayPayload, request
    )
    return d_ret

# @router.get(
#     "/log/",
#     response_model  = List,
#     summary         = """
#     GET the list of configured log element objects
#     """
# )
# async def logList_get() -> list:
#     """
#     Description
#     -----------
#     GET the list of configured log element objects handlers.
#     These objects constitute the most general level of log aggregation.
#     At this level, each handler can be thought of as a handler for a
#     large group of logging collections.
#     """
#     return logController.internalObjects_getList()

# @router.get(
#     "/log/{logObject}/info/",
#     response_model  = logModel.logInit,
#     summary         = "GET the meta information for a given log object"
# )
# async def logInfo_getForObject(
#     logObject: str
# ) -> dict:
#     """
#     Description
#     -----------
#     GET the setup info pertinent to a log object element called `logName`.
#     """
#     return logController.internalObject_getInfo(logObject)

# @router.get(
#     "/log/{logObject}/collections/",
#     response_model  = List,
#     summary         = """
#     GET the collections that constitute this log object
#     """
# )
# async def logCollections_getForObject(
#     logObject: str
# ) -> list:
#     """
#     Description
#     -----------
#     GET the list of collections in `logObject`. A _collection_ gathers
#     a set of events. For instance, a _collection_ called **02Feb2024** could
#     collect all events from the 2nd Feb 2024.
#     """
#     return logController.internalObject_getCollections(logObject)

# @router.get(
#     "/log/{logObject}/{logCollection}/events/",
#     response_model  = List,
#     summary         = """
#     GET the events that exist in the log object collection.
#     """
# )
# async def logEvents_getForObjectCollection(
#     logObject:str,
#     logCollection:str
# ) -> list:
#     """
#     Description
#     -----------
#     GET the list of events that have sent telemtryto the `logCollection`
#     of `logObject`.
#     """
#     return logController.internalObjectCollection_getEvents(
#         logObject,
#         logCollection
#     )

# @router.get(
#     "/log/{logObject}/{logCollection}/{logEvent}/",
#     response_model  = Dict,
#     summary         = """
#     GET a specific event that exists in this log object collection.
#     """
# )
# async def logEvent_getForObjectCollection(
#     logObject:str,
#     logCollection:str,
#     logEvent:str
# ) -> dict:
#     """
#     Description
#     -----------
#     GET the specific details of event `logEvent` in the collection
#     `logCollection` of the object `logObject`.
#     """
#     return logController.internalObjectCollection_getEvent(
#         logObject,
#         logCollection,
#         logEvent
#     )


# @router.delete(
#     "/log/{logObject}/{logCollection}/",
#     response_model  = logModel.logDelete,
#     summary         = """
#     DELETE all the events comprising this log object.
#     """
# )
# async def log_getForObjectCollection(
#     logObject:str,
#     logCollection:str
# ) -> bool:
#     """
#     Description
#     -----------
#     DELETE all the events in the collection `logCollection` of the object
#     `logObject`. Use with care!
#     """
#     return logController.internalObjectCollection_delete(
#         logObject,
#         logCollection
#     )

# @router.get(
#     "/log/{logObject}/{logCollection}/",
#     response_model  = List,
#     summary         = """
#     GET all the events comprising this log object collection as
#     a list of JSON objects.
#     """
# )
# async def log_getForObjectCollection(
#     logObject:str,
#     logCollection:str
# ) -> list:
#     """
#     Description
#     -----------
#     GET all the events in the collection `logCollection` of the object
#     `logObject` as a JSON return.
#     """
#     return logController.internalObjectCollection_get(
#         logObject,
#         logCollection
#     )

# @router.get(
#     "/log/{logObject}/{logCollection}/csv",
#     response_model  = str,
#     summary         = """
#     GET all the events comprising this log object collection as
#     a CSV formatted string
#     """
# )
# async def log_getForObjectCollectionAsCSV(
#     logObject:str,
#     logCollection:str,
#     style:str       = 'plain',
#     padding:bool    = False,
#     fields:str      = ''
# ) -> str:
#     """
#     Description
#     -----------
#     GET all the events in the collection `logCollection` of the object
#     `logObject` as a CSV formatted string.

#     By passing a URL query as `style=fancy` a _fancy_ CSV payload is
#     returned. Passing a comma-separated string of `fields=<strlist>`
#     will only return the `strlist` tokens in the CSV.
#     """
#     # pudb.set_trace()
#     return logController.internalObjectCollection_getCSV(
#         logObject,
#         logCollection,
#         format          = style,
#         applyPadding    = padding,
#         fields          = fields
#     )

# @router.get(
#     "/log/{logObject}/{logCollection}/stats",
#     response_model  = dict,
#     summary         = """
#     GET stats on the specified log object collection. The column to
#     process is specified in the optional query parameter.
#     """
# )
# async def log_getStatsForObjectCollection(
#     logObject:str,
#     logCollection:str,
#     key:str         = 'execTime',
# ) -> dict:
#     """
#     Description
#     -----------
#     GET statistics on all the events in the collection `logCollection` of
#     the object `logObject`.

#     The URL query `key=<key>` specifies the actual key field in the event
#     collection to process. This field key must contain numeric values.
#     """
#     # pudb.set_trace()
#     return logController.internalObjectCollection_getStats(
#         logObject,
#         logCollection,
#         column          = key
#     )

# @router.get(
#     "/log/{logObject}/stats",
#     response_model  = dict,
#     summary         = """
#     GET stats on the specified log object collection. The column to
#     process is specified in the optional query parameter. A dictionary
#     of keys where each key is one object collection is returned.
#     """
# )
# async def log_getStatsForObject(
#     logObject:str,
#     key:str         = 'execTime',
# ) -> dict:
#     """
#     Description
#     -----------
#     GET a dictionary keyed on collections of all the collections events
#     of object `logObject`. The stats of each collection are returned without
#     further processing.

#     The URL query `key=<key>` specifies the actual key field in the event
#     collection to process. This field key must contain numeric values.
#     """
#     # pudb.set_trace()
#     return logController.internalObject_getStats(
#         logObject,
#         column          = key
#     )

# @router.get(
#     "/log/{logObject}/stats_process",
#     response_model  = dict,
#     summary         = """
#     GET processed stats on the entire specified log object collection. The
#     column to process is specified in the optional query parameter.
#     """
# )
# async def log_processStatsForObject(
#     logObject:str,
#     key:str         = 'execTime',
# ) -> dict:
#     """
#     Description
#     -----------
#     GET a processed result of all the events in all the collections
#     of object `logObject`. A single dictionary `allCollections` is returned.

#     The URL query `key=<key>` specifies the actual key field in the event
#     collection to process. This field key must contain numeric values.
#     """
#     # pudb.set_trace()
#     return logController.internalObject_getStatsCumulative(
#         logObject,
#         column          = key
#     )

