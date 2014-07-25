from twisted.internet import defer, task
from twisted.names import dns

def main(reactor):
    proto = dns.DNSDatagramProtocol(controller=Controller())
    reactor.listenUDP(10053, proto)

    return defer.Deferred()

class Controller(object):
    def messageReceived(self, message, proto, address):
        print "MESSAGE_RECEIVED", message.queries, "FROM", address
        message.answer = True
        message.answers = [
            dns.RRHeader(message.queries[0].name.name,
                         payload=dns.Record_A('192.0.2.1'))
        ]
        proto.writeMessage(message, address)

task.react(main)
