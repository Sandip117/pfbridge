str_description = """
    This module contains logic pertinent to the PACS setup "subsystem"
    of the `pfdcm` service.
"""

from    concurrent.futures  import  ProcessPoolExecutor, ThreadPoolExecutor, Future

from    fastapi             import  APIRouter, Query, Request
from    fastapi.encoders    import  jsonable_encoder
from    fastapi.concurrency import  run_in_threadpool
from    pydantic            import  BaseModel, Field
from    typing              import  Optional, List, Dict, Callable, Any

import  numpy               as      np
from    scipy               import  stats

from    .jobController      import  jobber
import  asyncio
import  subprocess
from    models              import  relayModel
import  logging
import  os
from    datetime            import  datetime

import  pudb
from    pudb.remote         import set_trace
import  config
from    config              import settings
import  json
import  pypx
import  httpx

import  pathlib
import  sys
import  time
from    loguru              import logger
LOG             = logger.debug

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> │ "
    "<level>{level: <5}</level> │ "
    "<yellow>{name: >28}</yellow>::"
    "<cyan>{function: <30}</cyan> @"
    "<cyan>{line: <4}</cyan> ║ "
    "<level>{message}</level>"
)
logger.remove()
logger.opt(colors = True)
logger.add(sys.stderr, format=logger_format)
LOG     = logger.info


threadpool: ThreadPoolExecutor      = ThreadPoolExecutor()
processpool: ProcessPoolExecutor    = ProcessPoolExecutor()

def noop():
    """
    A dummy function that does nothing.
    """
    return {
        'status':   True
    }

async def relayAndEchoBack(
        payload             : relayModel.clientPayload,
        request             : Request
) -> dict:
    """
    Parse the incoming payload, expand to pflink needs,
    transmit, and return remote response.

    Args:
        payload (relayModel.clientPayload): the relay payload

    Returns:
        dict: the reponse from the remote server

    """
    timestamp = lambda : '%s' % datetime.now()
    pflinkPOST:relayModel.pflinkInput   = relayModel.pflinkInput()
    d_logEvent:dict      = {
        '_timestamp'        : timestamp(),
        'requestHost'       : request.client.host,
        'requestPort'       : str(request.client.port),
        'requestUserAgent'  : request.headers['user-agent'],
        'payload'           : payload
    }
    LOG(d_logEvent)

    pflinkPOST.PACSdirective    = payload.imageMeta
    pflinkPOST.FeedName                  = 'test'
    match payload.analyzeFunction:
        case 'dylld':
            pflinkPOST.analysisArgs.PluginName   = settings.dylld.analysisPluginName
            pflinkPOST.analysisArgs.Version      = settings.dylld.analysisPluginArgs
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
                settings.pflink.URL,
                data = pflinkPOST.json()
        )
        d_response  = response.json()
        LOG(d_response)
        return d_response

