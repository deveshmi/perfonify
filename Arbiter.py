import Request
from Request import *

class Arbiter:
    def __init__(self, num_ports=4, scheme='RR'):
        self.num_ports = num_ports
        self.request = []
        self.last_grant = []
        self.grant = []
        self.scheme = scheme
        for i in xrange(self.num_ports):
            self.request.append(Request())
            self.grant.append(False)
            self.last_grant.append(i)

    def arbitrate(self, request=[]):
        self.request = request
        winner_id = 0
        flag=False
        for i in xrange(self.num_ports):
            if (self.request[i]):
                flag=True
        if (flag):
            if (self.scheme == 'RR'):
                last_grant = self.last_grant[0]
                if (last_grant == self.num_ports-1):
                    check_port_id = 0
                else:
                    check_port_id = last_grant+1
                for i in xrange(self.num_ports):
                    if (self.request[check_port_id]):
                        winner_id = check_port_id
                        break
                    check_port_id += 1
                    if (check_port_id >= self.num_ports):
                        check_port_id = 0
                self.last_grant[0] = winner_id
                for i in xrange(self.num_ports):
                    if (i == winner_id):
                        self.grant[i] = True
                    else:
                        self.grant[i] = False
                return (self.grant)
            if (self.scheme == 'LRU'):
                for check_port_id in self.last_grant:
                    if (self.request[check_port_id]):
                        winner_id = check_port_id
                        break
                del self.last_grant[winner_id]
                self.last_grant.append(winner_id)
                for i in xrange(self.num_ports):
                    if (i == winner_id):
                        self.grant[i] = True
                    else:
                        self.grant[i] = False
                return (self.grant)
        else:
            for i in xrange(self.num_ports):
                self.grant[i] = False
            return (self.grant)

    def inc_clk(self):
        pass
