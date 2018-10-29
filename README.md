[![Follow on Twitter](https://img.shields.io/twitter/follow/websecurify.svg?logo=twitter)](https://twitter.com/websecurify)


	 ________  ________  ___  ___      ___ _______   ________     
	|\   ___ \|\   __  \|\  \|\  \    /  /|\  ___ \ |\   __  \    
	\ \  \_|\ \ \  \|\  \ \  \ \  \  /  / | \   __/|\ \  \|\  \   
	 \ \  \ \\ \ \   _  _\ \  \ \  \/  / / \ \  \_|/_\ \   _  _\  
	  \ \  \_\\ \ \  \\  \\ \  \ \    / /   \ \  \_|\ \ \  \\  \| 
	   \ \_______\ \__\\ _\\ \__\ \__/ /     \ \_______\ \__\\ _\ 
	    \|_______|\|__|\|__|\|__|\|__|/       \|_______|\|__|\|__|
	
	by SecApps
	

Docker-based execution environment for SecApps.com for local testing in continuous deliver/integration environments and more.

# How To Install

Simply do:

	docker pull websecurify/secapps-driver

# How To Use

There are various ways you can use the driver. Use the `-h` flag for options:

	docker run --name secapps-driver --rm websecurify/secapps-driver -h

# Reports

All tools generate reports in `/output` folder. To get the reports out of docker you need to mount a volume like this example:

	docker run --name secapps-driver --rm -v /your/folder/:/output websecurify/secapps-driver foundation http://target-to-test/

Once the tool complates execution you will find the reports inside `/your/folder` folder.

# Authentication

In order to use the more specialized tools you need to get your access token from secapps.com. Simply go to your Launchpad and follow the instructions.

# Examples

Start foundation scanner:

	docker run --name secapps-driver --rm websecurify/secapps-driver foundation http://target-to-test/

Start the general purpose scanner:

	docker run --name secapps-driver --rm websecurify/secapps-driver scanner http://target-to-test/ --access-token=your-access-token

Start recon:

	docker run --name secapps-driver --rm websecurify/secapps-driver recon http://target-to-test/ --access-token=your-access-token

Start wpscanner:

	docker run --name secapps-driver --rm websecurify/secapps-driver wpscanner http://target-to-test/ --access-token=your-access-token

# Extending

You can do a lot of cool things with this project. Simply fork and make your own driver.
