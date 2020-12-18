# cisco-parsers
Various Cisco parsers

## parsecfg.py :: parse ios config to python dictionary. 
To see how it'll be parsed use CLI in two possible ways:

- ````python3 parsecfg.py config-ios.sample````  (get config from specified file)
- ````python3 parsecfg.py````  (interactively asks ip, user, password to connect to device and get config)

To use as a library in your code put parsecfg.py to your project folder, then import and use:

    from parsecfg import build_dict
    dct = build_dict(your_config)

Script parse config to dict of lists (or dict of dicts of lists for "deep" sections of config). If key is starting with '#', than it means it's not a part of config, but just a key containing list of similar commands (about same thing). Resulting dict looks like this:  
````
{
        "ip dhcp pool HOME_LAN": [
                "network 172.16.1.0 255.255.255.0",
                "default-router 172.16.1.1",
                "domain-name foo.com",
                "dns-server 172.16.1.5",
                "lease 2"
        ],
        "# logging #": [
                "logging snmp-authfail",
                "logging buffered 65535 debugging",
                "logging rate-limit 50",
                "no logging console guaranteed",
                "logging facility local6",
                "logging source-interface Loopback0",
                "logging 172.16.1.5",
                "logging 172.16.1.7",
        ],
        "archive": {
                "log config": [
                        "logging enable",
                        "hidekeys"
                ],
                "path ftp://ns.foo.com//tftpboot/Foo-archive": [
                ]
        }
}
````
