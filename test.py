import subprocess as sub

p = sub.Popen(('sudo', 'tcpdump', '-lvv', '-B', '1024'), stdin=sub.PIPE, stdout=sub.PIPE)
p.communicate(b'123456\n')

with p.stdout:
    for line in iter(p.stdout.readline, b''):
        print(line)

p.wait()



