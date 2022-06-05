#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os


def is_root():
    if os.geteuid() != 0:
        print("!! This script required sudo privelages !!")
        sys.exit()


parser = argparse.ArgumentParser(description='Change Your Mac Adress')

parser.add_argument('--interface',
                    '-i',
                    default='eth0',
                    help='Which interface you want to change the Mac Adress for - Defaults is eth0')

parser.add_argument('--action',
                    '-a',
                    default='reset',
                    help='What do you want to do with your mac adress? Options: reset, change')


def bash(command):
    return subprocess.check_output(['bash', '-c', command], text=True)


def main(args):
    interface = args.interface
    mode = ''
    match args.action:
        case 'reset':
            mode = '-p'
        case 'change':
            mode = '-r'
        case _:
            print("Action is not supplied or is invalid. Exiting...")
            sys.exit()
    print("Changing The Mac Adress...")
    response = bash(
        f'airmon-ng check kill; \
        service NetworkManager stop; \
        ifconfig {interface} down; \
        macchanger {mode} {interface}; \
        rfkill unblock all; \
        service NetworkManager start; \
        ifconfig {interface} up'
    )
    print(response)
    print('!! Have Fun !!')


if __name__ == '__main__':
    is_root()
    main(parser.parse_args())
