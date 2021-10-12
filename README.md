# MqttInfluxDBBridge
Python based Mqtt to InfluxDB Bridge 

The script was created for a test setup, where I needed to build a simple bridge between a mqtt broker and an InfluxDb

As a convention I used the following topic naming convention:

[location name]\\[device name]\\[identifier]\\[value name]

This results in a InfluxDB insert as 

host = [device name]
\_field name = [identifier].[value name]
\_field value = float(payload)

The location can be used to adjust for pyhical locatons 

example:
	
	home/controller/relais/pump = 1 

	results in:
	
		host = controller
		field name = relais.pump
		field payload = float(1)

All the credentials and path, mqtt clientID ect. are configured through Environment variabls
This makes it easier to use the script for multiple locations. Or as  I use it, 
in multiple docker containers.  In combination with environment files and a docker-compose file.

The program isn't pretty, but it works quite well. 
Maybe someone can also use it in any case feel free to do so.

Regards
Matijs
