import pyshark
import time

cap = pyshark.LiveCapture(interface='enp3s0' , bpf_filter=None)

print('Starting...')
# cap.sniff(timeout=50)
print('Setting timeout...')
for packet in cap.sniff_continuously(packet_count=None):
    print('Just arrived:', packet)
    time.sleep(1)