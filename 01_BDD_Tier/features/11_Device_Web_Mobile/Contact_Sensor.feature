Feature: Validate the functionalities of Contact Sensors

    @ContactSensor
    Scenario Outline: Validate the basic operations for Contact Sensor 
    Given The Hive product is paired with hub
    When User redirect to the <ContactSensor> screen on the Client
    Then Verify the current status of the <ContactSensor>
    When Get the response from API for <ContactSensor> for <DeviceType>
    Then User navigates to the event logs in the Client
	When User check <WeekDays> day back in the event logs in the Client
	Then Validate the event logs are displayed
	
    Examples: 
      | ContactSensor   	 |  DeviceType 		|	WeekDays	|
      | Win/door sensor		 |  WDS00140002_1 	|   3 			|	

