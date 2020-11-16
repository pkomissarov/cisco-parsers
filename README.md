# cisco-parsers
Various Cisco parsers

## parsecfg.py :: parse ios config to python dictionary. 
To see how it'll be parsed use CLI in two possible ways:

- ````python3 parsecfg.py config-ios.sample````  (get config from specified file)
- ````python3 parsecfg.py````  (interactively asks ip, user, password to connect to device and get config)

To use as a library in your code put parsecfg.py to your project folder, then import and use:

    from parsecfg import build_dict
    dct = build_dict(your_config)
