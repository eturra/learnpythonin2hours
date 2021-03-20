# Lesson 10 - Modules: Part 3: lxml #

In this lesson we talk about lxml

## Basics ##

Python comes with its own xml library, called `xml`, and `lxml` implement almost exactly the same interface, so you can easily swap them. The advantages of `lxml` over `xml` are not just performance, but also safety if you are reading xml that someone else can craft. In general it is a good idea to use `lxml` if possible.

Regardless, if you plan to use the `xml` library that comes with [python because you don't want to install an additional component, most of what we are doing here will work for you too, you'll just have to remove the extra `l`

The lxml project is quite popular, and has a decently sized community, so you will be able to find a lot of help in internet, but the main place where to go for reference documentation is [here](https://lxml.de)

In the repository there's a collection of xml files you can use for some of the exercises in this module, they are under `samples/esximg/vibs/*.xml`. They come from an ESXi's image db, and they represent the installed vibs.

## lxml.etree ##

Let's say we want to read `samples/esximg/vibs/esx-base-699708918229420497.xml` as it is the largest file in the collection:

The first thing to do is find out how to read the file and parse the xml content, using `lxml.etree.parse`

```python
import lxml.etree as xtree
tree = xtree.parse(`samples/esximg/vibs/esx-base-699708918229420497.xml`)
```

There is no need to rename `lxml.etree` to `xtree`, but this allows you to easily switch from `lxml.etree` to python's `cElementTree` if you just replace that import with `import cElementTree as xtree`, for example.

The other observation here is that `lxml.etree.parse` receives a parameter that can be a filename, and in such a case, it takes care of opening the file and reading it, so we don't even need to worry about `with`, or what mode the file needs to be opened as.

Additionally, the `parse` method allows you to pass an http or https URL, and it will fetch it on its own, or even an opened file, if you happen to have it already open for other reasons.

The `tree` object is ready to use, so we need to start from the first element of the tree: the root.

This example assumes you are in the root of the repository, so that the file is accessible. You can specify, instead, the full path to the file, or copy it to your working directory and adjust the path, such as `/tmp/esx-base-699708918229420497.xml`.

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(root.tag)
```

This will produce `vib` as output. If you check the xml file, it contains something like this:

```xml
<vib version="5.0">
    <type>bootbank</type><name>esx-base</name><version>7.0.0-1.0.15843807</version><vendor>VMware</vendor><summary>ESXi base system</summary><description>VMware ESXi is a thin hypervisor integrated into server hardware. The compact, hardware embedded architecture of VMware ESXi raises the bar for security and reliability and lays the foundation for a dynamic, automated datacenter.</description><release-date>2020-03-16T09:40:25.912575+00:00</release-date><urls/>
    <relationships>
        <depends>
            <constraint name="esx-update" relation="&gt;=" version="7.0.0-1.0"/><constraint name="esx-update" relation="&lt;&lt;" version="7.0.0-1.1"/>
        </depends>
        <conflicts>
            <constraint name="misc-drivers" relation="&lt;&lt;" version="5.5.0"/><constraint name="native-misc-drivers" relation="&lt;&lt;" version="6.1.0"/>
        </conflicts>
        <replaces>
            <constraint name="esx-xlibs"/><constraint name="esx-tboot"/>
        </replaces>
[…]
        </payload>
    </payloads>
</vib>
```

So it is correct: the root of the document has a `vib` tag.

Now, what are the tags of the children of the root ?

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print('\n'.join([x.tag for x in r]))
```

```
type
name
version
vendor
summary
description
release-date
urls
relationships
software-tags
installdate
system-requires
file-list
acceptance-level
live-install-allowed
live-remove-allowed
cimom-restart
stateless-ready
overlay
payloads
```

This agrees with what we've seen in the file too.

How do we access the attributes of a node, then ? For example, the root (`vib`) node has an attribute called `version`: how can we read it?

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(root.attrib)
print(type(root.attrib))
print(type(root))
print(root.get('version'))
print(root.get('versions'))
print(root.get('versions', 1))
```

So, you can see that an xml node is of type `Element`, and it has an `attrib` property that gives access to a dict-like object with all the attributes of the node.

We can use the index (`[` and `]`) and the `get` usual ways of accessing the values from a key. The advantage of using `get` is that we can avoid receiving a `KeyError` if such attribute name is not in the node.

```
{'version': '5.0'}
<class 'lxml.etree._Attrib'>
<class 'lxml.etree._Element'>
5.0
None
1
```

If you don't like to use list comprehension to access the children of a node, you can use `getchildren`, but you can also use `find` and `findall`, to avoid looping through all the children if you know the tag of the node you're looking for.

The difference between `find` and `findall` is that `find` will always return 1 object, which, in the context of xml, is potentially not what you want, while `findall` will always return a list with all the objects that match.

The reason why `find` is potentially not what you want is because in xml, if you want to implement a list of items, you repeat multiple nodes with the same tag, so unless you know for sure that the tag you are looking for will never be repeated, it's better to use `findall`

Let's try an example with `vib.relationships.provides.provide`:

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(len(root.find('relationships').find('provides').findall('provide')))
```

This gives us `61`, because there are 61 `provide` objects. 

What if we did `find` instead of `findlal` ?

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(len(root.find('relationships').find('provides').find('provide')))
print(type(root.find('relationships').find('provides').find('provide')))
```

As you can see, `find` returns an element, and not a list, so `len` is not very helpful, but you also get no warning or error telling you that you probably shouldn't use `find`

```
0
<class 'lxml.etree._Element'>
```

That's why you need to be careful when you use `find`.

## xpath ##


Navigating an xml document like the above is Ok, but the power of xml is much easier to see if you use xpath, which `lxml` supports with the `xpath` method, but also in the `find` and `findall` methods:

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(len(root.findall('./relationships/provides/provide')))
```

And this returns `61` as expected, but it doesn't matter whether any of the nodes in that path is single or a list, xpath will descend them all, and thus using `find` in this case will just return the first from an unpredictable list.

Like everything in xml, xpath is extremely powerful and almost completely over-engineered, but if you learn the basics you can definitely do a lot of powerful scripts with just a few lines of code. Check out xpath [here](https://www.w3schools.com/xml/xpath_intro.asp)

Anyway, xpath allows you to traverse the tree even without starting from the root:


```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
print(len(tree.findall('//relationships/provides/provide')))
```

Notice how the root node (vib) is not included in the search, even from the tree.

And it can search by attribute value too!

For example, show me all the tags that contain an attribute called `version`, with value `5.0`:

```python
import lxml.etree as xtree
tree = xtree.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
print(','.join([x.tag for x in tree.findall("[@version='5.0']")]))
```

And the answer is `['vib']`. This will search the whole tree, automatically.

Nevertheless, `findall` has a subset of the features of `xpath`, `xpath` is much more powerful, but `findall` tends to be much faster.

Let's say you want to find out the size of each vib by just looking at their xml files:

```python
import sys
import os
import lxml.etree as xtree
path = '//vib/payloads/payload'
samplefilespath = 'samples/esximg/vibs/'
for file in filter(lambda x: x.endswith('.xml'), os.listdir(samplefilespath)):
  tree = xtree.parse(os.path.join(samplefilespath, file))
  for elem in tree.xpath(xpath):
    sys.stdout.write("{0}:{1}\n".format(elem.get('name'), elem.get('size')))
```

The output is this:

```
nenic:74308
uc_amd:5541
uc_hygon:29
uc_intel:1307186
crx:7379577
loadesx:13134
esxupdt:379876
tpmesxup:6064
weaselin:1076463
qfle3:846534
esx-dvfi:111660
elxnet:180908
lsi-msgp:137183
ilo:9382
nmlx4-co:196172
qedentv:1276215
nmlx4-en:180276
lsi-msgp:145218
sfvmk:180782
bnxtroce:93512
lsuv2-oe:4248
nmlx5-rd:87655
stage:12153
iavmd:61127
i40iwn:163419
lpnic:180091
xorg:1455532
vmkata:56892
lpfc:806950
nfnic:161904
vdfs:4558421
vmkfcoe:271599
qcnic:87393
qedrntv:1119691
qlnative:866010
stage:64163
vsan:14626056
mtip32xx:72129
iser:73079
vsanheal:499280
vsanmgmt:4061832
igbn:96541
esx-ui:3825881
smartpqi:102403
lsuv2-nv:2820
lsuv2-oe:4258
lsi-msgp:153908
vmkusb:331213
ne1000:180494
vmware-e:43898
cru:8512
stage:405
lsuv2-hp:24802
ntg3:33427
amscli:141538
lsuv2-oe:4392
stage:587096
sut:3287421
BOOTx64.EFI:182176
README:2202
b:135334
btldr:883321
efiboot.img:1048576
esximage.zip:1749650
extlinux:64011
fatBootSector:512
features:20
gptmbr.bin:424
isolinux.bin:14336
jumpstrt:20
k:5173387
ldlinux.sys:15218
mboot.c32:94000
mbr.bin:440
menu.c32:53456
metadata.xml:1696
osl.txt:4332389
precheck.py:135540
prep.py:5493
procfs:8800
s:12374755
safeboot.c32:61512
safeboot.efi:104448
sb:40801753
tpm:11326
useropts:30
vim:22977481
vmx:32651664
lsuv2-in:6772
stage:15645
nmlx4-rd:90673
brcmnvme:32244
nmlx5-co:461210
nvme-pci:30412
i40en:185932
native-m:578887
elx-esx-:470788
nvmerdma:43180
bnxtnet:197255
pvscsi:30935
qfle3f:346801
rste:221078
nvmxnet3:49406
stage:21968325
stage:6687567
lsuv2-sm:22416
qflge:201308
amsd:1223086
lsi-mr3:95644
nvmxnet3:57412
ixgben:161331
ssacli:7191693
elxiscsi:151376
lsuv2-ls:409575
qfle3i:109718
nhpsa:169352
vmw-ahci:66617
brcmfcoe:600424
```

We used `os.listdir` to get a list of files in the directory, we used `filter` to get only the files whose name ends in `.xml` (we could have used a list comprehension), and we used `os.path.join` to stitch together the directory and the file to get the full path.

After that, we used `xpath` to find all the objects.

If we want, we can use `findall` for the same purpose, but the search needs to start from the root:

```python
import sys
import os
import lxml.etree as xtree
path = '//payloads/payload'
samplefilespath = 'samples/esximg/vibs/'
for file in filter(lambda x: x.endswith('.xml'), os.listdir(samplefilespath)):
  tree = xtree.parse(os.path.join(samplefilespath, file))
  for elem in tree.findall(xpath):
    print("{0}:{1}".format(elem.get('name'), elem.get('size')))
```

## From String ##

What if you have some xml in a `str` , or better `bytes` object ?

There is a way to convert a `str` or a `bytes` object to a file-like object to pass to `parse`, but lxml does also offer the `fromstring` method, so we can use that:

Imagine that we want to get the news from CNN (from `http://rss.cnn.com/rss/edition.rss`), but pretend that that's not an RSS service, but rather an API call, as part of a series of API calls we need to make to a certain server, so we need to use `requests`:

```python
import lxml.etree as xtree
import requests
s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.verify = True
r = s.get('http://rss.cnn.com/rss/edition.rss')
if r.status_code == requests.codes.ok:
  root = xtree.fromstring(r.content)
  print('\n'.join(['{0} ({1})'.format(newsitem.find('title').text,newsitem.find('link').text) for newsitem in root.findall('./channel/item')]))
```

This will print the title of the news, and then a link to each news item.

This demonstrates how we can convert the data we got from `requests`, which is a `bytes` object, to the xml root (`fromstring` doesn't return the tree, so we get directly the root, so no need to do `getroot`).


## lxml.objectify ##

For some, this way of using xml, with `find` and findall`, or `xpath`, or getchildren() and its friends `getparent`, `getprevious`, and `getnext` is a bit too difficult, and because of that, `lxml.objectify` was introduced:

It will create properties of each node witht he name of the tags, so you can access them directly.

Let's try again the inital parsing of `samples/esximg/vibs/esx-base-699708918229420497.xml`, where we were looking for `//relationships/provides/provide`:

```python
import lxml.objectify as objectify
tree = objectify.parse('samples/esximg/vibs/esx-base-699708918229420497.xml')
root = tree.getroot()
print(len(root.relationships.provides.provide))
print('\n'.join([ x.attrib.get('name') for x in root.relationships.provides.provide]))
```

The first `print` will produce `61` as expected, and the 2nd shows you and example fo how to read the items in the list.

Most of the methods available in `xml.etree` are still available in `lxml.objectify`, so you can even do `import lxml.objectify as xtree` in an existing script, but it is not a good idea because reversing the change will not be possible, if you start using the "objectified" tags.

## lxml.html ##

If you arrived so far and are now very excited about pairing `requests` and `lxml.etree` to go and write your own google search engine, and scrape all the websites, you will be bisappointed: more than 90% of the html on the internet is invalid xml!!!

Try to parse any web page:

```python
import lxml.etree as xtree
import requests
s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.verify = True
r = s.get('http://www.vmware.com')
if r.status_code == requests.codes.ok:
  root = xtree.fromstring(r.content)
```

You'll get something like this:

```
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "src/lxml/etree.pyx", line 3237, in lxml.etree.fromstring
  File "src/lxml/parser.pxi", line 1896, in lxml.etree._parseMemoryDocument
  File "src/lxml/parser.pxi", line 1784, in lxml.etree._parseDoc
  File "src/lxml/parser.pxi", line 1141, in lxml.etree._BaseParser._parseDoc
  File "src/lxml/parser.pxi", line 615, in lxml.etree._ParserContext._handleParseResultDoc
  File "src/lxml/parser.pxi", line 725, in lxml.etree._handleParseResult
  File "src/lxml/parser.pxi", line 654, in lxml.etree._raiseParseError
  File "<string>", line 44
lxml.etree.XMLSyntaxError: xmlParseEntityRef: no name, line 44, column 192
```

So, what can we do ? Well, lxml is a very big project, and they have a solution for this too (the title of this chapter kind of gave it away already): `lxml.html`

So, now, if we want to get all the links in the page, followed by all the images, we can do this:

```python
import lxml.html
import requests
s = requests.Session()
s.headers['Accept'] = 'application/xml'
s.verify = True
r = s.get('http://www.vmware.com')
if r.status_code == requests.codes.ok:
  root = lxml.html.fromstring(r.content)
  print('\n'.join([ str(x.attrib.get('href', x.attrib.get('content', ''))) for x in root.xpath('//a')]))
  print('\n'.join([ str(x.attrib.get('src', '')) for x in root.xpath('//img')]))
```

## Namespace maps ##

When xml was designed, it was a bit over-engineered, to try to make it able to deal with every situation. One of the consequences of this is that there was a concern that 2 different authors would use the same tag for multiple purposes, and to avoid this, a concept ot a "namespace" was added.

What this means is that it is possible, int he xml, to attach a namespace to each tag, so that ewven if 2 elements had the same tag, you could distinguish because they would have different namespaces.

This sounds great, but it makes using xml a bit more complicated.

One example of namespaces can be found in the ovf files, you can find an example here: https://download3.vmware.com/software/VSANOVF/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf

Download the file, to let's say `/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf`, and if you look at the first part of the file, you see this:

```xml

<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns="http://schemas.dmtf.org/ovf/envelope/1" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:vmw="http://www.vmware.com/schema/ovf">
  <References>
    <ovf:File ovf:href="layout.json" ovf:size="351" ovf:id="layout.json_id"/>
    <File ovf:href="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-system.vmdk" ovf:size="925941760" ovf:id="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-system.vmdk_id"/>
    <File ovf:href="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-cloud-components.vmdk" ovf:size="98054656" ovf:id="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-cloud-components.vmdk_id"/>
    <File ovf:href="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-log.vmdk" ovf:size="2124800" ovf:id="VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962-log.vmdk_id"/>
  </References>
[…[]
```

Notice the `xmlns` pieces.

If you are using `find` or `findall` and all any other method in any `lxml` modules, something peculiar will now happen:

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()
print(len(root.findall('References')))
```

The surprise is that this will print `0`! Try to print all the tags that are direct children of root??

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()
print(len(root.findall('References')))
print('\n'.join([x.tag for x in root]))
```

And you will see what's happening with the namespaces:

```
{http://schemas.dmtf.org/ovf/envelope/1}References
{http://schemas.dmtf.org/ovf/envelope/1}NetworkSection
{http://www.vmware.com/schema/ovf}IpAssignmentSection
{http://schemas.dmtf.org/ovf/envelope/1}DiskSection
{http://schemas.dmtf.org/ovf/envelope/1}VirtualSystem
{http://schemas.dmtf.org/ovf/envelope/1}Strings
```

What ? All the tags now have a bit prepended! How are we going to deal with this ? 

The root node has a field called `nsmap`, which is the mapping between namespaces names and their values, based on what is in the root node in the xml document.

The default namespace has key `None`, which unfortunately is not (yet?) handled in lxml, but you can use it anyway:

Let's look at the map first:

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()
print(root.nsmap)
```

This is what it looks like:

```
{'ovf': 'http://schemas.dmtf.org/ovf/envelope/1', None: 'http://schemas.dmtf.org/ovf/envelope/1', 'rasd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData', 'vssd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'vmw': 'http://www.vmware.com/schema/ovf'}
```

So, we can use the default namespace, let's try:

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

defaultns = '{' + root.nsmap.get(None) + '}'

print(len(root.findall(defaultns + 'References')))
```

Now it works!

But what about tags that have a namespace attached (and thus do not use the default namespace) ? For example `File` ?

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

defaultns = '{' + root.nsmap.get(None) + '}'
ovfns = '{' + root.nsmap.get('ovf') + '}'
print(len(root.findall(defaultns + 'References/' + ovfns + 'File')))
```

This works, it produces `4`, but there's another way:


```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

defaultns = '{' + root.nsmap.get(None) + '}'
print(len(root.findall(defaultns + 'References/ovf:File', namespaces=root.nsmap)))
```

This also returns `4`: if you pass a mapping via `namespaces`, you can use the short name then in the search term.

It is unfortunate that the default is not used when the tag has no namespaces, but with our knowledge of python, we can fix that too!

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

nsmap = root.nsmap

if None in nsmap:
  nsmap['None'] = nsmap[None]

print(len(root.findall('None:References/ovf:File', namespaces=nsmap)))
```

And the result is `4` too!. Basically what we did is create a new namespace, called `'None'`, and we copied over the default. Then, we can use `None:` where the default would be.

It's not as nice as if the default could apply, because in our case we wouldn't match tags without any namespace attached.

Also, there's a risk that we are obliterating an existing namescape really called `'None'`, so in a real script, it would probably be better to check if `'None'` exists already, and change it to something else, maybe random.

But, this is just for a script to show you what namespaces are, so we are ok.

What about `xpath`, you ask ?

Well, there's one extra annoyance: `xpath` can't deal with the `None` in the nsmap (not the `'None'` we added, the original one:


```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

nsmap = root.nsmap

if None in nsmap:
  nsmap['None'] = nsmap[None]

print(len(root.xpath('//ovf:File', namespaces=nsmap)))
```

Will not work:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "src/lxml/etree.pyx", line 1579, in lxml.etree._Element.xpath
  File "src/lxml/xpath.pxi", line 259, in lxml.etree.XPathElementEvaluator.__init__
  File "src/lxml/xpath.pxi", line 131, in lxml.etree._XPathEvaluatorBase.__init__
  File "src/lxml/xpath.pxi", line 55, in lxml.etree._XPathContext.__init__
  File "src/lxml/extensions.pxi", line 81, in lxml.etree._BaseContext.__init__
TypeError: empty namespace prefix is not supported in XPath
```

So, the fix is to `pop` the default:

```python
import lxml.etree as xtree
import requests

tree = xtree.parse('/tmp/VMware-vSAN-File-Services-Appliance-7.0.0.1000-15817962_OVF10.ovf')
root = tree.getroot()

nsmap = root.nsmap

if None in nsmap:
  nsmap['None'] = nsmap.pop(None)

print(len(root.xpath('//ovf:File', namespaces=nsmap)))
```

## Creating xml ##

Apart from reading and processing xml, the  `lxml` modules allow you to create a root node and add children and attributes, to build a new xml document and save it, or to load it, add or delete nodes, and save it.

The first thing to do is decide whether you want to create a full tree, or just an xml section. This depends no what you plan to do with it, and what is required by whoever will receive it.

Since the tree contains the document, we will see how to do this with the full tree, but if you plan to just create an xml section, you can just avoid creating the tree and work with the root.

```python
import lxml.etree as xtree
root = xtree.Element('test')
tree = xtree.ElementTree(element = root)
print(xtree.tostring(tree))
```

```
b'<test/>'
```

Now, if you want to add attributes to a node, you can use `Element.set` or access `Element.attrib` directly as a dictionary.


```python
import lxml.etree as xtree
root = xtree.Element('test')
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
print(xtree.tostring(tree))
```

As you can see, both methods work.

```
b'<test version="0.3.7" someotherattribute="True"/>'
```

How do we add nodes ?

You can use `Element.append`, even directly or with a temporary object, or using the `SubElement` factory:

```python
import lxml.etree as xtree
root = xtree.Element('test')
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element('idea')
root.append(idea1)
idea1.set('description', 'good')
root.append(xtree.Element('idea', description='not so good'))
xtree.SubElement(root, 'idea', description='bad')
print(xtree.tostring(tree))
```

As you can see, you can either use the 

```
b'<test version="0.3.7" someotherattribute="True"><idea description="good"/><idea description="not so good"/><idea description="bad"/></test>'
```

If you have a tree, you can also save it to a file:

```python
import lxml.etree as xtree
root = xtree.Element('test')
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element('idea')
root.append(idea1)
idea1.set('description', 'good')
root.append(xtree.Element('idea', description='not so good'))
xtree.SubElement(root, 'idea', description='bad')
tree.write('/tmp/a.xml')
```

And the content of the xml file is the same.

```xml
<test version="0.3.7" someotherattribute="True"><idea description="good"/><idea description="not so good"/><idea description="bad"/></test>
```

You can handle namespaces too

```python
import lxml.etree as xtree
namespaces = {'nstest':'http://some.url/with/namespace'}
root = xtree.Element('{http://some.url/with/namespace}test', nsmap=namespaces)
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element('idea')
root.append(idea1)
idea1.set('{http://some.url/with/namespace}description', 'good')
root.append(xtree.Element('{http://some.url/with/namespace}idea', description='not so good'))
xtree.SubElement(root, '{http://some.url/with/namespace}idea', description='bad')
tree.write('/tmp/a.xml')
```

And our document will have the namespaces applied:

```xml
<nstest:test xmlns:nstest="http://some.url/with/namespace" version="0.3.7" someotherattribute="True"><idea nstest:description="good"/><nstest:idea description="not so good"/><nstest:idea description="bad"/></nstest:test>
```

You can use the `QName` object to avoid the complexity of dealing with namespaces, if you prefer:

```python
import lxml.etree as xtree
namespaces = {'testns': 'http://some.url/with/namespace'}
def testns(tag):
  "Shortcut to using tag with QName and the testns"
  return xtree.QName(namespaces.get('testns'), tag)

root = xtree.Element(testns('test'), nsmap=namespaces)
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element(testns('idea') )
root.append(idea1)
idea1.set('description', 'good')
root.append(xtree.Element(testns('idea'), description='not so good'))
xtree.SubElement(root, testns('idea'), description='bad')
tree.write('/tmp/a.xml')
```

As you can see, it is a little bit easier:

```xml
<testns:test xmlns:testns="http://some.url/with/namespace" version="0.3.7" someotherattribute="True"><testns:idea description="good"/><testns:idea description="not so good"/><testns:idea description="bad"/></testns:test>
```

Of you expect the document to be readable also by humans, you mygt want to "prettify" the output:

```python
import lxml.etree as xtree
namespaces = {'testns': 'http://some.url/with/namespace'}
def testns(tag):
  "Shortcut to using tag with QName and the testns"
  return xtree.QName(namespaces.get('testns'), tag)

root = xtree.Element(testns('test'), nsmap=namespaces)
tree = xtree.ElementTree(element = root)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element(testns('idea') )
root.append(idea1)
idea1.set('description', 'good')
root.append(xtree.Element(testns('idea'), description='not so good'))
xtree.SubElement(root, testns('idea'), description='bad')
tree.write('/tmp/a.xml', pretty_print=True)
```

And the output is indented and nicer to read (although bigger, and thus more expensive):

```xml
<testns:test xmlns:testns="http://some.url/with/namespace" version="0.3.7" someotherattribute="True">
  <testns:idea description="good"/>
  <testns:idea description="not so good"/>
  <testns:idea description="bad"/>
</testns:test>
```

This works also on the `tostring`

```python
import lxml.etree as xtree
namespaces = {'testns': 'http://some.url/with/namespace'}
def testns(tag):
  "Shortcut to using tag with QName and the testns"
  return xtree.QName(namespaces.get('testns'), tag)

root = xtree.Element(testns('test'), nsmap=namespaces)
root.set('version', '0.3.7')
root.set('someotherattribute', 'True')
idea1 = xtree.Element(testns('idea') )
root.append(idea1)
idea1.set('description', 'good')
root.append(xtree.Element(testns('idea'), description='not so good'))
xtree.SubElement(root, testns('idea'), description='bad')
print(xtree.tostring(root, pretty_print=True).decode('utf-8'))
```

We use `decode` here just to convert it to string, so that `print` understands the newlines:

```xml
<testns:test xmlns:testns="http://some.url/with/namespace" version="0.3.7" someotherattribute="True">
  <testns:idea description="good"/>
  <testns:idea description="not so good"/>
  <testns:idea description="bad"/>
</testns:test>
```

That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
