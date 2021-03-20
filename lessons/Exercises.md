# Lesson 12 - Exercises #

In this lesson, you are going to be mostly on your own. Using some of your new scripting skills, and write a few scripts that achieve the goals below.

The plan is to use what you've learnt so far, and try to apply it to a *somewhat* realistic use case, such as performing some maintenance on a bunch of VMs.

-	Take inspiration from (e.g. copy) List all the script from the `pyvmomi` module to list VMs, and tweak it to:
	1.	print also the guest operating system
	1.	print the name of the ESXi server on which each VM is running
	1.	print the VM's annotation
	1.	power each powered on VM off
	1.	print the VM's current memory and cpu reservation
	1.	print the VM's current memory and cpu reservation, together with the max values (e.g. the total Mhz of the cpu of the host where the VM is running, and the total amount of memory of the VM
	1.	zero out any cpu or memory reservations for the VM
	1.	double their ram or the cpu reservation. If the VM has no reservation, set it to 10% of the max.

The `samples` directory will contains some example implementation for you refer to.


That completes the lesson. You should now be ready to move on to some additional topics. [Click here to return to the lesson list](../README.md)
