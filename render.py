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

from prrd import prrdgen

#
# GRAPH TYPES
#
# load - load average
# cpu  - cpu usage (idle, user, etc.)
#

# construct object
p = prrdgen.prrdbase('settings.json')

# generate load graphs
p.create_graph('load', 86400, 'load_day.png')
p.create_graph('load', 86400 * 7, 'load_week.png')

# generate cpu usage graphs
p.create_graph('cpu', 86400, 'cpu_day.png')
p.create_graph('cpu', 86400 * 7, 'cpu_week.png')

# generate memory usage
p.create_graph('memory', 86400, 'memory_day.png')
p.create_graph('memory', 86400 * 7, 'memory_week.png')

# generate internet usage graphs
interfaces = ['eno1', 'eth0', 'wlan0', 'enp4s0f0', 'enp0s25', 'enp10s0', 'wlx74da387f8eed', 'enxb827eb10dc2b']
for interface in interfaces:
	p.graph_internet(86400, interface + '_day.png', interface)
	p.graph_internet(86400 * 7, interface + '_week.png', interface)

# generate GPU data
for i in range(0,10):
	p.graph_gpu_temperature(86400, 'temperature_gpu_%02i.png' % i, i)
	p.graph_gpu_power(86400, 'power_gpu_%02i.png' % i, i)
	p.graph_gpu_utilization(86400, 'utilization_gpu_%02i.png' % i, i)
	p.graph_gpu_fan(86400, 'fan_gpu_%02i.png' % i, i)

# generate temperature graphs
p.create_graph('temperature', 86400 * 7, 'temperature_week.png')

# generate disk space for 100 days
p.create_graph('diskspace', 86400 * 100, 'disk_root_100days.png')

# generate disk space for other partitions
partitions = ['storage-disk1']
for partition in partitions:
	p.graph_df(86400 * 100, 'disk_%s_100days.png' % partition, partition)
