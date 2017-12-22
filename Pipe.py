import Request
from Request import *

class Pipe:
    def __init__(self, num_stages=4, stall_scheme='FREEZE'):
        self.pipe_stage = []
        self.num_stages = num_stages
        self.stall_scheme = stall_scheme # SKID or FREEZE
        self.stall = False
        self.insert = Request()
        self.insert_pend = False
        for i in xrange(self.num_stages):
            self.pipe_stage.append(Request())

    def insert_req(self, request):
        self.insert = request
        self.insert_pend = True

    def output(self):
        return self.pipe_stage[self.num_stages-1]

    def stallPipe(self):
        self.stall = True

    def printPipe(self):
        st = ''
        for i in xrange(self.num_stages):
            st = st + ' ' + str(self.pipe_stage[i].valid)
        print st

    def advance(self):
        i=self.num_stages-1
        while (i > 0):
            self.pipe_stage[i] = self.pipe_stage[i-1]
            i-=1
        if (self.insert_pend):
            self.pipe_stage[0] = self.insert

    def inc_clk_skid(self):
        if (self.stall): # collapse bubbles
            i = 0
            while (i < (self.num_stages - 1)):
                this_stage_vld = self.pipe_stage[i].valid
                next_stage_vld = self.pipe_stage[i+1].valid
                if this_stage_vld and not next_stage_vld:
                    self.pipe_stage[0].valid = False
                    for n in xrange(i):
                        self.pipe_stage[n+1] = self.pipe_stage[n]
        else:
            self.advance()
        self.stall = False
        self.insert_pend = False
    
    def inc_clk_freeze(self):
        if (self.stall): # collapse bubbles
            #nop
            pass
        else: 
            self.advance()
        self.stall = False
        self.insert_pend = False


    def inc_clk (self):
        if (self.stall_scheme=='SKID'):
            self.inc_clk_skid()
        else:
            self.inc_clk_freeze()
