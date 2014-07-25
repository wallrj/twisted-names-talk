from netaddr import IPNetwork
from twisted.internet import defer, task
from twisted.names import client

def main(reactor):
    pending = []
    for addr in IPNetwork('79.170.40.0/24'):
        d = client.lookupPointer(addr.reverse_dns, timeout=(1,))
        pending.append(d)

    return defer.DeferredList(pending, consumeErrors=True).addCallback(printResult)

def printResult(results):
    good = 0
    for success, result in results:
        if success:
            answers, authority, additional = result
            print 'RESULT: ', [(a.name.name, a.payload) for a in answers]
            good += 1
    print good, 'responses to', len(results), 'queries'

task.react(main)
