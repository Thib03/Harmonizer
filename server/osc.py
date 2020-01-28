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
    client = Client()
    chord_length = 4
    # regularyly generate random chords in range [60, 72]
    while True:
        chord = [random.randint(60, 72) for i in range(chord_length)]
        print("Sending chord", chord)
        client.send(chord, "/chords")
        time.sleep(5)
