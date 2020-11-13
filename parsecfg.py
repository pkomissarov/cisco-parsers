import re
from napalm import get_network_driver
from getpass import getpass


def pretty_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent+1)
        elif isinstance(value, list):
            for e in value:
                print('\t' * (indent+1) + str(e))
        else:
            print('\t' * (indent+1) + str(value))


def build_dict(cfg):
    """    Builds nested/deep dictionary from Cisco ios
    config using recursion function 'child()', which also
    changes "the most child" dictionaries to list if possible.
    For global Cisco commands make special keys based on
    first word in the command, e.g.: '# aaa #'
    """
    def group_global_childless(dct):
        for k in list(dct):
            if not dct[k]:
                dct.pop(k,None)
                w = k.split()
                if w[0] == 'no':
                    sec_name = f"# {w[1]} #"
                else:
                    sec_name = f"# {w[0]} #"
                if sec_name in dct.keys():
                    dct[sec_name].append(k)
                else:
                    dct.update({sec_name: [k]})

    def child(base_indent):
        nonlocal n
        result = {}
        while True:
            if n >= len(lines):
                break
            stripped = lines[n].lstrip()
            indent = len(lines[n]) - len(stripped)
            if base_indent >= indent:
                break
            n = n + 1
            result.update({stripped: child(indent)})
        # In case we got all values={} transform result to list
        if not [v for v in result.values() if v]:
            result = [k for k in result.keys()]
        return result

    n = 0
    cfg, special_cases = cut_special_cases(cfg)
    lines = cfg.splitlines()
    lines = [line for line in lines if line
                and not line.startswith('!')
                and not line.startswith('end')]
    dct = child(base_indent=-1)
    dct.update(special_cases)
    group_global_childless(dct)
    return(dct)


def cut_special_cases(cfg):
    """ Cut special cases (banners, boot markers) from config and
    put them in special_cases dictionary, that is also returned
    """
    special_cases = {}
    rgx = r"((?:(?P<type>(?:set\s+)*banner\s\w+\s+)(?P<delim>\S+))((.*\r?\n)+?.*?)(\3).*)"
    re_banners = re.findall(rgx,cfg)
    for r in re_banners:
        cfg = cfg.replace(r[0],"",1)
        special_cases.update({f"# {r[1]}#": r[0].splitlines()})
    rgx = r"boot-start-marker\r?\n(.*\r?\n)*boot-end-marker"
    re_boot = re.search(rgx,cfg)
    cfg = cfg.replace(re_boot[0],"",1)
    special_cases.update({"# boot #": re_boot[0].splitlines()})
    return cfg, special_cases


def main():
    driver = get_network_driver('ios')
    ipaddress = input('IP address: ')
    username = input('Username: ')
    ios_conn = driver(ipaddress, username, getpass())
    ios_conn.open()
    cfgs = ios_conn.get_config()
    dct = build_dict(cfgs['running'])
    pretty_print(dct,1)

if __name__ == "__main__":
    main()

