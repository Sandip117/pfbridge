class Pflink:
    prodURL:str             = 'http://localhost:8050/workflow'
    testURL:str             = 'http://localhost:8050/testing/'

class Dylld(Pflink):
    analysisPluginName:str  = 'pl-dylld'
    analysisPluginArgs:str  = ''
    clinicalUser:str        = 'radstar'
    analysisFeedName:str    = 'dylld-%SeriesInstanceUID'

pflink  = Pflink()
dylld   = Dylld()
