import simplejson as json
import Request
from Request import *

# Trace File is a JSON dump of transaction_data and requestor attributes
# Trace file example
# 
# {
#   req_rate : 0.5,
#   req_burst_type : random/deterministic,
#   req_burst_size : 4,
#   trace :[req1, req2, req3, ... , reqN]
# }
#   
#

class Requestor:
    def __init__(self, requestor_cfg_fname):
        with open(requestor_cfg_fname) as fh:
            self.requestorCfgDict = json.load(fh)
        self.req_rate = self.requestorCfgDict['req_rate']
        self.req_burst_type = self.requestorCfgDict['req_burst_type']
        self.req_burst_size = self.requestorCfgDict['req_burst_size']
        traceFN = self.requestorCfgDict['trace_file']
        with open(traceFN) as fh:
            self.trace = fh.readlines()
        self.xaction_id = 0
        self.requestor_done = False
        self.request = Request()
        self.clk_cnt = 0.0

    def get_request(self):
        if not (self.requestor_done):
            self.request.valid = True 
            self.request.data = self.trace[self.xaction_id]
            return (self.request)
        return (False)
    
    def request_accepted(self):
        # Return True if requestor has more transactions to send
        # Return False when requestor is done
        self.xaction_id += 1
        if (self.xaction_id < len(self.trace)):
            return True
        self.requestor_done = True
        return False

    def is_requestor_done(self):
        # Return True if requestor has more transactions to send
        # Return False when requestor is done
        return (self.requestor_done)

    def printStats(self):
        st = ''
        st = st + 'rate = ' + str(self.xaction_id/self.clk_cnt) + ' num_xactions = ' + str(self.xaction_id) + ' num_clks = ' + str(self.clk_cnt)
        print st

    def inc_clk(self):
        self.clk_cnt+=1
