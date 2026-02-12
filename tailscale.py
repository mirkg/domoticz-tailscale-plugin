
import subprocess
import json
import domoticz
import traceback
from time import time

class Tailscale:

    last_update = 0
    ieee = ''

    def __init__(self, cmd_path, track_devices, interval):
        self.cmd_path = cmd_path
        self.track_devices = track_devices
        self.interval = interval
        self.ndevices = {}
        
    def run_request(self, args, command='/tailscale.sh'):
        cmd = " ".join(args)
        try:
            output = subprocess.check_output(self.cmd_path + command + " " + cmd, stderr=subprocess.STDOUT, shell=True)
            return {'resp': 'executed: ' + cmd, 'output': json.loads(output)}
        except Exception as ex:
            domoticz.debug('failed: ' + cmd +  ' with output=[' + str(traceback.format_exc().splitlines()) + ']')
            return {'resp': 'failed: ' + cmd, 'error': str(ex)}

    def check_updates(self):
        global status
        now = int(time())
        if self.last_update + self.interval < now:
            try:
                self.last_update = now
                status = self.run_request(['status', '--json'])
                domoticz.debug('status: ' + str(status))
                if self.track_devices:
                    if not 'error' in status:
                        self.process_devices(status['output'])
            except Exception:
                domoticz.error('check status failed: ' + traceback.format_exc())

    def process_devices(self, status):
            ndev = {'id': 'backend_state', 'name':'BackendState', 'type': 'Text'}
            if not ndev['id'] in self.ndevices:
                self.ndevices[ndev['id']] = self.create_domoticz_dev(ndev)
            self.update_device_string_value(ndev['id'], status['BackendState'])

            if not status['BackendState'] == 'Running':
                for did in self.ndevices.keys():
                    self.update_device_bool_value(did, False)            
            else:
                d = status['Self']
                ndev = {'id': d['ID'], 'name':d['DNSName'], 'type': 'Contact'}
                if not ndev['id'] in self.ndevices:
                    self.ndevices[ndev['id']] = self.create_domoticz_dev(ndev)
                self.update_device_bool_value(ndev['id'], d['Online'])

                if 'Peer' in status and status['Peer'] != None:
                    peers = status['Peer']
                    for peer in peers.keys():
                        ndev = {'id': peers[peer]['ID'], 'name':peers[peer]['DNSName'], 'type': 'Contact'}
                        if not ndev['id'] in self.ndevices:
                            self.ndevices[ndev['id']] = self.create_domoticz_dev(ndev)
                        self.update_device_bool_value(ndev['id'], peers[peer]['Online'])

    def update_device_bool_value(self, id, value):
        dev = self.ndevices[id]
        dev.sValue = ""
        if value:
           dev.nValue = 1
        else:
            dev.nValue = 0
        dev.Update()
    
    def update_device_string_value(self, id, value):
        dev = self.ndevices[id]
        dev.sValue = value
        dev.nValue = 0
        dev.Update()

    def create_domoticz_dev(self, dev):
        domoticz.debug('creating device: ' + str(dev))
        device = domoticz.get_device(dev['id'], 1)        
        if device == None:
            device = domoticz.create_device(
                Unit=1,
                DeviceID=dev['id'],
                Name=dev['name'],
                TypeName=dev['type']
            )
        return device

    def connect(self):
        return self.run_request(['up'])

    def disconnect(self):
        return self.run_request(['down'])

    def devices(self):
        devs = []
        ret = self.run_request(['status', '--json'])
        if not 'error' in ret:
            keys = ['ID', 'HostName', 'DNSName', 'OS', 'TailscaleIPs', 'LastSeen', 'Online']
            ndev = {}
            d = ret['output']['Self']
            for key in keys:
                ndev[key] = d[key]
            devs.append(ndev)            
            if 'Peer' in ret['output'] and ret['output']['Peer'] != None:
                peers = ret['output']['Peer']
                for peer in peers.keys():
                    ndev = {}
                    for key in keys:
                        ndev[key] = peers[peer][key]
                    devs.append(ndev)
        return devs

    def login(self):
        domoticz.debug('tailscale login')
        return self.run_request(['login', '--timeout', '1s'])

    def logout(self):
        domoticz.debug('tailscale logout')
        return self.run_request(['logout'])

    def status(self):
        return self.run_request(['status', '--json'])

    def update_cert(self, domain):
        return self.run_request([domain], command='/tailscale_update_cert.sh')
