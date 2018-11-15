# import subprocess as sub
#
# p = sub.Popen(('sudo', 'tcpdump', '-lvv', '-B', '1024'), stdin=sub.PIPE, stdout=sub.PIPE)
# p.communicate(b'123456\n')
#
# try:
#     for row in iter(p.stdout.readline, b''):
#         print(row.rstrip())  # process here
# except KeyboardInterrupt:
#     pass
# finally:
#     p.send_signal(9)

# from pcap import pcap
import libpcap

def addr_finder(pkt, offset):
    return '.'.join(ord(pkt[i]) for i in range(offset, offset + 4))


sniffer = libpcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=0)
sniffer = libpcap.open()
for ts, pkt in sniffer:
    pkt = str(pkt, encoding='ascii', errors='ignore')
    print(pkt)
    # pkt = str(pkt)
    # print('%d\tSRC %-16s\tDST %-16s' % (
    #     ts,
    #     addr_finder(pkt, sniffer.dloff + 12),
    #     addr_finder(pkt, sniffer.dloff + 16)
    # ))
