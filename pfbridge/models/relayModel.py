str_description = """

    The data models/schemas for the PACS QR collection.

"""

from    pydantic            import BaseModel, Field
from    typing              import Optional, List, Dict, Any
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

class pfdcmInfo(BaseModel):
    pfdcm_service:str               = settings.pfdcm.pfdcmServiceProvider
    PACS_service:str                = settings.pfdcm.PACSserviceProvider
    cube_service:str                = settings.pfdcm.CUBEandSwiftKey
    swift_service:str               = settings.pfdcm.CUBEandSwiftKey
    dicom_file_extension:str        = DICOMfile().extension
    db_log_path:str                 = db().path

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

class analysisModel(BaseModel):
    feed_name:str                  = settings.analysis.feedName
    user_name:str                  = settings.analysis.clinicalUser
    plugin_name:str                = ""
    plugin_version:str             = ""
    plugin_params:str              = ""
    pipeline_name:str              = ""

class pflinkInput(BaseModel):
    pfdcm_info:pfdcmInfo            = pfdcmInfo()
    PACS_directive:PACSqueryCore    = PACSqueryCore()
    workflow_info:analysisModel     = analysisModel()

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
    status: bool                    = False
    workflow_state: str             = ""
    state_progress: str             = "0%"
    feed_id: str                    = ""
    feed_name: str                  = ""
    error: str                      = ""

class clientResponseSchema(BaseModel):
    """
    The response ultimately received by the client. This is a modified
    subset of the pflinkResponseSchema
    """
    Status:bool                     = False
    State:str                       = ''
    Progress:str                    = ''
    ErrorWorkflow:str               = ''
    ModelViolation:Any              = None
    ErrorComms:pflinkError          = pflinkError()
