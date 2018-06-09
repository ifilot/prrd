 ##################################################################################
 # The MIT License (MIT)
 # Copyright (c) 2018 ifilot
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 # IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 # DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 # OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
 # OR OTHER DEALINGS IN THE SOFTWARE
 # 
 ##################################################################################

import sys
import socket 		# hostname
import rrdtool

##
## @brief      Class for rrd graph.
##
##
## Usage note: remember to use \\n for newlines, see:
## https://github.com/oetiker/rrdtool-1.x/issues/23
## 
class prrdbase:
	def __init__(self):
		"""
		{ item_description }
		"""
		self.base_path = '/var/lib/collectd/rrd/'
		self.hostname = socket.gethostname()

	def create_graph(self, type):
		if type == 'load':
			self.graph_load()
		if type == 'cpu':
			self.graph_cpu()

	def graph_load(self):
		path = self.base_path + self.hostname + "/load/load.rrd"
		img = 'load.png'
		rrdtool.graph(img,
			'--imgformat', 'PNG',
			'--width', '540',
			'--height', '100',
			'--start', "end - 86400",
			'--end', "now",
			'--title', 'Running average CPU loads',
			'DEF:st=' + path + ':shortterm:AVERAGE',
			'DEF:mt=' + path + ':midterm:AVERAGE',
			'DEF:lt=' + path + ':longterm:AVERAGE',
			'VDEF:stlast=st,LAST',
			'VDEF:stmin=st,MINIMUM',
			'VDEF:stmax=st,MAXIMUM',
			'VDEF:stavg=st,AVERAGE',
			'VDEF:mtlast=mt,LAST',
			'VDEF:mtmin=mt,MINIMUM',
			'VDEF:mtmax=mt,MAXIMUM',
			'VDEF:mtavg=mt,AVERAGE',
			'VDEF:ltlast=lt,LAST',
			'VDEF:ltmin=lt,MINIMUM',
			'VDEF:ltmax=lt,MAXIMUM',
			'VDEF:ltavg=lt,AVERAGE',
			"COMMENT:            Now      Min     Max     Avg\\n",
			'LINE1:st#FF0000:1 min ',
			'GPRINT:stlast:%6.2lf',
			'GPRINT:stmin:%6.2lf',
			'GPRINT:stmax:%6.2lf',
			"GPRINT:stavg:%6.2lf\\n",
			'LINE1:mt#00FF00:5 min ',
			'GPRINT:mtlast:%6.2lf',
			'GPRINT:mtmin:%6.2lf',
			'GPRINT:mtmax:%6.2lf',
			"GPRINT:mtavg:%6.2lf\\n",
			'LINE1:lt#0000FF:15 min',
			'GPRINT:ltlast:%6.2lf',
			'GPRINT:ltmin:%6.2lf',
			'GPRINT:ltmax:%6.2lf',
			'GPRINT:ltavg:%6.2lf\\n')

	def graph_cpu(self):
		pathb = self.base_path + self.hostname + "/cpu-0"
		img = 'cpu.png'
		rrdtool.graph(img,
			'--imgformat', 'PNG',
			'-c', 'ARROW#000000',
			'-Y',
			'-u', '100',
			'-r',
			'-l', '0',
			'-L', '5',
			'-v', 'jiffies',
			'--width', '450',
			'--height', '75',
			'--start', "end - 86400",
			'--end', "now",
			'--title', 'CPU utilization::' + self.hostname,
			'DEF:idle=' + pathb + '/cpu-idle.rrd:value:AVERAGE',
			'DEF:nice=' + pathb + '/cpu-nice.rrd:value:AVERAGE',
			'DEF:user=' + pathb + '/cpu-user.rrd:value:AVERAGE',
			'DEF:wait=' + pathb + '/cpu-wait.rrd:value:AVERAGE',
			'DEF:system=' + pathb + '/cpu-system.rrd:value:AVERAGE',
			'DEF:softirq=' + pathb + '/cpu-softirq.rrd:value:AVERAGE',
			'DEF:interrupt=' + pathb + '/cpu-interrupt.rrd:value:AVERAGE',
			'DEF:steal=' + pathb + '/cpu-steal.rrd:value:AVERAGE',
			'CDEF:cdef-steal=steal,UN,0,steal,IF',
			'CDEF:cdef-interrupt=interrupt,UN,0,interrupt,IF,cdef-steal,+',
			'CDEF:cdef-softirq=softirq,UN,0,softirq,IF,cdef-interrupt,+',
			'CDEF:cdef-system=system,UN,0,system,IF,cdef-softirq,+',
			'CDEF:cdef-wait=wait,UN,0,wait,IF,cdef-system,+',
			'CDEF:cdef-user=user,UN,0,user,IF,cdef-wait,+',
			'CDEF:cdef-nice=nice,UN,0,nice,IF,cdef-user,+',
			'CDEF:cdef-idle=idle,UN,0,idle,IF,cdef-nice,+',
			'AREA:cdef-idle#f1f1f1',
			'AREA:cdef-nice#bff7bf',
			'AREA:cdef-user#bfbfff',
			'AREA:cdef-wait#ffebbf',
			'AREA:cdef-system#ffbfbf',
			'AREA:cdef-softirq#ffbfff',
			'AREA:cdef-interrupt#e7bfe7',
			'AREA:cdef-steal#bfbfbf',
			'LINE1:cdef-idle#c8c8c8:idle',
			'GPRINT:idle:AVERAGE:     %5.1lf Avg,',
			'GPRINT:idle:MIN:%5.1lf Min,',
			'GPRINT:idle:MAX:%5.1lf Max,',
			"GPRINT:idle:LAST:%5.1lf Last\\n",
			'LINE1:cdef-nice#00e000:nice',
			'GPRINT:nice:AVERAGE:     %5.1lf Avg,',
			'GPRINT:nice:MIN:%5.1lf Min,',
			'GPRINT:nice:MAX:%5.1lf Max,',
			"GPRINT:nice:LAST:%5.1lf Last\\n",
			'LINE1:cdef-user#0000ff:user',
			'GPRINT:user:AVERAGE:     %5.1lf Avg,',
			'GPRINT:user:MIN:%5.1lf Min,',
			'GPRINT:user:MAX:%5.1lf Max,',
			"GPRINT:user:LAST:%5.1lf Last\\n",
			'LINE1:cdef-wait#ffb000:wait',
			'GPRINT:wait:AVERAGE:     %5.1lf Avg,',
			'GPRINT:wait:MIN:%5.1lf Min,',
			'GPRINT:wait:MAX:%5.1lf Max,',
			"GPRINT:wait:LAST:%5.1lf Last\\n",
			'LINE1:cdef-system#ff0000:system',
			'GPRINT:system:AVERAGE:   %5.1lf Avg,',
			'GPRINT:system:MIN:%5.1lf Min,',
			'GPRINT:system:MAX:%5.1lf Max,',
			"GPRINT:system:LAST:%5.1lf Last\\n",
			'LINE1:cdef-softirq#ff00ff:softirq',
			'GPRINT:softirq:AVERAGE:  %5.1lf Avg,',
			'GPRINT:softirq:MIN:%5.1lf Min,',
			'GPRINT:softirq:MAX:%5.1lf Max,',
			"GPRINT:softirq:LAST:%5.1lf Last\\n",
			'LINE1:cdef-interrupt#a000a0:interrupt',
			'GPRINT:interrupt:AVERAGE:%5.1lf Avg,',
			'GPRINT:interrupt:MIN:%5.1lf Min,',
			'GPRINT:interrupt:MAX:%5.1lf Max,',
			"GPRINT:interrupt:LAST:%5.1lf Last\\n",
			'LINE1:cdef-steal#000000:steal',
			'GPRINT:steal:AVERAGE:    %5.1lf Avg,',
			'GPRINT:steal:MIN:%5.1lf Min,',
			'GPRINT:steal:MAX:%5.1lf Max,',
			"GPRINT:steal:LAST:%5.1lf Last\\n")