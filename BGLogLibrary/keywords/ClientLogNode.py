from collections import namedtuple

ClientLogNode = namedtuple('CLNode', 
					['pc_time', 'client_time','tag','msg'])


if __name__ == '__main__':
	cNode = ClientLogNode("123",'456','7','8')
	print cNode
