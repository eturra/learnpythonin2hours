#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim
from pyVim.task import WaitForTask
import argparse
import getpass
import re

def generateProgress(taskDescription):
  """
  Generate a function that will print the task update, but customised to print the message in taskDescription
  """
  def progressCB(task, percentDone):
    """
    Print the progress of a task
    """
    if percentDone is None:
      percentDone = task.info.state
    if isinstance(percentDone, int):
      percentDone = '{0}%% complete'.format(percentDone)
    print('{0} is {1}.'.format(taskDescription, percentDone))
  return progressCB

def getArgs():
  """
    get the cli arguments
  """
  parser = argparse.ArgumentParser(
      description="Double the reservation",
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
  #To avoid recalculating the cpu clock every time, we keep a dict to map the name to the cpu clock
  cpus = dict()
  for vm in filter(
       lambda vm: vmre.match(vm.name) is not None,
       si.content.viewManager.CreateContainerView(
                  container=si.content.rootFolder,
                  type=[ vim.VirtualMachine],
                  recursive=True,
                  ).view):
    if vm.runtime.host.name not in cpus:
      cpus[vm.runtime.host.name] = int(vm.runtime.host.hardware.cpuInfo.hz/1000000)
    cpureservation = vm.config.cpuAllocation.reservation * 2
    if cpureservation == 0:
      #If it si 0 we can't double it, so we will set it to 10% fo max cpu
      cpureservation = int(cpus.get(vm.runtime.host.name) / 10)
    memoryreservation = vm.config.memoryAllocation.reservation * 2
    if memoryreservation == 0:
      #If it is 0, we can't double it, so we will set it to 10% of the total memory
      memoryreservation = int(vm.config.hardware.memoryMB / 10)

    #We need to build the configspec
    cs = vim.vm.ConfigSpec(
        #We need to pass the changeVersion from the VM's, otherwise the change will fail
        changeVersion = vm.config.changeVersion,
        cpuAllocation = vim.ResourceAllocationInfo(reservation=cpureservation),
        memoryAllocation = vim.ResourceAllocationInfo(reservation=memoryreservation),
        )
    task = vm.ReconfigVM_Task(spec=cs)
    WaitForTask(task, si=si, onProgressUpdate=generateProgress('Setting the reservation to {0} Mb and {1} Mhz for VM {2}'.format(memoryreservation, cpureservation, vm.name)))
  Disconnect(si)


