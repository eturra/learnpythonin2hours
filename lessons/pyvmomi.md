# Lesson 10 - Modules: Part 7: pyvmomi #

In this lesson we talk about pyvmomi a python bindings for vSphere SDK API.

## Basics ##

The main interface for using vSphere API is WSDL and SOAP based, but there are a few libraries available to hide the complexity behind WSDL and SOAP.

For python, the most popular is pyvmomi. The name is linked to "vmomi" being the protocol used by vCenter.

The pyvmomi project is in [github](https://github.com/vmware/pyvmomi), and the documentation of the vSphere API is [here](https://code.vmware.com/apis/968/vsphere).

If you download the vSphere SDK zip file, which contains the bindings for Java, you will also find the offline documentation, under `SDK/vsphere-ws/ReferenceGuide`.

The `pyvmomi` module is basically a small python layer that uses http and xml to take care of transporting the vSphere Managed Objects and their properties to and from the vCenter server, so its structure is following the vSphere Managed Object architecture.

This means that if you read the vSphere SDK documentation, you will also get the documentation for `pyvmomi`.

There are a few additional components in `pyvmomi`, that are not documented in the vSphere SDK, so we will cover some of these aspects, and then we will just go through some examples of how to map the vSphere SDK to a `pyvmomi` script.

We will assume that the reader is familiar with the vCenter Managed Object modes, vSphere inventory concepts, and at least familiar with vCenter's Managed Object Browser (a.k.a. "mob").

The latter, together with the vSphere SDK Reference Guide, is a great resource for figuring out how to do things and where to find things in `pyvmomi` (just as with any other library to use the vSphere SDK API).

## The Managed Object Model ##

Before starting, we will go over a brief review of the Managed Object model.

First of all, we need to make a distinction between the so called "Managed Objects" and simple data objects: Managed objects in vCenter have a managed object reference to identify them, which looks like this: `<type>-<number>`, where `type` is a string representing the type of the object, and the number is just a sequential number identifying the object itself. This Managed Object Reference, often called MoRef or moid, can be used to retrieve the object. For example, if you point your browser to a URL like this: `https://vCenter/mob/?moid=<moref>`, it will take you to that object.

The Managed Objects have properties but also methods, such as `PowerOnVM_Task` for a `VirtualMachine`. Data Objects, on the other hand, are just structures with a bunch of properties, used to carry the data together, they do not have any identifier, and can only be obtained by using a property or method from a Managed Object.

vCenter's inventory and all the other components that are available programmatically, are organised in a hierarchical structure that looks like a tree whose root is the `ServiceInstance` object.

If you don't know what MoRef to use, try `https://vCenter/mob/?moid=ServiceInstance`, because the `ServiceInstance` is a so called "singleton", meaning that there is only 1, and therefore it has a special MoRef without number. When you log in to vCenter's "mob", that's the default place where you will end up.

From the `ServiceInstance` you need to go to the `ServiceContent` object, and you can do that via the `ServiceInstance.content` property, or `ServiceInstance.RetrieveServiceContent()` method.

Either way, this will give you access to the whole vCenter server. Many of the Managed Objects you find there are "Manager" type of objects, that allow you to control some aspect of vCenter, and the property called `rootFolder` is the root of the inventory, which takes you to a list of datacentres.

The inventory is accessible under each datacentre is organised in various folders, one for virtual machines, one for hosts, one for networks, and one for storage. If you check the UI, you will see that it follows the same structure.

The datacentre also has other properties such as `network` or `datastore`, to give you some short-cuts, but look for the "…Folder" properties.

Please note that here we've been talking about vCenter, but the ESXi server uses the same vmomi protocol, and so `pyvmomi` (and the "mob", if you enable it) will work with an ESXi server just as well. From now on we will mention "server" or "vCenter", but you can replace that with ESXi too.


## Importing ##

So far we've seen modules that could be imported with a simple "import" command.

With `pyvmomi`, it is a bit more complicated, because it is made of a few packages, and each contains a bunch of modules.

The modules you will use mostly are `pyVim.connect` and `vim` from `pyVmomi`. The first is to give you the tools to connect, and the second to give you access to the object definitions if you need them.

Lastly, if you need a machine with `pyvmomi` and you are in a rush, the ESXi server has python and a version of `pyvmomi` installed.

## Connecting to vCenter ##

The first thing you will want to do is obviously to connect to vCenter.

There are a few ways to do so, but the best is to use `SmartConnect` (and its companion, `Disconnect`)

`SmartConnect`, if successful, will return the `ServiceInstance` object for you (The log-in process uses that object too)

```python
from pyVim.connect import SmartConnect, Disconnect

si = SmartConnect(host='servername',
   user='username',
   pwd='password',
   )
Disconnect(si)
```

This should give you an error like this:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3/dist-packages/pyVim/connect.py", line 831, in SmartConnect
    supportedVersion = __FindSupportedVersion(protocol,
  File "/usr/lib/python3/dist-packages/pyVim/connect.py", line 714, in __FindSupportedVersion
    serviceVersionDescription = __GetServiceVersionDescription(protocol,
  File "/usr/lib/python3/dist-packages/pyVim/connect.py", line 637, in __GetServiceVersionDescription
    tree = __GetElementTree(protocol, server, port,
  File "/usr/lib/python3/dist-packages/pyVim/connect.py", line 604, in __GetElementTree
    conn.request("GET", path)
  File "/usr/lib/python3.9/http/client.py", line 1255, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/usr/lib/python3.9/http/client.py", line 1301, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.9/http/client.py", line 1250, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.9/http/client.py", line 1010, in _send_output
    self.send(msg)
  File "/usr/lib/python3.9/http/client.py", line 950, in send
    self.connect()
  File "/usr/lib/python3.9/http/client.py", line 1424, in connect
    self.sock = self._context.wrap_socket(self.sock,
  File "/usr/lib/python3.9/ssl.py", line 500, in wrap_socket
    return self.sslsocket_class._create(
  File "/usr/lib/python3.9/ssl.py", line 1040, in _create
    self.do_handshake()
  File "/usr/lib/python3.9/ssl.py", line 1309, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)
```

This is because you probably are using a self-signed certificate in your vCenter, or the certificate's CA is not trusted on this machine.

There are a few ways to deal with this, but the easiest is to use `SmartConnectNoSSL` instead of `SmartConnect`. If you script will later use `argparse` (and it should), you will be able to add an option `--insecure`, and then you can do something like this:

```python

from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
import argparse
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
  return parser.parse_args()

if __name__ == "__main__":
  args = getArgs()
  connect = SmartConnect
  if args.insecure:
    connect = SmartConnectNoSSL
  si = connect()
```

In the next exercises we will use `SmartConnect` or `SmartConnectNoSSL` directly without the above distinction, but in a real script you should consider doing something like that (and add `logging`).

Another consideration to make is that you might want to disconnect in case of an exception.

Unfortunately the `ServiceInstance` object is not a context manager, but you now have enough knowledge to create one yourself. If you don't want to do that, you can use the `atextt` module:

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
```

This will take a bit of time to connect, but the script will work.  From now on, you can assume we will use `atexit` this way even if you don't see it in the examples.

What is this `si` object then ?

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
print(str(si))
print(type(si))
```

Will print:

```
'vim.ServiceInstance:ServiceInstance'
<class 'pyVmomi.VmomiSupport.vim.ServiceInstance'>
```

This `si` object is a `vim.ServiceInstance` object as we expected, and we see that `str` and `repr` are the same and they both show you the type of the object followed by its "MoRef", which as we know, for the `ServiceInstance` is `ServiceInstance`.

All the objects that come from vCenter (or ESXi) will have a type whose name starts with `vim`. This is how they are called internally in vCenter, and in `pyvmomi`, to try to maintain the same naming convention, they are all kept in the `vim` module.

If you don't need to create new objects, but you just want to use the objects you can fetch from vCenter, you don't need the `vim` module.

Let's look a bit further into this `ServiceInstance` object! Check the documentation of the `ServiceInstance`, or go to the "mob", and you'll see what methods and properties we can use!

For example, there's a property called `serverClock`, what does it provide ?

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
print(si.serverClock)
```

No surprise there: it's the time according to the server, as the name suggested.

```
2021-03-26 10:35:07.967812+00:00
```

You've now used a property of a Managed Object using `pyvmomi`! What about a method?

If you check the documentation (or the mob) there's a method called `CurrentTime` that takes no parameters: what will that do ?

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
print(si.CurrentTime())
```

No surprise there either: it's the same as `serverClock`, but instead of a property, it's a method. These 2 look designed just for the purpose of learning the APIs.

```
2021-03-26 10:38:53.942578+00:00
```

Now that you know how to use properties and methods, we can explore the tree, which is accessible via the `content` property or the `RetrieveServiceContent` method. We will use the property just because it's shorter to type:

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
print(si.content)
```

The output is a bit long, but this will be the case for most of the managed objects we will see from here on.

Note how in my example I am connecting to an ESXi server too:

```
(vim.ServiceInstanceContent) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   rootFolder = 'vim.Folder:ha-folder-root',
   propertyCollector = 'vmodl.query.PropertyCollector:ha-property-collector',
   viewManager = 'vim.view.ViewManager:ViewManager',
   about = (vim.AboutInfo) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      name = 'VMware ESXi',
      fullName = 'VMware ESXi 7.0.0 build-15843807',
      vendor = 'VMware, Inc.',
      version = '7.0.0',
      build = '15843807',
      localeVersion = 'INTL',
      localeBuild = '000',
      osType = 'vmnix-x86',
      productLineId = 'embeddedEsx',
      apiType = 'HostAgent',
      apiVersion = '7.0.0.0',
      instanceUuid = <unset>,
      licenseProductName = 'VMware ESX Server',
      licenseProductVersion = '7.0'
   },
   setting = 'vim.option.OptionManager:HostAgentSettings',
   userDirectory = 'vim.UserDirectory:ha-user-directory',
   sessionManager = 'vim.SessionManager:ha-sessionmgr',
   authorizationManager = 'vim.AuthorizationManager:ha-authmgr',
   serviceManager = 'vim.ServiceManager:ha-servicemanager',
   perfManager = 'vim.PerformanceManager:ha-perfmgr',
   scheduledTaskManager = <unset>,
   alarmManager = <unset>,
   eventManager = 'vim.event.EventManager:ha-eventmgr',
   taskManager = 'vim.TaskManager:ha-taskmgr',
   extensionManager = <unset>,
   customizationSpecManager = <unset>,
   customFieldsManager = <unset>,
   accountManager = 'vim.host.LocalAccountManager:ha-localacctmgr',
   diagnosticManager = 'vim.DiagnosticManager:ha-diagnosticmgr',
   licenseManager = 'vim.LicenseManager:ha-license-manager',
   searchIndex = 'vim.SearchIndex:ha-searchindex',
   fileManager = 'vim.FileManager:ha-nfc-file-manager',
   datastoreNamespaceManager = 'vim.DatastoreNamespaceManager:ha-datastore-namespace-manager',
   virtualDiskManager = 'vim.VirtualDiskManager:ha-vdiskmanager',
   virtualizationManager = <unset>,
   snmpSystem = <unset>,
   vmProvisioningChecker = <unset>,
   vmCompatibilityChecker = <unset>,
   ovfManager = 'vim.OvfManager:ha-ovf-manager',
   ipPoolManager = <unset>,
   dvSwitchManager = 'vim.dvs.DistributedVirtualSwitchManager:ha-dvsmanager',
   hostProfileManager = <unset>,
   clusterProfileManager = <unset>,
   complianceManager = <unset>,
   localizationManager = 'vim.LocalizationManager:ha-l10n-manager',
   storageResourceManager = 'vim.StorageResourceManager:ha-storage-resource-manager',
   guestOperationsManager = 'vim.vm.guest.GuestOperationsManager:ha-guest-operations-manager',
   overheadMemoryManager = <unset>,
   certificateManager = <unset>,
   ioFilterManager = <unset>,
   vStorageObjectManager = 'vim.vslm.host.VStorageObjectManager:ha-vstorage-object-manager',
   hostSpecManager = <unset>,
   cryptoManager = 'vim.encryption.CryptoManagerHost:ha-crypto-manager',
   healthUpdateManager = <unset>,
   failoverClusterConfigurator = <unset>,
   failoverClusterManager = <unset>
}
```

Now let's navigate the inventory to list all the VMs in the VM's root folder.

Check the documentation for the `vim.Folder` object, and you'll see that the contents are available under the `childEntity` property, which is a list.

To get to the VMs, we need to use the `vmFolder` object in the `vim.Datacenter` objects, which are available in the `rootFolder` object.

Let's start with printing the datacentre's names:

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
for dc in si.content.rootFolder.childEntity:
  print('Datacentre:', dc.name)
```

The result will depend on what is in your server.

Now, as per the documentation, the VMs are in the `vmFolder`.


```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
for dc in si.content.rootFolder.childEntity:
  print('Datacentre:', dc.name)
  for vm in dc.vmFolder.childEntity:
    print(' VM:', vm.name)
```

In my server I have only 1 VM:

```
Datacentre: datacenter
 VM: test1
```

In the `vmFolder` there might be also folders, together with other VMs, so the above code will not work very well.

What you need to do is check what type of object it is, and for that we need the `vim` module too:

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
for dc in si.content.rootFolder.childEntity:
  print('Datacentre:', dc.name)
  for o in dc.vmFolder.childEntity:
    if isinstance(o, vim.VirtualMachine):
      print(' VM:', o.name)
```

Now we are skipping any object in the `vmFolder` that is not a virtual machine.

Recursing all the folders is a matter of dealing with any other `Folder` objects too


```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
for dc in si.content.rootFolder.childEntity:
  print('Datacentre:', dc.name)
  folders = [dc.vmFolder]
  while folders:
    folder = folders.pop()
    for o in folder.childEntity:
      if isinstance(o, vim.VirtualMachine):
        print(' VM:', o.name)
      elif isinstance(o, vim.Folder):
        folders.insert(1, o)
```

Python prefers iteration to recursion, so the example above is using iteration, but the reader can try to do the same in a recursive way, and compare the performance.

Another exercise could be to print the full path, with all the folder names before the VM name.

## View ##

Navigating the inventory this way is probably something that you would do only if you are planning to implement some form of UI, typically you either know what specific VM you need, or you want to search them all.

If you know exactly which VM you want, you can use the `SearchIndex` object, for example, if you know the full path in the inventory, you can use `FindByInventoryPath`:

Be sure to change the `path` to match your environment, checking the name of each object you traverse, starting from the datacentre, to the `vmFolder` (check its `name` property! It is 'vm'), to any other folder, tot he VM. 

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
path='/Datacentre/vm/test1'
vm = si.content.searchIndex.FindByInventoryPath(path)
print(vm.name)
```

If you want to see all the VMs (or any other Managed Object) matching a certain criteria, you probably want to use a view (you can also use something called `PropertyCollector`, but you need to be very experienced with the vSphere API to do that, and its use is the same with `pyvmomi` or any other bindings, so we will consider that out of scope here.)

If you check the vSphere API documentation, creating a view is done via the `vim.ViewManager` object, which can be accessed through the `viewManager` property of the `ServiceContent` object, using the `CreateContainerView` method.

In `pyvmomi`, every time you need to pass a parameter to a method, you should try to use the named(or optional) parameters, rather than the positional one. If the parameter is not a simple type, but a `vim` type, you will need to use its constructor.

The `CreateContainerView` does not need a complex object, so it will not need any constructor:

```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
vmview = si.content.viewManager.CreateContainerView(
                  container=si.content.rootFolder,
                  type=[ vim.VirtualMachine],
                  recursive=True,
                  )
for vm in vmview.view:
  print('VM:', vm.name)
```

The container view shows you all the objects of the specified types (can be many, since it's a list), descending from a certain container.

In the example above, our starting point was `si.content.rootFolder`, but if you want to list only the VMs in a certain datacentre, you can replace the value for the `container` parameter to match.

This is handy, for example, if you want to implement the same type of script as the one we implemented above, where we list all the VMs per datacentre, and you can use 2 levels of view too


```python
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

atexit.register(Disconnect, si)

si = SmartConnectNoSSL(host='servername',
   user='username',
   pwd='password',
   )
for dc in si.content.viewManager.CreateContainerView(
                  container=si.content.rootFolder,
                  type=[ vim.Datacenter],
                  recursive=True,
                  ).view:
  print('Datacentre:', dc.name)
  for vm in si.content.viewManager.CreateContainerView(
                  container=dc.vmFolder,
                  type=[ vim.VirtualMachine],
                  recursive=True,
                  ).view:
    print('VM:', vm.name)
```

## Examples ##

We have covered the main aspects of using `pyvmomi` that are not specifically documented in the vSphere API documentation.

The main skill you need to hone for being proficient with `pyvmomi` is figuring out how the API itself, and that means practising searching through its documentation.

For that, what we can do now is cover a few examples and exercises.

### Find all VMs ##

Let's say we want to write a small script that takes as parameter (and therefore will need `argparse`) a regular expression (meaning we need `re`), and the script will print the name (and the moref) of all the VMs whose name matches the supplied regular expression.

Optionally we would like to print its power state and its IP addresses. And since we're using `argparse`, we also want the `-k` option, and options to specify server, username and password. If the password is not specified, we'd like the script to ask for it, using `getpass`.

First we set up the skeleton with `argparse`

```python
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
    print('{0} ({1})'.format(vm.name, vm._moId))
  Disconnect(si)
```

There is nothing special here, we are using `filter` with `re.match`, we've learnt about this in previous modules.

Now, you need to add the option to print the VM's power state. For this, you can go and look up the `VirtuamMachine` object in the documentation, or browse the "mob", find a VM and see where its power state is.

Make sure you do this, as it's the main point of this exercise, before you read the next few lines.

The documentation should show you that the `VirtualMachine` has a `runtime` property, which contains the `powerState` object. Another way to get to it would be to look for `powerState` in the list of properties, and from there follow the line of "property of" until you get to the `VirtualMachine` object.

There are many other ways to "stumble" into some part of this sequence, for example, you might search among all the so called "Enum" for one with the value `poweredOn`, which will take you to `vim.VirtualMachine.PowerState`, and then follow the "Property of".

That is the important part: getting familiar with the process of figuring out what object, method or property does what you need.

If you go the "mob" route, the advantage is that you see the values together with the property names, the downside is that it is not searchable, you need to click around and use your creativity. The best is to use both.

Anyway, now we know that what we want is `VirtualMachine.runtime.powerState`, and so all we need to do is add another option to enable this feature:

```python
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
    print()
  Disconnect(si)
```

Lastly, we want to also print the IP addresses of the VM.

After a bit of research, you will have found that the object you want is probably `vim.vm.GuestInfo`, but there are 3 sources for this information: `ipAddress`, `net` and `ipStack`.

We will discard `ipAddress` because it is whatever the system detects as "primary", which is not reliable.

Between the other 2, the documentation states that 'ipStack' is about the configured IPs, and the `net` (a list of `vim.vm.GuestInfo.NicInfo`) is what is in use.

We will take the `net`, as we want to know what is in use, so we can ssh or rdp to the VMs we are interested in.

The `net` property is a list, with an entry for each interface. For each interface there's a property called `ipAddress`, which is a list of IP addresses, and one called `ipConfig`, which contains a property called `ipAddress`, which is a list of objects, one per IP address, containing also the subnet prefix and other information.

For what we need to do, `net[].ipAddress[]` will do.

So, we will need to add another option, we can call it `--ips`, and print the information.

We will be dealing with a list of lists, and we'd like to merge it all into one list, which then we `join` with a comma. This means we need a nested list comprehension.

To make the nested list comprehension work, we need the outer comprehension first, and the inner one after. This is a very pythonic way, but if you prefer, you can build a function to do this with 2 for loops.

```python
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
```

### Tasks ###

Many methods, especially methods that perform operations that might take more than an instant to complete, will return a `Task` managed object.

The script can't assume that the method succeeded, it must repeatedly check the status of the task until it is completed, and then check if it completed successfully or with an error.

Let's say you've been asked to write a script that changes the annotation of any VM matching the regular expression.

We can re-use the script from the previous examples, but here we will need to wait for the task to complete, and this might require you to learn how to use the property collector.

Luckily `pyvmomi` comes with a helper module called `pyVim.task`, which contains `WaitForTask` and `WaitForTasks`. We will look at the first, the second just takes a list of tasks.

`WaitForTask` expects the task through the mandatory `task` parameter, and the `ServiceInstance` object via the mandatory `si` parameter.

Optionally, you can pass a callable via `onProgressUpdate` to print the progress. The callable should accept 2 parameters: `task` and `percentDone`.

You can use something like this: (taken from the documentation)
```python
            def OnTaskProgressUpdate(task, percentDone):
                print 'Task %s is %d%% complete.' % (task, percentDone)
```

Unfortunately it doesn't return the task when it's finished, so you need to store the task first, and then call `WaitForTask`, and then check if it finished successfully.

If you want, you can go look at the file `pyVim/task.py`, and change `WaitForTask` to return the `task` object at the end to make this more user-friendly, and maybe also spy a bit how it uses the property collector.

```python
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
      description="Change the VM's annotation",
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
  parser.add_argument('-A', '--annotation', required=True,  help='Set the annotation to ANNOTATION')
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
  #We can prepare the configspec outside of the loop since it will be the same for each VM
  cs = vim.vm.ConfigSpec(annotation=args.annotation)
  for vm in filter(
       lambda vm: vmre.match(vm.name) is not None,
       si.content.viewManager.CreateContainerView(
                  container=si.content.rootFolder,
                  type=[ vim.VirtualMachine],
                  recursive=True,
                  ).view):
    task = vm.ReconfigVM_Task(spec=cs)
    WaitForTask(task, si=si, onProgressUpdate=generateProgress('Reconfiguring annotation for VM ' + vm.name))
  Disconnect(si)
```

Note that we used a function generator for the progress callback. This is a way to overcome the situation here you want to pass an extra parameter (the message to print) to where it is expected to pass a function that does not receive such parameter.

Also, notice that this script is OK without checking the task status after `WaitForTask` because we don't have anything else to do, but if your script had a few chained operations to perform, such as change the annotation and then do something else, you'd need to check `Task.info.state`.

If you check the documentation, `Task.info.state` is an enum called `vim.TaskInfo.State`, and the value we want is `success`. If you want, you can take advantage of the fact that the enum is translated to a string, `'success'`, but the proper, reliable way of checking is to use the enum value:

This would translate to something like this:

```python
    if task.info.state == vim.TaskInfo.State.success:
      doSomething()
```

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
