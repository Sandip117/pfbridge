import  os
from    pydantic    import BaseSettings

class Pflink(BaseSettings):
    prodURL:str             = 'http://localhost:8050/api/v1/workflow'
    testURL:str             = 'http://localhost:8050/api/v1/testing'

class DylldAnalysis(Pflink):
    pluginName:str          = 'pl-dylld'
    pluginArgs:str          = ''
    clinicalUser:str        = 'radstar'
    feedName:str            = 'dylld-%SeriesInstanceUID'

class Pfdcm(BaseSettings):
    pfdcmServiceProvider: str          = 'PFDCMLOCAL'
    PACSserviceProvider: str           = 'orthanc'
    CUBEandSwiftKey: str               = 'local'


pflink          = Pflink()
analysis        = DylldAnalysis()
pfdcm           = Pfdcm()
