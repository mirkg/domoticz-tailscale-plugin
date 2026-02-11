from api.plugin import *


commands = dict({
    'plugin_info': Info,
    'connect': Connect,
    'disconnect': Disconnect,
    'getstatus': GetStatus,
    'getdevices': GetDevices,
    'login': Login,
    'logout': Logout,
    'update_tls_cert': UpdateCert,
})
