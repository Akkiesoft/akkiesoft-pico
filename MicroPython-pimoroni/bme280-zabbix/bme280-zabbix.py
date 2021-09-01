import time
import struct
import json
from breakout_bme280 import BreakoutBME280,FILTER_COEFF_OFF, STANDBY_TIME_0_5_MS, OVERSAMPLING_2X, OVERSAMPLING_4X, OVERSAMPLING_8X, NORMAL_MODE
from pimoroni_i2c import PimoroniI2C
import picowireless
import config


TCP_MODE = const(0)

def connect(host_address, port, client_sock, timeout=1000):
    picowireless.client_start(host_address, port, client_sock, TCP_MODE)
    t_start = time.time()
    timeout /= 1000.0
    while time.time() - t_start < timeout:
        state = picowireless.get_client_state(client_sock)
        if state == 4:
            return True
        time.sleep(1.0)
    return False


def zabbix_send(client_sock, ip, data, port=10051, timeout=5):
    host_address = tuple(int(x) for x in ip.split('.'))
    print("Connecting to {1}.{2}.{3}.{4}:{0}...".format(port, *host_address))
    if not connect(host_address, port, client_sock):
        print("Connection failed!")
        return False
    print("Connected!")

    data_len = struct.pack('<Q', len(data))
    http_request = b'ZBXD\x01' + data_len + data

    print("Sending data...")
    picowireless.send_data(client_sock, http_request)

    t_start = time.time()
    while True:
        if time.time() - t_start > timeout:
            picowireless.client_stop(client_sock)
            print("Request timed out.".format(host_address, port))
            return False

        avail_length = picowireless.avail_data(client_sock)
        if avail_length > 0:
            break
    print("Got response: {} bytes".format(avail_length))

    response = b""
    while len(response) < avail_length:
        data = picowireless.get_data_buf(client_sock)
        response += data

    response = response.decode("utf-8")
    print(response)

    picowireless.client_stop(client_sock)


picowireless.init()

print("Connecting to {}...".format(config.ssid))
picowireless.wifi_set_passphrase(config.ssid, config.password)

while picowireless.get_connection_status() != 3:
    pass
my_ip = picowireless.get_ip_address()
print("Local IP: {}.{}.{}.{}".format(*my_ip))
client_sock = picowireless.get_socket()


PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
bme = BreakoutBME280(i2c)
bme.configure(FILTER_COEFF_OFF, STANDBY_TIME_0_5_MS, OVERSAMPLING_8X, OVERSAMPLING_4X, OVERSAMPLING_2X, NORMAL_MODE)

while True:
    print("--------------------")
    temperature,pressure,humidity = bme.read()
    pressure = pressure / 100
    print("Temp:%.2f" % (temperature))
    print("Humi:%.2f" % (humidity))
    print("Pres:%.2f" % (pressure))
    data = json.dumps({
      "request":"sender data",
      "data":[
        {"host":"pico-wireless","key":"bme280.temp","value":temperature},
        {"host":"pico-wireless","key":"bme280.humidity","value":humidity},
        {"host":"pico-wireless","key":"bme280.pressure","value":pressure}
    ]})
    zabbix_send(client_sock, config.zabbix_server_ip, data)
    time.sleep(60)
