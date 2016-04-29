# Python App on Bluemix using Secure Gateway for on-prem data access
## Setting up the Data Center

This project provides the skeleton for a modern Cloud-based web application that accesses on-premises data,
a database behind the corporate firewall. It shows how a (public or dedicated) cloud environment is used for
a ["System of Engagement"](https://en.wikipedia.org/wiki/Systems_of_Engagement), while sensitive data remains
in a ["System of Record"](https://en.wikipedia.org/wiki/System_of_record).

In this document we describe how to set up the "Data Center" part of the example. It is simulated by a virtual
machine running either on [Bluemix](http://www.ibm.com/cloud-computing/bluemix/) or on your own infrastructure. If you came to this document by accident, please start reading the [overview document](README.md).

In the following we describe how to provision a Virtual Machine on Bluemix, then how to install a MySQL database server

### Create a Bluemix Virtual Machine (VM)

We will use a VM in this demo to represent our on-premises data center and will host a MySQL instance in it. This represents our "System of Record".

1. Create a Bluemix Account

    [Sign up for Bluemix][bluemix_url] or use an existing account.
    
2. Create a VM from the console dashboard by clicking on `Run Virtual Machines`

	**Note**: Right now the Virtual Machines are only open for new users in the EU-GB/London region. You may need to switch your account to use that region.
	
	![](https://raw.githubusercontent.com/data-henrik/Bluemix-onprem-data/master/screenshots/BluemixRegion.png)

	**Note**: If you do not yet have access to the Bluemix VM beta, complete your request and wait for your confirmation email. This may take up to a few days, so please be patient!

	a) Depending on the offered choices select an `Ubuntu` or `Debian` image for your VM. Then click `NEXT`.
	![](https://raw.githubusercontent.com/data-henrik/Bluemix-onprem-data/master/screenshots/BluemixSelectVM.png)

	b) On the next page, give the VM a name.

	c) Keep `SINGLE` as type.

	d) Select the smallest offered size.

	e) Make sure that `Assign pubic IP address` is active, so that the VM is accessible from outside of Bluemix. Note that this public IP address is needed only to administrate the VM directly from your computer.

	f) Create an SSH key for securely connecting to your VM for administration. For instructions on how to do this, check out the [documentation][vm_ssh_key_docs]. Make sure to save the generated key to your machine.

	g) Default to the `private` network (if more types are offered).  

	h) Click `CREATE` to create and launch your VM. Once it has started, take note of your public IP address on the VM dashboard. The IP address is needed during some steps later on.
	![](https://raw.githubusercontent.com/data-henrik/Bluemix-onprem-data/master/screenshots/Bluemix_VMDetails.png)

3. Open a terminal and make sure that your private key file is in your working directory. It needs to have the correct permissions, to set them use the command:

	```sh
	$ chmod 700 ./NameOfMyPrivateKeyFile.pem
	```

4. Use the ssh command to log into your newly created VM. Make sure to substitute the public IP address of your VM (it should start with 129) for XXX.XX.XXX.XX.

	```sh
	$ ssh -i ./NameOfMyPrivateKeyFile.pem ibmcloud@XXX.XX.XXX.XX
	```

	If you receive a "No route to host" error, it is an indicator that the network fabric has not yet completed the setup. Wait a minute or two and retry.

5. Resync your VM's package index files from their sources:

	```sh
	$ sudo apt-get update
	```

Your Virtual Machine is now ready to have software installed. For our example we are going to use the MySQL database server.


### Install a MySQL database instance

6. Install MySQL on your VM:

	```sh
	$ sudo apt-get install mysql-server
	```

	**Note**: During the installation process you will be asked to assign a password to your MySQL server. Make sure to write it down, you will need it for database access.


7. Grant remote access to your MySQL DB instance (by using the password you assigned in step 1 above), create a database and then restart the mysql service:

	```
	$ mysql -u root -p
	Enter password: <PasswordFromStep1>

	mysql> GRANT ALL ON *.* to root@'%' IDENTIFIED BY '<PasswordFromStep1>';
	mysql> flush privileges;
	mysql> create database readlist;
	mysql> exit

	$ sudo service mysql restart
	```

Please note that `create database readlist` is not part of the actual installation, but included for convenience. That database is needed for our application and the step is described in the database setup again.

## Closing

In this part of the documentation we have shown how to set up a Virtual Machine on Bluemix and to install the MySQL database server into it. Please go back to the [overview document](README.md) to continue.

[bluemix_url]: http://www.ibm.com/cloud-computing/bluemix/
