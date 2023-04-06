"""
This module provides "mapping" functionality that "maps" the data boundary
between the clinical caller and the ChRIS pflink workflow controller.

On the "input" side, i.e from the clinical service into `pfbridge`, the
clinical payload is "mapped" into one suitable for `pflink`.

On the "output" (or "return" from `pflink`) side, the `pflink` response
is mapped into a simpler resultant suitable for consumption by the clinical
service.
"""

from models         import relayModel
from config         import settings
import              httpx

class Map:
    """
    A class that maps or "transforms" JSON data across a boundary.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.mapName:str        = "dylld"
        self.mapContext:str     = "radstar"
        self.d_description: dict[str, str]      = \
        {
            "STARTED":          "Starting workflow",
            "RETRIEVING":       "Pulling image for analysis",
            "PUSHING":          "Pushing image into ChRIS",
            "REGISTERING":      "Registering image to ChRIS",
            "FEED_CREATED":     "Analysis created in ChRIS",
            "ANALYSIS_STARTED": "Analysis running in ChRIS",
            "COMPLETED":        "Results available in PACS"
        }
        for k, v in kwargs.items():
            if k == 'name'      : self.mapName  = v

    def intoPflink_transform(self, payload:relayModel.clientPayload) -> relayModel.pflinkInput:
        """
        Convert the payload received from the clinical service into
        a payload suitable for `pflink`.

        Args:
            payload (relayModel.clientPayload): the imageMeta to process and
                                                analysis to perform

        Returns:
            relayModel.pflinkInput: a payload suitable for relaying on to `pflink`.
        """
        pflinkPOST:relayModel.pflinkInput   = relayModel.pflinkInput()
        pflinkPOST.PACSdirective            = payload.imageMeta
        pflinkPOST.FeedName                 = payload.analyzeFunction
        match payload.analyzeFunction:
            case 'dylld':
                pflinkPOST.analysisArgs.PluginName   = settings.dylld.analysisPluginName
                pflinkPOST.analysisArgs.Version      = settings.dylld.analysisPluginArgs
        return pflinkPOST

    def fromPflink_transform(self, payload:httpx.Response) -> relayModel.clientResponseSchema:
        """
        The response that is ultimately returned back to the client. This is
        an edited subset of the actual response from pflink.

        Args:
            payload (relayModel.pflinkResponseSchema): the full response from
                                                       pflink

        Returns:
            relayModel.clientResponseSchema: the subset returned to the caller
        """
        toClinicalService:relayModel.clientResponseSchema   = relayModel.clientResponseSchema()
        fromPflink:dict             = payload.json()
        toClinicalService.Status    = self.d_description.get(fromPflink['WorkflowState'],
                                                                 "Unknown state encountered")
        if not fromPflink['StudyFound']:
            toClinicalService.Status    = "Image not found!"
        toClinicalService.Progress      = fromPflink['StateProgress']
        toClinicalService.ErrorWorkflow = fromPflink['Error']
        return toClinicalService
