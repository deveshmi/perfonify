import Request
from Request import *

class Fifo:
    def __init__(self, depth=8):
        self.occupancy = 0
        self.depth = depth
        self.storage = []
        for i in xrange(self.depth):
            self.storage.append(Request())

        self.stats = []
        self.push_pend_request = Request()
        self.push_pend = False
        self.pop_pend = False
    
    def push(self, request):
        if (self.occupancy < self.depth):
            self.push_pend_request = request
            self.push_pend = True
            return (True)
        else:
            return (False)

    def read(self):
        if (self.occupancy > 0):
            rd_data = self.storage[self.occupancy-1]
            return (rd_data)
        else:
            return (Request())

    def pop(self):
        if (self.occupancy > 0):
            self.pop_pend = True
            return (True)
        else:
            return (False)

    def inc_clk(self):
        if (self.push_pend):
            self.storage[self.occupancy] = self.push_pend_request
            if not (self.pop_pend):
                self.occupancy += 1
        if (self.pop_pend):
            self.occupancy -= 1
        self.push_pend = False
        self.pop_pend = False
