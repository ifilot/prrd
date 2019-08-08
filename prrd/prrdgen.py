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
import json
import os.path
from datetime import datetime
from pprint import pprint

##
## @brief      Class for rrd graph.
##
##
## Usage note: remember to use \\n for newlines, see:
## https://github.com/oetiker/rrdtool-1.x/issues/23
##
class prrdbase:

	def __init__(self, filename):
		"""
		@brief      Constructs the object.
		
		@param      self      The object
		@param      filename  path to settings json file
		"""
		self.base_path = '/var/lib/collectd/rrd/'
		self.hostname = socket.getfqdn()
		self.hostnamelabel = self.hostname + ' - ' + self.get_os_name()
		self.defaultfont = 'DEFAULT:8'

		# load json file
		if filename:
			with open(filename, 'r') as f:
				data = json.load(f)

		self.width = data['settings']['width']
		self.height = data['settings']['height']

	def get_os_name(self):
		with open("/etc/os-release") as f:
			d = {}
			for line in f:
				k,v = line.rstrip().split("=")
				d[k] = v
			return d['PRETTY_NAME'].strip('"')

	def create_graph(self, type, time, imgfile):
		"""
		@brief      Creates a graph.
		
		@param      self     The object
		@param      type     type of the graph
		@param      time     The time
		@param      imgfile  url to image file
		
		@return     void
		"""
		if type == 'load':
			self.graph_load(time, imgfile)
		if type == 'cpu':
			self.graph_cpu(time, imgfile)
		if type == 'memory':
			self.graph_memory(time, imgfile)
		if type == 'temperature':
			self.graph_temperature(time, imgfile)
		if type == 'diskspace':
			self.graph_df_root(time, imgfile)

	def get_time(self):
		dtobj = datetime.now()
		return dtobj.strftime("%Y-%m-%d %H:%M:%S")

	def graph_load(self, time, imgfile):
		"""
		@brief      generate load graph
		
		@param      self     The object
		@param      time     number of seconds in the past
		@param      imgfile  url to image file
		
		@return     void
		"""
		path = self.base_path + self.hostname + "/load/load.rrd"
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', "end - " + str(time),
			'--end', "now",
			'--font',self.defaultfont,
			'--title', self.hostnamelabel + "\\nLoad averages @ " + self.get_time(),
			'DEF:st=' + path + ':shortterm:AVERAGE',
			'DEF:stmaxl=' + path + ':shortterm:MAX',
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
			'AREA:stmaxl#AAFFAA',
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

	def graph_cpu(self, time, imgfile):
		"""
		@brief      generate cpu usage graph
		
		@param      self  The object
		@param      time  number of seconds in the past
		@param      imgfile  url to image file
		
		@return     void
		"""
		pathb = self.base_path + self.hostname + "/cpu-0"
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'-c', 'ARROW#000000',
			'-Y',
			'-u', '100',
			'-r',
			'-l', '0',
			'-L', '5',
			'-v', 'Jiffies [-]',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', "end - " + str(time),
			'--end', "now",
			'--title', self.hostnamelabel + "\\nCPU Utilization @ " + self.get_time(),
			'--font',self.defaultfont,
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

	def graph_gpu_temperature(self, time, imgfile, gpu_id):
		"""
		Output GPU temperature

		time		Number of seconds to plot
	 	imgfile 	Filename
		gpu_id		ID of the GPU
		"""
		pathb = self.base_path + self.hostname + '/cuda-00000000:%02i:00.0/temperature-temperature_gpu.rrd' % gpu_id
		rpi = True
		if not os.path.isfile(pathb):
			return

		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'--title', self.hostnamelabel + "\\nGPU Temperature @ " + self.get_time(),
			'--font',self.defaultfont,
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-l', '30',
			'-u', '80' if rpi else '120',
			'-v Temperature',
			'DEF:min=' + pathb.replace(':','\:') + ':value:MIN',
			'DEF:avg=' + pathb.replace(':','\:') + ':value:AVERAGE',
			'DEF:max=' + pathb.replace(':','\:') + ':value:MAX',
			'CDEF:ds_red=max,70,GT,max,UNKN,IF',
			'CDEF:ds_orange=max,50,GT,max,70,GT,70,max,IF,UNKN,IF',
			'CDEF:ds_green=max,50,GT,50,max,IF',
			'AREA:ds_red#FF4444',
			'LINE1:ds_red#FF0000',
			'AREA:ds_orange#FFD044',
			'LINE1:ds_orange#FFB000',
			'AREA:ds_green#CCFFCC',
			'LINE1:ds_green#00FF00',
			'GPRINT:avg:AVERAGE:Temperature   %5.1lf Avg,',
			'GPRINT:avg:MIN:%5.1lf Min,',
			'GPRINT:avg:MAX:%5.1lf Max',
			'GPRINT:avg:LAST:%5.1lf Last')

	def graph_memory(self, time, imgfile):
		"""
		@brief      generate memory usage graph
		
		@param      self  The object
		@param      time  number of seconds in the past
		@param      imgfile  url to image file
		
		@return     void
		"""
		pathb = self.base_path + self.hostname + "/memory"
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-l', '0',
			'-L', '5',
			'-v', 'Memory [bytes]',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'--title', self.hostnamelabel + "\\nMemory @ " + self.get_time(),
			'--font',self.defaultfont,
			'DEF:mem_buf=' + pathb + '/memory-buffered.rrd' + ':value:AVERAGE',
			'DEF:mem_cached=' + pathb + '/memory-cached.rrd' + ':value:AVERAGE',
			'DEF:mem_free=' + pathb + '/memory-free.rrd' + ':value:AVERAGE',
			'DEF:mem_used=' + pathb + '/memory-used.rrd' + ':value:AVERAGE',
			'CDEF:mem_buf_add=mem_buf,UN,0,mem_buf,IF,mem_used,+',
			'CDEF:mem_cached_add=mem_cached,UN,0,mem_cached,IF,mem_buf_add,+',
			'CDEF:mem_free_add=mem_free,UN,0,mem_free,IF,mem_cached_add,+',
			'TEXTALIGN:left',
			'AREA:mem_free_add#CCFFCC',
			'AREA:mem_cached_add#CCCCFF',
			'AREA:mem_buf_add#f3dfb7',
			'AREA:mem_used#FFCCCC',
			'LINE1:mem_free_add#00FF00:Free',
			'GPRINT:mem_free:AVERAGE:        %5.1lf%s Avg,',
			'GPRINT:mem_free:MIN:%5.1lf%s Min,',
			'GPRINT:mem_free:MAX:%5.1lf%s Max,',
			"GPRINT:mem_free:LAST:%5.1lf%s Last\\n",
			'LINE1:mem_cached_add#0000FF:Page cache',
			'GPRINT:mem_cached:AVERAGE:  %5.1lf%s Avg,',
			'GPRINT:mem_cached:MIN:%5.1lf%s Min,',
			'GPRINT:mem_cached:MAX:%5.1lf%s Max,',
			'GPRINT:mem_cached:LAST:%5.1lf%s Last',
			'LINE1:mem_buf_add#f0a000:Buffer cache',
			'GPRINT:mem_buf:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:mem_buf:MIN:%5.1lf%s Min,',
			'GPRINT:mem_buf:MAX:%5.1lf%s Max,',
			"GPRINT:mem_buf:LAST:%5.1lf%s Last\\n",
			'LINE1:mem_used#FF0000:Used',
			'GPRINT:mem_used:AVERAGE:        %5.1lf%s Avg,',
			'GPRINT:mem_used:MIN:%5.1lf%s Min,',
			'GPRINT:mem_used:MAX:%5.1lf%s Max,',
			"GPRINT:mem_used:LAST:%5.1lf%s Last\\n")

	def graph_internet(self, time, imgfile, interface):
		"""
		@brief      generate memory usage graph
		
		@param      self  The object
		@param      time  number of seconds in the past
		@param      imgfile  url to image file
		
		@return     void
		"""
		pathb = self.base_path + self.hostname + "/interface-" + interface + "/if_octets.rrd"
		if not os.path.isfile(pathb):
			return
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-v Bytes/s',
			'--title', self.hostnamelabel + "\\n" + interface + ' interface @' + self.get_time(),
			'--font',self.defaultfont,
			'DEF:rx_max=' + pathb + ':rx:MAX',
			'DEF:rx_avg=' + pathb + ':rx:AVERAGE',
			'DEF:tx_max=' + pathb + ':tx:MAX',
			'DEF:tx_avg=' + pathb + ':tx:AVERAGE',
			'CDEF:tx_avg_m=0,tx_avg,-',
			'CDEF:tx_max_m=0,tx_max,-',
			'VDEF:rx_total=rx_avg,TOTAL',
			'VDEF:tx_total=tx_avg,TOTAL',
			'AREA:rx_avg#CCFFCC',
			'AREA:tx_avg_m#CCCCFF',
			'TEXTALIGN:left',
			'LINE1:rx_avg#00FF00:Incoming',
			'GPRINT:rx_avg:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:rx_avg:MAX:%5.1lf%s Max,',
			'GPRINT:rx_avg:LAST:%5.1lf%s Last',
			'GPRINT:rx_total:(ca. %5.1lf%s Total)',
			'LINE1:tx_avg_m#0000FF:Outgoing',
			'GPRINT:tx_avg:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:tx_avg:MAX:%5.1lf%s Max,',
			'GPRINT:tx_avg:LAST:%5.1lf%s Last',
			'GPRINT:tx_total:(ca. %5.1lf%s Total)')

	def graph_ping(self, time, imgfile, website):
		"""
		@brief      generate memory usage graph
		
		@param      self  The object
		@param      time  number of seconds in the past
		@param      imgfile  url to image file
		
		@return     void
		"""
		pathb = self.base_path + self.hostname + "/ping/ping-" + website + ".rrd"
		if not os.path.isfile(pathb):
			return
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-v ms',
			'-l 0',
			'--title', "Ping " + website + ' / ' + self.get_time(),
			'--font',self.defaultfont,
			'DEF:avg=' + pathb + ':value:AVERAGE',
			'LINE1:avg#00FF00:Incoming',
			'GPRINT:avg:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:avg:MIN:%5.1lf%s Min,',
			'GPRINT:avg:MAX:%5.1lf%s Max',
			'GPRINT:avg:LAST:%5.1lf%s Last')

	def graph_temperature(self, time, imgfile):
		# temperature sensors on Raspberry Pi
		pathb = self.base_path + self.hostname + '/curl-CpuTemp/temperature-CPUTemp_switchpi.rrd'
		rpi = True
		if not os.path.isfile(pathb):
			# temperature sensors on mac mini
			pathb = self.base_path + self.hostname + '/sensors-coretemp-isa-0000/temperature-temp2.rrd'
			rpi = False
			if not os.path.isfile(pathb):
				return
		
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'--title', self.hostnamelabel + "\\nCPU Temperature @ " + self.get_time(),
			'--font',self.defaultfont,
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-l', '30',
			'-u', '80' if rpi else '120',
			'-v Temperature',
			'DEF:min=' + pathb + ':value:MIN',
			'DEF:avg=' + pathb + ':value:AVERAGE',
			'DEF:max=' + pathb + ':value:MAX',
			'CDEF:minc=min,1000,/' if rpi else 'CDEF:minc=min',
			'CDEF:avgc=avg,1000,/' if rpi else 'CDEF:avgc=avg',
			'CDEF:maxc=max,1000,/' if rpi else 'CDEF:maxc=max',
			'CDEF:ds_red=maxc,70,GT,maxc,UNKN,IF',
			'CDEF:ds_orange=maxc,50,GT,maxc,70,GT,70,maxc,IF,UNKN,IF',
			'CDEF:ds_green=maxc,50,GT,50,maxc,IF',
			'AREA:ds_red#FF4444',
			'LINE1:ds_red#FF0000',
			'AREA:ds_orange#FFD044',
			'LINE1:ds_orange#FFB000',
			'AREA:ds_green#CCFFCC',
			'LINE1:ds_green#00FF00')

	def graph_df_root(self, time, imgfile):
		pathb = self.base_path + self.hostname + '/df-root'
		rrdtool.graph(imgfile,
			'--imgformat', 'PNG',
			'--width', str(self.width),
			'--height', str(self.height),
			'--start', 'end - ' + str(time),
			'--end', 'now',
			'--title', self.hostnamelabel + "\\nDisk Space (root) @ " + self.get_time(),
			'--font',self.defaultfont,
			'-c', 'ARROW#000000',
			'-Y',
			'-r',
			'-l', '0',
			'-L', '5',
			'-v', 'Space',
			'DEF:free=' + pathb + '/df_complex-free.rrd:value:AVERAGE',
			'DEF:reserved=' + pathb + '/df_complex-reserved.rrd:value:AVERAGE',
			'DEF:used=' + pathb + '/df_complex-used.rrd:value:AVERAGE',
			'CDEF:cdef-used=used,UN,0,used,IF',
			'CDEF:cdef-reserved=reserved,UN,0,reserved,IF,cdef-used,+',
			'CDEF:cdef-free=free,UN,0,free,IF,cdef-reserved,+',
			'AREA:cdef-free#bff7bf',
			'AREA:cdef-reserved#bfbfff',
			'AREA:cdef-used#FFCCCC',
			'LINE1:cdef-free#00FF00:Free',
			'GPRINT:free:AVERAGE:    %5.1lf%s Avg,',
			'GPRINT:free:MIN:%5.1lf%s Min,',
			'GPRINT:free:MAX:%5.1lf%s Max,',
			"GPRINT:free:LAST:%5.1lf%s Last\\n",
			'LINE1:cdef-reserved#0000FF:Reserved',
			'GPRINT:reserved:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:reserved:MIN:%5.1lf%s Min,',
			'GPRINT:reserved:MAX:%5.1lf%s Max,',
			"GPRINT:reserved:LAST:%5.1lf%s Last\\n",
			'LINE1:cdef-used#FF0000:Used    ',
			'GPRINT:used:AVERAGE:%5.1lf%s Avg,',
			'GPRINT:used:MIN:%5.1lf%s Min,',
			'GPRINT:used:MAX:%5.1lf%s Max,',
			"GPRINT:used:LAST:%5.1lf%s Last\\n")
