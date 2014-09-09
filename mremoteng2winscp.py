#!/usr/bin/env python2.7

# The MIT License (MIT)

# Copyright (c) 2014 Elie Deloumeau, Network Informatique

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import xml.etree.ElementTree as ET
import ConfigParser

mremoteng_configfile = 'C:\Users\Administrator\AppData\Roaming\mRemoteNG\confCons.xml'
print '\tReading mRemoteNG config file (' + mremoteng_configfile + ')'
tree = ET.parse(mremoteng_configfile)

winscp_configfile = 'C:\Users\Administrator\Documents\WinSCP.ini'
print '\tReading WinSCP config file (' + winscp_configfile + ')\n'
winscp = ConfigParser.RawConfigParser()
winscp.read(winscp_configfile)

persistent_name = 'persistent_name'
name = ''
jumplist = winscp.get('Configuration', 'JumpList')

for c in tree.findall('.//Node'):
    ctype = c.get('Type')
    cproto = c.get('Protocol')
    if persistent_name != name and ctype == 'Container':
        persistent_name = c.get('Name')
        jumplist += '\"' + persistent_name + '/' + persistent_name + '\",'
    if ctype == 'Connection' and cproto == 'SSH2':
        name = c.get('Name')
        hostname = c.get('Hostname')
        username = c.get('Username')
        port = c.get('Port')

        if persistent_name != '':
            title = 'Sessions\\' + persistent_name + '/' + name
            jumplist_str = ',\"' + persistent_name + '/' + name + '\"'
        else:
            title = 'Sessions\\' + name
            jumplist_str = ',\"' + name + '\"'

        title = title.replace(' ', '%20')

        try:
            winscp.get(title, 'HostName')
        except:
            print '\tProcessing ' + name
            jumplist += jumplist_str
            winscp.add_section(title)
            winscp.set(title, 'HostName', hostname)
            if port != '22':
                winscp.set(title, 'PortNumber', port)
            winscp.set(title, 'UserName', username)

winscp.set('Configuration', 'JumpList', jumplist.replace(' ', '%20'))

with open(winscp_configfile, 'wb') as configfile:
    print '\n\tWriting WinSCP config file (' + winscp_configfile + ')'
    winscp.write(configfile)

print '\n\tDone.\r'
t = input('Type enter to exit...')