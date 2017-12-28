import Cache
from Cache import *
import Requestor
from Requestor import *

requestor_cfg_fname = 'requestorConfig.txt'
requestor_0 = Requestor(requestor_cfg_fname)
cache = Cache(1, 64)

cache.run_trace(requestor_0.trace)
