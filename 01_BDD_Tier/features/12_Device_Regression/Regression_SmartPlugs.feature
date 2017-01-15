Feature: Contains all the Regression scenarios for Smart Plugs testing

  @SC-SP-SH01-01 @SmartPlug
  Scenario: SC-SP-SH01-01_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_1						| 96             |
    
     @SC-SP-SH01-02 @SmartPlug
  Scenario: SC-SP-SH01-02_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_2					| 8             |
    
    
     @SC-SP-SH01-03 @SmartPlug
  Scenario: SC-SP-SH01-03_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_3					| 48             |
    
    
     @SC-SP-SH01-04 @SmartPlug
  Scenario: SC-SP-SH01-04_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_4					| 2             |
    
    
     @SC-SP-SH01-05 @SmartPlug
  Scenario: SC-SP-SH01-05_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_5					| 4             |
    
    
      @SC-SP-SH02-01 @SmartPlug @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-SP-SH02-01_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below schedule is set for <Day> via Hub
      | Start Time | SmartPlug State |
      | 06:30      | ON              |
      | 08:30      | OFF             |
      | 12:00      | OFF             |
      | 14:00      | OFF             |
      | 16:00      | ON              |
      | 21:30      | OFF             |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |
      
        @SC-SP-FT01-01 @Regression @SmartPlug @Hub
  Scenario: SC-SP-FT01-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | 02095120       | NA             |
      | SP         | SLP2       | NA             | 02115120       |
      
        @SC-SP-FT02-01 @Regression @SmartPlug @Telegisis
  Scenario: SC-SP-FT02-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | 1.08           | NA             |
      | SP         | SLP2       | 2.08           | NA             |
      | SB         | SLB1       | NA             | 1.09           |
      | SP         | SLP2       | NA             | 2.09           |
      
      
     # behave --tags=Regression --tags=SmartPlug --tags=Hub
      #behave --tags=Regression --tags=SmartPlug --tags=Telegisis