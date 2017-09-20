import os
from keywords import _RunOnFailureKeywords
from BGLogLibrary.keywords import keywordgroup

from utils import LibraryListener

from keywords._ClientLog import _ClientLog
from keywords._ServerManager import _ServerManager
from keywords._logging import _LoggingKeywords
from keywords._OsspLog import _OsspDetailLogHelper
from BGLogLibrary.keywords.clientlib import ClientLogCatcherThread
from BGLogLibrary.keywords.clientlib import iFlyClientLogBase
from BGLogLibrary.keywords.clientlib.IFlyLogParser import RequestLogParser,ResponseLogParser
from BGLogLibrary.keywords.clientlib import IFlyLogTagsObserver

from version import VERSION

__version__ = VERSION

class BGLogLibrary(
    _LoggingKeywords,
    _RunOnFailureKeywords,
    _ClientLog,
    _OsspDetailLogHelper,
    _ServerManager,
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self,run_on_failure='Capture Page Screenshot',
    ):
    
        for base in BGLogLibrary.__bases__:
            base.__init__(self)
        self.register_keyword_to_run_on_failure(run_on_failure)
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        
        