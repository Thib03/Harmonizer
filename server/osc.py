from pythonosc import udp_client
import time
import random


class Client:
    def __init__(self, ip="127.0.0.1", port=3000):
        self.ip = ip
        self.port = int(port)
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def send(self, payload, channel="/chords"):
        self.client.send_message(channel, payload)


if __name__ == '__main__':
    port = 3000
    ips = ["127.0.0.1", "10.24.227.10"]
    clients = []
    for ip in ips:
        client = Client(ip, port)
        clients.append(client)
    chord_length = 4
    # regularyly generate random chords in range [60, 72]
    while True:
        chord = [random.randint(0, 11) for i in range(chord_length)]
        for client in clients:
            print("Sending chord", chord, "to IP", client.ip)
            client.send(chord, "/chords")
        time.sleep(5)
