import subprocess
host = 'DESKTOP-5GDVQA7'
pingAvg=0
for c in range(10):
    out, error = subprocess.Popen(
        ['ping', host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        ).communicate()
    out = out.decode()
    # print(out)
    out = out[::-1]
    ping = int(out[4:out.find("=")].strip()[::-1])
    print(ping)
    pingAvg += ping
pingAvg/=10
print(pingAvg)
