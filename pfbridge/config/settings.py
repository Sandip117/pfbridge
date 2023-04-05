class pflink:
    URL:str                 = 'http://havana.tch.harvard.edu:8050/testing/'

class dylld(pflink):
    analysisPluginName:str  = 'pl-dylld'
    analysisPluginArgs:str  = ''
    clinicalUser:str        = 'radstar'
    analysisFeedName:str    = 'dylld-%SeriesInstanceUID'
