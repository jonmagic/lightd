from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import argparse
import logging
from rpi_rf import RFDevice

hostName = "0.0.0.0"
serverPort = 8081
gpio = 17
protocol = 1
pulse_length = 402
rfdevice = RFDevice(gpio)
rfdevice.enable_tx()
codes = {
    "toggle_power": 2677763,
    "delay_off": 2677762,
    "increase_brightness": 2677764,
    "decrease_brightness": 2677770,
    "minimum_brightness": 2677773,
    "100_brightness": 2677765,
    "75_brightness": 2677766,
    "50_brightness": 2677768,
    "25_brightness": 2677769,
    "diy_1": 2677771,
    "diy_2": 2677772,
    "diy_3": 2677774,
    "diy_4": 2677775,
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path_parts = self.path.split("/")
        controller = path_parts[1]
        print(f'controller: {controller}')
        command = path_parts[2]
        print(f'command: {command}')
        print(f'code: {codes[command]}')

        if controller == "pergola":
            if command in codes:
                rfdevice.tx_code(codes[command], protocol, pulse_length)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"status":"ok"}', "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    rfdevice.cleanup()
    webServer.server_close()
    print("Server stopped.")
