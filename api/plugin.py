from api.command import APICommand
import domoticz

class Connect(APICommand):
    def execute(self, params):    
        resp = self.adapter.connect()
        self.send_response(resp)

class Disconnect(APICommand):
    def execute(self, params):    
        resp = self.adapter.disconnect()
        self.send_response(resp)

class Login(APICommand):
    def execute(self, params):    
        resp = self.adapter.login()
        self.send_response(resp)

class Logout(APICommand):
    def execute(self, params):    
        resp = self.adapter.logout()
        self.send_response(resp)

class GetDevices(APICommand):
    def execute(self, params):    
        resp = self.adapter.devices()
        self.send_response(resp)

class GetStatus(APICommand):
    def execute(self, params):    
        resp = self.adapter.status()
        self.send_response(resp)

class UpdateCert(APICommand):
    def execute(self, params):
        resp = self.adapter.update_cert(params['domain'])
        self.send_response(resp)

class Info(APICommand):
    def execute(self, params):
        data = domoticz.get_plugin_parameters()
        self.send_response(data)