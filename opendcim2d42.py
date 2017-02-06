#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import pymysql as sql
import codecs
import requests
import base64 
import random
import json


# ========================================================================
# IMPORTANT !!!
# Devices that are not based on device template are not going to be migrated
# * TemplateID (openDCIM) == Hardware Model (Device42)
# Racks without height, are not going to be migrated
# ========================================================================



# ====== MySQL Source (openDCIM) ====== #
DB_IP     = ''
DB_PORT   = ''
DB_NAME   = ''
DB_USER   = ''
DB_PWD    = ''
# ====== Log settings  ==================== #
LOGFILE    = 'migration.log'
DEBUG      = True
# ====== Device42 upload settings ========= #
D42_USER   = ''
D42_PWD    = ''
D42_URL    = 'https://'
DRY_RUN    = False

class Logger():
    def __init__(self, logfile):
        self.logfile  = LOGFILE

    def writer(self, msg):  
        if LOGFILE and LOGFILE != '':
            with codecs.open(self.logfile, 'a', encoding = 'utf-8') as f:
                f.write(msg.strip()+'\r\n')  # \r\n for notepad
        try:
            print msg
        except:
            print msg.encode('ascii', 'ignore') + ' # < non-ASCII chars detected! >'


class REST():
    def __init__(self):
        self.password = D42_PWD
        self.username = D42_USER
        self.base_url = D42_URL
        
    def uploader(self, data, url):
        payload = data
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(self.username + ':' + self.password),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(url, data=payload, headers=headers, verify=False)
        msg = 'Status code: %s' % str(r.status_code)
        logger.writer(msg)
        if DEBUG:
            msg =  unicode(payload)
            logger.writer(msg)
            msg = str(r.text)
            logger.writer(msg)

    def fetcher(self, url):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(self.username + ':' + self.password),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        r = requests.get(url, headers=headers, verify=False)
        msg = 'Status code: %s' % str(r.status_code)
        logger.writer(msg)
        if DEBUG:
            msg = str(r.text)
            logger.writer(msg)
        return r.text


    def post_ip(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/ip/'
            msg =  '\r\nPosting IP data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def post_device(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/device/'
            msg =  '\r\nPosting device data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def post_location(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/buildings/'
            msg =  '\r\nPosting location data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def post_room(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/rooms/'
            msg =  '\r\nPosting room data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def post_rack(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/racks/'
            msg =  '\r\nPosting rack data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
    
    def post_pdu(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/pdus/'
            msg =  '\r\nPosting PDU data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)

    def post_pdu_update(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/pdus/rack/'
            msg =  '\r\nUpdating PDU data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def get_pdu_models(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/pdu_models/'
            msg =  '\r\nFetching PDU models from %s ' % url
            logger.writer(msg)
            self.fetcher(url)
        
    def get_racks(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/racks/'
            msg =  '\r\nFetching racks from %s ' % url
            logger.writer(msg)
            data = self.fetcher(url)
            return data
            
    def get_devices(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/devices/'
            msg =  '\r\nFetching devices from %s ' % url
            logger.writer(msg)
            data = self.fetcher(url)
            return data
            
    def get_racks(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/racks/'
            msg =  '\r\nFetching racks from %s ' % url
            logger.writer(msg)
            data = self.fetcher(url)
            return data

    def get_buildings(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/buildings/'
            msg =  '\r\nFetching buildings from %s ' % url
            logger.writer(msg)
            data = self.fetcher(url)
            return data
            
    def get_rooms(self):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/rooms/'
            msg =  '\r\nFetching rooms from %s ' % url
            logger.writer(msg)
            data = self.fetcher(url)
            return data

    def post_hardware(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/hardwares/'
            msg =  '\r\nAdding hardware data to %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            
    def post_device2rack(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/device/rack/'
            msg =  '\r\nAdding device to rack at %s ' % url
            logger.writer(msg)
            self.uploader(data, url)
            

class DB():
    def __init__(self):
        self.con = None
        self.tables = []
        self.datacenters_dcim = {}
        self.manufacturers = {}
        
    def connect(self):
        self.con = sql.connect(host=DB_IP,  port=DB_PORT,  db=DB_NAME, user=DB_USER, passwd=DB_PWD)
        
    def get_ips(self):
        net = {}
        adrese = []
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = "SELECT PrimaryIP FROM fac_Device" 
            cur.execute(q)
            ips = cur.fetchall()
        for line in ips:
            if line[0] != '':
                ip = line[0]
                net.update({'ipaddress':ip})
                rest.post_ip(net)
                
        with self.con:
            cur = self.con.cursor()
            q = "SELECT IPAddress FROM fac_PowerDistribution" 
            cur.execute(q)
            ips = cur.fetchall()
        for line in ips:
            if line[0] != '':
                ip = line[0]
                net.update({'ipaddress':ip})
                rest.post_ip(net)
                

    def get_locations(self):
        building = {}
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT DatacenterID,Name,DeliveryAddress,Administrator FROM fac_DataCenter'
            cur.execute(q)
        data = cur.fetchall()
        
        for row in data:
            #building.clear()
            id, name, address, contact = row
            building.update({'name':name})
            building.update({'address':address})
            building.update({'contact_name':contact})
            self.datacenters_dcim.update({id:name})
            rest.post_location(building)
            
    def get_rooms(self): 
        rooms = {}
        # get building IDs from D42
        building_map = {}
        buildings = json.loads(rest.get_buildings())
        for building in buildings['buildings']:
            building_map.update({building['name']:building['building_id']})
        
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT DatacenterID,Location FROM fac_Cabinet'
            cur.execute(q)
        data = cur.fetchall()
        for row in data:
            rid = row[0]
            room  = row[1]
            dc = self.datacenters_dcim[rid]
            id = building_map[dc]
            rooms.update({'name':room})
            rooms.update({'building_id':id})
            rest.post_room(rooms)
            
            
    def get_racks(self):
        rack = {}
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT CabinetID,DatacenterID,Location,CabinetHeight,Model FROM fac_Cabinet'
            cur.execute(q)
        data = cur.fetchall()
        for row in data:
            cid, did, room, height, name = row
            dc = self.datacenters_dcim[did]
            if height != 0:
                if name == '':
                    rnd =  str(random.randrange(101,9999))
                    name = 'Unknown'+rnd
                rack.update({'name':cid})
                rack.update({'size':height})                
                rack.update({'room':room})
                rack.update({'building':did})
                rest.post_rack(rack)
           
    
    def get_datacenter_from_id(self, id):
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT Name FROM fac_DataCenter where DataCenterID = %d' % id
            cur.execute(q)
        data = cur.fetchone()
        return data
        
      
                
    def get_room_from_cabinet(self, cabinetID):
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT DatacenterID,Location,Model FROM fac_Cabinet where CabinetID = %d' % cabinetID
            cur.execute(q)
        data = cur.fetchone()
        id, room, model = data
        datacenter = self.get_datacenter_from_id(id)[0]
        return datacenter, room, model
        
        
    def get_vendor_and_model(self, id):
        self.get_manufacturers()
        hardware = {}
        
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT ManufacturerID, Model FROM fac_DeviceTemplate WHERE TemplateID=%d' % id
            cur.execute(q)
        data = cur.fetchone()
        id, model = data
        vendor = self.manufacturers[id]
        return vendor, model


    def get_devices(self):
        roomdata = json.loads(rest.get_rooms())
        racks_d42 = json.loads(rest.get_racks())
                
        #print roomdata['rooms']
        device        = {}
        device2rack = {}
        hardware     = {}
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT Label, SerialNo, AssetTag, PrimaryIP,ESX, Cabinet,Position,Height,DeviceType,HalfDepth,BackSide, TemplateID FROM fac_Device'
            cur.execute(q)
        data = cur.fetchall()
        for row in data:
            name, serial_no, comment, ip,esx, rackid, position, size, devicetype, halfdepth, backside, tid = row
            datacenter, room, rack_name = self.get_room_from_cabinet(rackid)
            vendor, model = self.get_vendor_and_model(tid)
            for rdata in roomdata['rooms']:
                if rdata['building'] == datacenter:
                    if rdata['name'] == room:
                        storage_room_id = rdata['room_id']
                        storage_room     = room
            # post device
            device.update({'name':rackid})
            device.update({'serial_no':serial_no})
            if devicetype.lower() == 'switch':
                device.update({'is_it_switch':'yes'})
            device.update({'storage_room_id':storage_room_id})
            device.update({'storage_room':storage_room})
            device.update({'notes':comment})
            device.update({'manufacturer':vendor})
            device.update({'hardware':model})
            rest.post_device(device)
            
            #post device 2 rack
            device2rack.update({'device':name})
            #device2rack.update({'building':datacenter})
            #device2rack.update({'room':room})
            device2rack.update({'rack':rackid})
            device2rack.update({'start_at':position-1})
            if backside == '1':
                device2rack.update({'orientation':'back'})
            rest.post_device2rack(device2rack)
    
        
    def get_manufacturers(self):
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT ManufacturerID, Name from fac_Manufacturer'
            cur.execute(q)
        data = cur.fetchall()
        for row in data:
            id, vendor = row
            self.manufacturers.update({id:vendor})
            
    def get_depth(self, id):
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT HalfDepth FROM fac_Device WHERE TemplateID=%d' % id
            cur.execute(q)
        data = cur.fetchone()
        d = data[0]
        if d == 0:
            return 1
        elif d ==1:
            return 2
        
    def get_hardware(self):
        self.get_manufacturers()
        hardware = {}
        
        if not self.con:
            self.connect()
        with self.con:
            cur = self.con.cursor()
            q = 'SELECT TemplateID, ManufacturerID, Model, Height, Wattage, DeviceType, FrontPictureFile, RearPictureFile FROM fac_DeviceTemplate'
            cur.execute(q)
        data = cur.fetchall()
        for row in data:
            TemplateID, ManufacturerID, Model, Height, Wattage, DeviceType, FrontPictureFile, RearPictureFile = row
            depth = self.get_depth(TemplateID)
            vendor = self.manufacturers[ManufacturerID]
        
            hardware.update({'name':Model})
            hardware.update({'type':1})
            hardware.update({'size':Height})
            hardware.update({'depth':depth})
            hardware.update({'watts':Wattage})
            hardware.update({'manufacturer':vendor})
            hardware.update({'front_image':FrontPictureFile})
            hardware.update({'back_image':RearPictureFile})
            rest.post_hardware(hardware)

def main():
    db = DB()
    
    db.get_ips()
    db.get_locations()
    db.get_rooms()
    db.get_racks()
    db.get_hardware()
    db.get_devices()
    
    
if __name__ == '__main__':
    logger = Logger(LOGFILE)
    rest = REST()
    main()
    print '\n[!] Done!'
    sys.exit()
