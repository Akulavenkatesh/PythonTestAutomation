Feature: Contains all the scenario related to Smart Plugs

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
    
    
      @SC-SP-SH02-02 @SmartPlug @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-SP-SH02-02_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State |
      | 06:30      | ON              |
      | 08:30      | OFF             |
      | 12:00      | OFF             |
      | 14:00      | OFF             |
      | 16:00      | ON              |
      | 21:30      | OFF             |
    Then Verify if the Schedule is set

    Examples: 
      |Device  | Day   | 
      |SLP2_1 | Today |
      

      
    @SC-SP-SH02-03 @SmartPlug @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-SP-SH02-03_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
       | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      |Device  | Day   | 
      |SLP2_1 | Today |