import wifi
import socketpool

use_ssl = False

ap_list = [
  ('myap', 'mypassphrase'),
]

con = 0
for ap in ap_list:
    try:
        print("Trying to connect with %s..." % ap[0])
        wifi.radio.connect(ap[0], ap[1])
        print("Connected with %s." % ap[0])
        con = 1
        break
    except Exception as e:
        print("Failed to connected: %s" % e)

if con:
    radio = wifi.radio
    pool = socketpool.SocketPool(wifi.radio)
    if use_ssl:
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(cadata="")
else:
    print("Failed to connected all ap(s).")