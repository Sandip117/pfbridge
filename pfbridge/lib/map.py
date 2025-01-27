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
            "UNKNOWN":                   "An unknown state was encounted",
            "initializing workflow":     "Initializing workflow",
            "retrieving from PACS":      "Pulling image for analysis",
            "pushing to swift":          "Pushing image into ChRIS",
            "registering to CUBE":       "Registering image to ChRIS",
            "feed created":              "Analysis created in ChRIS",
            "analyzing study":           "Analysis running in ChRIS",
            "completed":                 "Results available in PACS"
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
        pflinkPOST:relayModel.pflinkInput    = relayModel.pflinkInput()
        pflinkPOST.PACS_directive            = payload.imageMeta
        pflinkPOST.workflow_info.feed_name   = payload.analyzeFunction
        match payload.analyzeFunction:
            case 'dylld':
                pflinkPOST.workflow_info.plugin_name   = settings.analysis.pluginName
                pflinkPOST.workflow_info.plugin_params = settings.analysis.pluginArgs
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
        toClinicalService.State    = self.d_description.get(fromPflink.get('workflow_state',
                                                                            'UNKNOWN'),
                                                                 "Unknown state encountered")
        if not 'status' in fromPflink.keys():
            # Here the response from the client violates its own response model!
            toClinicalService.ModelViolation  = fromPflink
            return toClinicalService
        if not fromPflink['status']:
            toClinicalService.State     = "Workflow failed. Please check any error messages."
        toClinicalService.Status        = fromPflink['status']
        toClinicalService.Progress      = fromPflink['state_progress']
        toClinicalService.ErrorWorkflow = fromPflink['error']
        return toClinicalService
