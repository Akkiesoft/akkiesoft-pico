import board
from busio import SPI
from digitalio import DigitalInOut
import adafruit_connection_manager
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K

class akkie_wiznet5k():
    def __init__(self,
            cs   = board.GP17,
            sck  = board.GP18,
            mosi = board.GP19,
            miso = board.GP16
        ):
        self.connected = False
        self.eth = None
        self.pool = None
        self.ssl_context = None
        self.cs = DigitalInOut(cs)
        self.spi_bus = SPI(sck, MOSI=mosi, MISO=miso)

    def connect(self):
        try:
            print("Trying to connect to wired network...")
            self.eth = WIZNET5K(self.spi_bus, self.cs)
            self.pool = adafruit_connection_manager.get_radio_socketpool(self.eth)
            self.ssl_context = adafruit_connection_manager.get_radio_ssl_context(self.eth)
            self.connected = True
        except Exception as e:
            print("Failed to connect: %s" % e)
        if not self.connected:
            print("Failed to connect to wired network.")

    def disconnect(self):
        # WIZNET5K does not implement the disconnect.
        pass