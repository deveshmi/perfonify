import random

# replacement policies = FIFO, LRU, RR
class Cache:
    def __init__(self, num_sets, num_ways, miss_q_depth=8, replacement = 'FIFO'):
        self.clk_cnt = 0
        self.num_sets= num_sets
        self.num_ways = num_ways
        self.replacement = replacement
        self.tags = [[]]
        for set_index in xrange(num_sets):
            self.tags.append([])
            for way in xrange(num_ways):
                self.tags[set_index].append([])
                self.tags[set_index][way] = -1
        self.miss_q = []
        for i in xrange(self.miss_q_depth):
            self.miss_q.append(-1)

    def compute_set_index(self, addr):
        set_index = addr % self.num_sets
        return set_index

    def compute_tag(self, addr):
        tag = addr / self.num_sets
        return tag

    def lookup(self, addr):
        set_index = self.compute_set_index(addr)
        tag = self.compute_tag(addr)
        if (tag in self.tags[set_index]):
            hit = True
            if (self.replacement == 'LRU'):
                hit_way = self.tags[set_index].index(tag)
                self.tags[set_index].pop(hit_way)
                self.tags[set_index].insert(self.num_ways-1, tag)
        else:
            hit = False
        return hit

    def compute_fill_latency(self):
        return (random.randint(self.min_fill_latency, self.max_fill_latency))

    def update(self, addr):
        print ("fill returned for addr {}...updating tags".format(addr))
        set_index = self.compute_set_index(addr)
        tag = self.compute_tag(addr)
        if (self.replacement == 'FIFO'):
            self.tags[set_index][1:] = self.tags[set_index][:-1]
            self.tags[set_index][0] = tag
        if (self.replacement == 'LRU'):
            self.tags[set_index][0] = tag
        print (self.tags[set_index])
            

    def launch_fill_req(self, addr):
        latency = self.compute_fill_latency()
        enq_time = (self.clk_cnt + latency) % len(self.timeline)
        event = {}
        event['function'] = self.update
        event['args'] = addr
        self.timeline[enq_time].append(event)
        print "current time : {}, enq'd fill event at time {}".format(self.clk_cnt, self.clk_cnt + latency)

    def deq_timeline(self):
        deq_time = self.clk_cnt % len(self.timeline)
        for event in self.timeline[deq_time]:
            event['function'](event['args'])
        self.timeline[deq_time] = []

    def inc_clk(self):
        self.deq_timeline()
        self.clk_cnt += 1

    def is_hum(self):
        if (addr in self.miss_q):
            return (True)
        else:
            return (False)

    def run_trace(self, trace):
        i=0
        xaction_done = True
        addr = trace[i]
        if (self.lookup(int(addr, 16))):
            print 'xaction_id : {}, addr : {} ---> hit!'.format(i, addr)
        else:
            print 'xaction_id : {}, addr : {} ---> miss!'.format(i, addr)
            if not (self.is_hum(int(addr, 16))):
                if not self.launch_fill_req(int(addr, 16)):
                    xaction_done = False
