import wifi
import socketpool
import ssl

class akkie_wifi():
    def __init__(self, ap_list):
        self.ap_list = ap_list
        self.connected = False
        self.pool = None
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.load_verify_locations(cadata="")

    def connect(self):
        wifi.radio.start_station()
        wifi.radio.enabled = True
        for ap in self.ap_list:
            try:
                print("Trying to connect with %s..." % ap[0])
                wifi.radio.connect(ap[0], ap[1])
                print("Connected with %s." % ap[0])
                self.pool = socketpool.SocketPool(wifi.radio)
                self.connected = True
                break
            except Exception as e:
                print("Failed to connected: %s" % e)
        if not self.connected:
            print("Failed to connected all aps.")

    def disconnect(self):
        wifi.radio.enabled = False
        wifi.radio.stop_station()
        self.connected = False
        self.pool = None