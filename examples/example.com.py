zone = [
    SOA(
        'example.com',
        mname = "ns1.example.com",
        rname = "dnsmaster.example.com",
        serial = 2013092001,
        refresh = "1H",
        retry = "1H",
        expire = "1H",
        minimum = "1H"
    ),

    NS('example.com', 'ns1.example.com'),
    MX('example.com', 0, 'mail.example.com'),

    A('example.com', '192.0.2.10'),
    CNAME('www.example.com', 'example.com'),
    A('mail.example.com', '192.0.2.20'),
    A('ns1.example.com', '192.0.2.30'),
]
