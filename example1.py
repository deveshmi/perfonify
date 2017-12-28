import Fifo
from Fifo import *
import Pipe
from Pipe import *
import Arbiter
from Arbiter import *
import Requestor
from Requestor import *
import Request
from Request import *
import json

requestor_cfg_fname = 'requestorConfig.txt'

requestor_0 = Requestor(requestor_cfg_fname)
requestor_1 = Requestor(requestor_cfg_fname)
requestor_2 = Requestor(requestor_cfg_fname)
requestor_3 = Requestor(requestor_cfg_fname)

fifo_0 = Fifo(depth=8)
fifo_1 = Fifo(depth=8)
fifo_2 = Fifo(depth=8)
fifo_3 = Fifo(depth=8)

pipe_0 = Pipe(num_stages=8)
pipe_1 = Pipe(num_stages=4)
pipe_2 = Pipe(num_stages=2)
pipe_3 = Pipe(num_stages=12)

arb_0 = Arbiter(num_ports=4)

all_requestors_done = False
clk_cnt = 0

def inc_clk():
    requestor_0.inc_clk()
    requestor_1.inc_clk()
    requestor_2.inc_clk()
    requestor_3.inc_clk()
    
    fifo_0.inc_clk()
    fifo_1.inc_clk()
    fifo_2.inc_clk()
    fifo_3.inc_clk()
    
    pipe_0.inc_clk()
    pipe_1.inc_clk()
    pipe_2.inc_clk()
    pipe_3.inc_clk()
    
    arb_0.inc_clk()

i=0
#while (i < 4):
while not all_requestors_done:
    req_0 = requestor_0.get_request()
    req_1 = requestor_1.get_request()
    req_2 = requestor_2.get_request()
    req_3 = requestor_3.get_request()
    print req_0.valid

    if (fifo_0.push(req_0)):
        requestor_0.request_accepted()
    if (fifo_1.push(req_1)):
        requestor_1.request_accepted()
    if (fifo_2.push(req_2)):
        requestor_2.request_accepted()
    if (fifo_3.push(req_3)):
        requestor_3.request_accepted()

    fifo_0_out_req = fifo_0.read()
    fifo_1_out_req = fifo_1.read()
    fifo_2_out_req = fifo_2.read()
    fifo_3_out_req = fifo_3.read()
    print fifo_0_out_req.valid

    pipe_0.insert_req(fifo_0_out_req)
    pipe_1.insert_req(fifo_1_out_req)
    pipe_2.insert_req(fifo_2_out_req)
    pipe_3.insert_req(fifo_3_out_req)

    pipe_0_out = pipe_0.output()
    pipe_1_out = pipe_1.output()
    pipe_2_out = pipe_2.output()
    pipe_3_out = pipe_3.output()
    print pipe_0_out.valid

    arb_reqs = [pipe_0_out, pipe_1_out, pipe_2_out, pipe_3_out]
    arb_in = [arb_reqs[0].valid, arb_reqs[1].valid, arb_reqs[2].valid, arb_reqs[3].valid]
    print "devesh"

    print arb_in
    arb_out = arb_0.arbitrate(arb_in)
    print arb_out
    
    if (arb_out[0]):
        fifo_0.pop()
    if (arb_out[1]):
        fifo_1.pop()
    if (arb_out[2]):
        fifo_2.pop()
    if (arb_out[3]):
        fifo_3.pop()

    if arb_in[0] and not (arb_out[0]):
        pipe_0.stallPipe()
    if arb_in[1] and not (arb_out[1]):
        pipe_1.stallPipe()
    if arb_in[2] and not (arb_out[2]):
        pipe_2.stallPipe()
    if arb_in[3] and not (arb_out[3]):
        pipe_3.stallPipe()

    inc_clk()
    pipe_0.printPipe()
    requestor_0.printStats()
    requestor_1.printStats()
    requestor_2.printStats()
    requestor_3.printStats()
    i+=1
    all_requestors_done = requestor_0.is_requestor_done() and  \
                        requestor_1.is_requestor_done() and \
                        requestor_2.is_requestor_done() and \
                        requestor_3.is_requestor_done()
    raw_input("press enter key")


