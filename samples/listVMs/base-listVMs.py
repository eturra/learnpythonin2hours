#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim
import argparse
import getpass
import re

def getArgs():
  """
    get the cli arguments
  """
  parser = argparse.ArgumentParser(
      description='Some script',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter
      )
  parser.add_argument('-k', '--insecure', action='store_true',
                      required=False, default=False,
                      help='Disable SSL verificatiojn for the connection')
  parser.add_argument('-s', '--host', required=True, action='store', help='Remote host to connect to')
  parser.add_argument('-o', '--port', type=int, default=443, action='store', help='Port to connect on')
  parser.add_argument('-u', '--user', required=False, action='store', default=getpass.getuser(), help='User name to use when connecting to host')
  parser.add_argument('-p', '--password', required=False, action='store', help='Password to use when connecting to host. If not supplied, it will be prompted')
  parser.add_argument('-v', '--vms', required=True, action='store', help='Regular expression matching the names of the virtual machines to list')
  parser.add_argument('-P', '--powerstate', required=False, action='store_true', help='Print also the powerstate of the VM')
  parser.add_argument('-I', '--ips', required=False, action='store_true', help='Print also the ip addresses of the VM')
  args =  parser.parse_args()
  if args.password is None:
      args.password = getpass.getpass(prompt='Enter {0.user}@{0.host}: '.format(args))
  return args

if __name__ == "__main__":
  args = getArgs()
  connect = SmartConnect
  if args.insecure:
    connect = SmartConnectNoSSL
  vmre = re.compile(args.vms)
  si = connect(
       host=args.host,
       user=args.user,
       pwd=args.password,
       port=args.port
      )
  for vm in filter(
       lambda vm: vmre.match(vm.name) is not None,
       si.content.viewManager.CreateContainerView(
                  container=si.content.rootFolder,
                  type=[ vim.VirtualMachine],
                  recursive=True,
                  ).view):
    print('{0} ({1})'.format(vm.name, vm._moId), end='')
    if args.powerstate:
      print(' ', vm.runtime.powerState, end='')
    if args.ips:
      print(' ', ','.join([y for x in vm.guest.net for y in x.ipAddress]), end='')
    print()
  Disconnect(si)


