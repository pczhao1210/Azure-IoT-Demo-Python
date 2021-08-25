import json, random, string
from functions import print_twin, print_device_info, print_query_result, print_device_info_short
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, QuerySpecification, Twin, TwinProperties, CloudToDeviceMethodResult

connection_str = "{Your-Hub-Connection-String}"

device_id = "{Your-Device-ID-Here}"

task_selection = int(input(
    "Please choose your task: \n"
    "1. IoT Hub Operations \n"
    "2. Demo Device Operations \n"
    ))

if task_selection == 1:
    hub_option = int(input(
        "IoT Hub Operations: \n"
        "1. Show IoT Hub Status \n"
        "2. Get All Device Twin \n"
        "3. Create a Device \n"
        "4. Delete a Device \n"
        ))
    if hub_option == 1: # Show IoT Hub Status
        try:
            # Create IoTHubRegistryManager
            registry_manager = IoTHubRegistryManager(connection_str)

            # Get devices
            max_number_of_devices = 10
            devices = registry_manager.get_devices(max_number_of_devices)
            if devices:
                x = 0
                for d in devices:
                    print_device_info_short("Get devices {0}".format(x), d)
                    x += 1
            else:
                print("No device found")
            
            # GetStatistics
            service_statistics = registry_manager.get_service_statistics()
            print("Service Statistics:")
            print(
                "Total connected device count             : {0}".format(
                    service_statistics.connected_device_count
                )
            )
            print("")

            registry_statistics = registry_manager.get_device_registry_statistics()
            print("Device Registry Statistics:")
            print(
                "Total device count                       : {0}".format(
                    registry_statistics.total_device_count
                )
            )
            print(
                "Enabled device count                     : {0}".format(
                    registry_statistics.enabled_device_count
                )
            )
            print(
                "Disabled device count                    : {0}".format(
                    registry_statistics.disabled_device_count
                )
            )
            print("")

        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_statistics stopped")

    if hub_option == 2: # Get All Device Twin
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)

            query_specification = QuerySpecification(query="SELECT * FROM devices")

            # Get specified number of devices (in this case 4)
            #query_result0 = iothub_registry_manager.query_iot_hub(query_specification, None, 4)
            #print_query_result("Query 4 device twins", query_result0)

            # Get all device twins using query
            query_result1 = iothub_registry_manager.query_iot_hub(query_specification)
            print_query_result("Query all device twins", query_result1)

            # Paging... Get more devices (over 1000)
            continuation_token = query_result1.continuation_token
            if continuation_token:
                query_result2 = iothub_registry_manager.query_iot_hub(
                    query_specification, continuation_token
                )
                print_query_result("Query all device twins - continued", query_result2)


        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")    

    if hub_option == 3: # Create a Device
        create_device = input("Please Input the Device ID to be Created: ")
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)

            # Create a device
            primary_key = ''.join(random.sample(string.ascii_letters + string.digits, 44))
            secondary_key = ''.join(random.sample(string.ascii_letters + string.digits, 44))
            device_state = "enabled"
            new_device = iothub_registry_manager.create_device_with_sas(
                create_device, primary_key, secondary_key, device_state
            )
            print_device_info("create_device", new_device)
        
        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped") 

    if hub_option == 4: # Delete a Device
        delete_device_id = input("Please Input the Device ID to be Deleted: ")
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)

            # Delete the device
            remove_device = iothub_registry_manager.delete_device(delete_device_id)
            
            print("Remove Device "+ delete_device_id + " Successfully")
        
        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped") 

