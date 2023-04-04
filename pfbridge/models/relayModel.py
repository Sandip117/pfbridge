str_description = """

    The data models/schemas for the PACS QR collection.

"""

from    pydantic            import BaseModel, Field
from    typing              import Optional, List, Dict
from    datetime            import datetime
from    enum                import Enum
from    pathlib             import Path
import  pudb

class pacsService(BaseModel):
    provider:str                    = 'orthanc'

class pfdcmService(BaseModel):
    provider:str                    = 'PFDCMLOCAL'

class CUBEandSwiftKey(BaseModel):
    key:str                         = 'local'

class db(BaseModel):
    path:str                        = '/home/dicom/log'

class DICOMfile(BaseModel):
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

class imageDescriptor(BaseModel):
    headerMeta:dict                 = {}

class pacsModel(BaseModel):
    PFDCMservice:str                = pfdcmService().provider
    PACSservice:str                 = pacsService().provider
    PACSdirective:dict              = PACSqueryCore

class pypxModel(BaseModel):
    db:db
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

class feedModel(BaseModel):
    dblogbasepath:str               = db().path
    FeedName:str                    = ''
    User:str                        = 'radstar'
    analysisArgs:analysisModel

class pflinkInput(BaseModel):
    imageDetail:pacsModel
    thenArgs:dict                   = pypxModel
    pflinkMeta:feedModel

class clientPayload(BaseModel):
    imageMeta:dict                  = PACSqueryCore()
    analyzeFunction:str             = ''

class pflinkResponseSchema(BaseModel):
    """The Workflow status response Model"""
    StudyFound                          : bool = False
    WorkflowState                       : str  = ''
    StateProgress                       : str  = "0%"
    FeedId                              : str  = ""
    FeedName                            : str  = ""
    CurrentNode                         : list = []
    Message                             : str  = ""
    Error                               : str  = ""

