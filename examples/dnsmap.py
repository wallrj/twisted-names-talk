import sys
from twisted.internet import defer, task
from twisted.names import client, error

CONCURRENCY = 100

def subdomains(parent_domain, children):
    yield parent_domain
    for child in children:
        yield child + '.' + parent_domain

class DNSMapper(object):
    def __init__(self):
        self.success = []
        self.failure = []
        self.timeout = []

    def _handle_result(self, res, domain):
        answers, authority, additional = res
        if answers:
            self.success.append(domain)
            sys.stdout.write("{domain} ({count})\n".format(domain=domain, count=len(answers)))

    def _handle_error(self, result, domain):
        error_type = result.trap(error.DNSQueryTimeoutError, error.DomainError, defer.TimeoutError)
        if error_type in (error.DNSQueryTimeoutError, defer.TimeoutError):
            self.timeout.append(domain)
        elif error_type is error.DomainError:
            self.failure.append(domain)

    def sender(self, domains):
        resolver = client.Resolver(servers=[('8.8.8.8', 53)])
        for domain in domains:
            d = resolver.lookupAllRecords(domain, timeout=(5,10))
            d.addCallback(self._handle_result, domain)
            d.addErrback(self._handle_error, domain)
            yield d

    def summary(self):
        return 'SUCCESS: {success}, FAILURE: {failure}, TIMEOUT: {timeout}'.format(
            success=len(self.success),
            failure=len(self.failure),
            timeout=len(self.timeout))

def main(reactor, parent_domain, wordfile=None):
    if wordfile in (None, '-'):
        wordfile = sys.stdin
    else:
        wordfile = open(wordfile)

    mapper = DNSMapper()
    domains = subdomains(parent_domain, (word.strip() for word in wordfile))

    clients = []
    for i in range(CONCURRENCY):
        client = task.cooperate(mapper.sender(domains))
        clients.append(client.whenDone())
    result = defer.DeferredList(clients)

    def print_summary(res):
        print(mapper.summary())

    result.addBoth(print_summary)
    return result

task.react(main, sys.argv[1:])