if task_selection == 2: # Demo Device Operations

    defined_device_option = int(input(
        "Demo Device Operations: \n"
        "1. Get Device Information \n"
        "2. Get Device Twin \n"
        "3. Set Telemetry Inverval \n"
        "4. Set Send_Data Switch \n"
        "5. Revoke a Direct Method on Device \n"
        "6. Send a C2D Message on Device \n"
        ))

    if defined_device_option == 1: # Get Device Info
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)

            # Get device information
            device = iothub_registry_manager.get_device(device_id)
            print_device_info("Device Twin Infomation is: \n", device)

        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")

    if defined_device_option == 2: # Get Device Twin
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)

            # Get device twin
            twin = iothub_registry_manager.get_twin(device_id)
            print_twin("The Twin Informations is: \n", twin)
            print("")  

        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")
      
    if defined_device_option == 3: # Set Telemetry Interval
        defined_telemetry_value = int(input(
        "1. 5 seconds \n"
        "2. 10 seconds \n"
        "3. 20 seconds \n"
        "4. Input your Value \n"
        ))
        if defined_telemetry_value == 1: telemetry_interval_value = 5
        if defined_telemetry_value == 2: telemetry_interval_value = 10
        if defined_telemetry_value == 3: telemetry_interval_value = 20
        if defined_telemetry_value == 4: telemetry_interval_value = defined_device_option       
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)
            twin = iothub_registry_manager.get_twin(device_id)

            # Update twin
            twin_patch = Twin()
            twin_patch = twin
            twin_patch.properties = TwinProperties(desired={"Telemetry_Interval": telemetry_interval_value})
            updated_twin = iothub_registry_manager.update_twin(device_id, twin_patch, twin.etag)
            print("Set Telemetry Interval to: " + str(telemetry_interval_value) + "\n", updated_twin)
            print("")
        
        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")
            
    if defined_device_option == 4: # Set Send_Data Switch  
        defined_Send_Data_value = int(input(
        "1. Set Send_Data ON \n"
        "2. Set Send Data OFF \n"
        ))

        if defined_Send_Data_value == 1: send_data_value = True
        if defined_Send_Data_value == 2: send_data_value = False
     
        try:
            # Create IoTHubRegistryManager
            iothub_registry_manager = IoTHubRegistryManager(connection_str)
            twin = iothub_registry_manager.get_twin(device_id)

            # Update twin
            twin_patch = Twin()
            twin_patch = twin
            twin_patch.properties = TwinProperties(desired={"Send_Data": send_data_value})
            updated_twin = iothub_registry_manager.update_twin(device_id, twin_patch, twin.etag)
            print("Set Send_Data Switch to: " + str(send_data_value) + "\n", updated_twin)
            print("")
        
        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")

    if defined_device_option == 5: # Revoke Method
        try:
            method_selection = int(input(
                "Please Choose a Method: \n"
                "1. Get Firmware Info \n"
                "2. Get Send_Data Swith Status \n"
                "3. Firmware Update \n"
                "4. Other Mehod \n"
                ))
            if method_selection ==1: 
                method_name = "Get_FW_info"
                method_payload = "{}"
            if method_selection ==2: 
                method_name = "Get_Send_Data_info"
                method_payload = "{}"
            if method_selection ==3: 
                firmware_version_set = float(input("Please Set a Firmware Version: "))
                method_name = "FW_Update"
                method_payload = firmware_version_set
            if method_selection ==4: 
                method_name = "Other_Method"
                method_payload = "{}"        
            
            registry_manager = IoTHubRegistryManager(connection_str)

            deviceMethod = CloudToDeviceMethod(method_name=method_name, payload=method_payload)
            method_response = registry_manager.invoke_device_method(device_id, deviceMethod)
            print(method_response)


        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_registry_manager_sample stopped")

    if defined_device_option == 6: # Send C2D Message
        try:
            send_message = input("Please input a message send to Device: ")
            # Create IoTHubRegistryManager
            registry_manager = IoTHubRegistryManager(connection_str)
            #print("Conn String: {0}".format(connection_str))

            # Send Message To Device
            registry_manager.send_c2d_message(device_id, send_message)
            print("Successfully Sent Message: " + str(send_message))

        except Exception as ex:
            print("Unexpected error {0}".format(ex))
        except KeyboardInterrupt:
            print("iothub_statistics stopped")