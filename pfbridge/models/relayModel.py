str_description = """

    The data models/schemas for the PACS QR collection.

"""

from    pydantic            import BaseModel, Field
from    typing              import Optional, List, Dict
from    datetime            import datetime
from    enum                import Enum
from    pathlib             import Path
import  pudb
from    config              import settings

class pacsService(BaseModel):
    """Name of the PACS service provider"""
    provider:str                    = 'orthanc'

class pfdcmService(BaseModel):
    """Name of the PFDCM service provider -- relevant to ChRIS"""
    provider:str                    = 'PFDCMLOCAL'

class CUBEandSwiftKey(BaseModel):
    """Lookup key for CUBE and swift information -- relevant to ChRIS"""
    key:str                         = 'local'

class db(BaseModel):
    """Path of the ChRIS managed PACS filesystem database"""
    path:str                        = '/home/dicom/log'

class DICOMfile(BaseModel):
    """Explicit extention of DICOMS -- relevant to ChRIS"""
    extension:str                   = 'dcm'

class PACSqueryCore(BaseModel):
    """The PACS Query model"""
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

class pypxModel(BaseModel):
    db:str                          = db().path
    swift:str                       = CUBEandSwiftKey().key
    CUBE:str                        = CUBEandSwiftKey().key
    swiftServicesPACS:str           = pacsService().provider
    swiftPackEachDICOM:bool         = True
    parseAllFilesWithSubstr:str     = DICOMfile().extension

class analysisModel(BaseModel):
    PluginName:str                  = ''
    Version:str                     = ''
    Params:str                      = ''
    PassUserCreds:bool              = False

class pflinkInput(BaseModel):
    PFDCMservice:str                = pfdcmService().provider
    PACSservice:str                 = pacsService().provider
    PACSdirective:PACSqueryCore     = PACSqueryCore()
    thenArgs:pypxModel              = pypxModel()
    dblogbasepath:str               = db().path
    FeedName:str                    = settings.dylld.analysisFeedName
    User:str                        = settings.dylld.clinicalUser
    analysisArgs:analysisModel      = analysisModel()

class clientPayload(BaseModel):
    imageMeta:PACSqueryCore         = PACSqueryCore()
    analyzeFunction:str             = ''

class pflinkError(BaseModel):
    """
    A model returned when a pflink connection error has been flagged
    """
    error:str                       = ""
    URL:str                         = ""
    help:str                        = ""

class pflinkURLs(BaseModel):
    productionURL:str               = settings.pflink.prodURL
    testingURL:str                  = settings.pflink.testURL

class pflinkResponseSchema(BaseModel):
    """
    The Workflow status response model. This is the return from pflink.
    """
    StudyFound:bool                 = False
    WorkflowState:str               = ''
    StateProgress:str               = "0%"
    FeedId:str                      = ""
    FeedName:str                    = ""
    CurrentNode:list                = []
    Message:str                     = ""
    Error:str                       = ""

class clientResponseSchema(BaseModel):
    """
    The response ultimately received by the client. This is a modified
    subset of the pflinkResponseSchema
    """
    Status:str                      = ''
    Progress:str                    = ''
    ErrorWorkflow:str               = ''
    ErrorComms:pflinkError          = pflinkError()
