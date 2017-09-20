from collections import namedtuple

ClientLogNode = namedtuple('CLNode', 
					['tag','pc_time', 'client_time','msg'])
class ClientLogNode:

    def __init__(self, tag,pc_time,client_time,msg):
        self.tag = tag
        self.pc_time = pc_time
        self.client_time = client_time
        self.msg = msg

if __name__ == '__main__':
	cNode = ClientLogNode("123",'456','7','8')
	print cNode
