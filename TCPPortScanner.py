from threading import Thread,Lock
from queue import Queue
import socket
from optparse import OptionParser

print_lock=Lock()

class tcpscan(Thread):
	def __init__(self,work_queue,address):
		super().__init__()
		self.work_queue=work_queue
		self.address=address
	def run(self):
		port=self.work_queue.get()
		scan.TCPscan(self.address,port)
		self.work_queue.task_done()

def main():
	p=OptionParser(usage="%Program -t|--target [target] -s|--start [start_port] -e|--end [end_port]")
	p.add_option('-t','--target',action='store',type='string',dest='target',help='target')
	p.add_option('-s','--start',action='store',type='int',dest='sp',help='start port scanning from this')
	p.add_option('-e','--end',action='store',type='int',dest='ep',help='port scanning until here')
	options,args=p.parse_args()
	if(options.target==None or options.sp==None or options.ep==None):
		p.error("ERROR")
	sp=options.sp
	ep=options.ep
	target=options.target
	lenght=ep-sp
	if(lenght <=0 or sp<1 or ep <2 or target.isdigit() or target.startswith('http')):
		p.error('bad input')
	q=Queue(lenght)
	for i in range(sp,ep):
		q.put(i)
	for i in range(10):
		obj=tcpscan(q,target)
		obj.daemon=True
		obj.start()
	q.join()


class scan():
	@staticmethod
	def TCPscan(host,p):
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(10)
		try:
			con=s.connect((host,p))
			with print_lock:
				print('{} is open!'.format(p))
			con.close() 
			s.close()
		except:
			pass

if __name__=='__main__':
	main()
print('DONE...')	

