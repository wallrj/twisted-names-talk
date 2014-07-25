from twisted.internet import task
from twisted.names import dns

def main(reactor):
    proto = dns.DNSDatagramProtocol(controller=None)
    reactor.listenUDP(0, proto)

    d = proto.query(('8.8.8.8', 53), [dns.Query('www.example.com', dns.AAAA)])
    d.addCallback(printResult)
    return d

def printResult(res):
    print 'ANSWERS: ', [a.payload for a in res.answers]

task.react(main)
