# Azure-IoT-Hub-Demo-Python
## A full functional Azure IoT Hub Device Simulator and Controller
An Azure IoT Hub Demo Script with Python

From samples from azure-iot-sdk-python, make a combined script for both device client and service client.

## Changelog:
##### 20210811：Optimize the Device Twin retrival function to allow registered device with no Device Twin run this application with no error
##### 20200407: Adding DPS function while connecting
##### 20201013: Adding new simulator competible with Azure IoT Python SDK 2.3.0, replace some deprecated API with latest one

## Simulated Device (IoT SDK)

Before Start: 
#### Using Connection String from IoT Hub
1. Run following command in Command Line Tool, such as Windows Terminal:
```
      pip install -r requirements.txt
```
2. Replace your DEVICE connection string to conn_str
3. Add following desired properties in the device twin, properties, desired. 
```
      "Telemetry_Interval":10,
      "Send_Data":true,
```
And it looks like this:
```
     "properties": {
        "desired": {
          "Telemetry_Interval": 10,
          "Send_Data": true,
          "$metadata": {
               ......
          }
         },
```

#### Using Device Provisioning Service to Connect (This can be also used with IoT Central)
1. Uncomment the DPS part and comment the connection string part
2. Replace your: </br>
    id_scope: # can be found on your dps frontpage </br>
    registration_id: # define yourself one if using group enrollment or set one uesing individual enrollment </br>
    symmetric_key: # provisioning master key </br>
3. Edit the Initial Device Twin State like this:
```
{
  "tags": {},
  "properties": {
    "desired": {
      "Telemetry_Interval": 10,
      "Send_Data": true
    }
  }
}
```

#### Device Client D2C Message
For device client, will generate a message to Azure IoT Hub with random data in this format: </br>
{"Voltage":random_voltage, "Ampere":random_ampere, "Walt":random_walt} </br>

And when walt reach some point, a custom property will be add to this message and send to IoT Hub.

#### Device Twin  
2 pre-defined twin properties are:
- Telemetry_Interval：{int}
- Send_Data: {bool}

#### Method
Some pre-defined method listed below, and after execute them, a response will send back to IoT Hub:
- Get_FW_info : report firmware info from local environment
- Get_Send_Data_info: report if the device is sending message to cloud
- FW_Update: trigger local simulate firmware update process, for OTA tutorial, please find [here](https://docs.microsoft.com/en-us/azure/iot-hub/tutorial-firmware-update)
- Other Method: report unkown

#### C2D Message
Also, when receive C2D message, will display on output.

## Simulated Control Service (IoT Hub Controller with Service SDK)

Before Start, replace your IOT HUB connection String to connection_str, and put your device id in device_id.

For Service client, use menu selection mode to perform operations:
- IoT Hub Operations
  1. Show IoT Hub Status: show all device connection status and summary
  2. Get All Device Twin: show all device twin
  3. Create a Device: will create a device with your input device id and random generated key
  4. Delete a Device: Delete a device with your input device id
- Demo Device Operations
  1. Get Device Information
  2. Get Device Twin
  3. Set Telemetry Inverval: choose a interval in seconds or input
  4. Set Send_Data Switch
  5. Revoke a Direct Method on Device
  6. Send a C2D Message on Device
  
 ## Summary
 By using this script to have a basic learning of how a device commucate to Azure IoT Hub, get more infomation at [Here](https://docs.microsoft.com/en-us/azure/iot-hub/)

