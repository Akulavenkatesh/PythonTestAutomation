Feature: Validate the various mode change for Central Heating end point in the Boiler Module

   @BasicSmokeTest @SC-CH-MC01 @Heating @ModeTest @All_Client @V6_App @NGD @V5_User_Negative
  Scenario Outline: SC-CH-MC01_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Target Temperature is automatically set to 20.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to <FirstSetTemperature> on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as <FirstSetTemperature>
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples: 
      | FirstSetTemperature |
      | 27.0                |

  @SC-CH-MC02 @Heating @ModeTest @Device @WebMobile @V6_App @NGD @V5_User_Negative
  Scenario Outline: SC-CH-MC02_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to BOOST with Target Temperature as <Boost Temperature> for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Target Temperature is automatically set to 7.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 7.0

    Examples: 
      | Boost Temperature |
      | 27.0              |

  @SC-CH-MC04 @Heating @ModeTest @Device @WebMobile @V6_App @NGD
  Scenario Outline: SC-CH-MC04_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to BOOST with Target Temperature as <Boost Temperature> for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples: 
      | AutoOverRideTemperature | Boost Temperature |
      | 12.0                    | 27.0              |

  @ModeTest2
  Scenario Outline: SC-CH-MC3_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is manually changed to OFF on the Client
    Then Manually validate current mode as OFF with Target Temperature as 1.0
    When Mode is manually changed to MANUAL on the Client
    Then Manually validate current mode as MANUAL with Target Temperature as 20.0

    Examples: 
      | Boost Temperature |
      | 27.0              |

  @SC-CH-MC05 @Heating @ModeTest @Device @WebMobile @V5_App
  Scenario Outline: SC-CH-MC05_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to <FirstSetTemperature> on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as <FirstSetTemperature>
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to 7.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 7.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples: 
      | FirstSetTemperature |
      | 27.0                |

      
  @SC-CH-MC0Temp @Heating @ModeTest @Device @WebMobile @V5_App
  Scenario Outline: SC-CH-MC05_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Dual Channel with Zigbee Validation
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to HOLIDAY with Target Temperature as <HOLDAY Temperature> for a duration of 300 seconds on the Client
    And Wait for 300 seconds
    Then Automatically validate current mode as HOLIDAY with Target Temperature as <HOLDAY Temperature>
    And Wait for 360 seconds
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0

    Examples: 
      | HOLDAY Temperature |
      | 11.0                |
      
   @SC-CH-MC0Temp1 @Heating @ModeTest @Device @WebMobile @V5_App
  Scenario Outline: SC-CH-MC05_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Dual Channel with ZIgbeeAPI Validation
    When Mode is automatically changed to BOOST with Target Temperature as <Boost Temperature> for a duration of 1 hour on the Client for Heating
    Then Automatically validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Mode is automatically changed to BOOST on the Client for Hot Water
    Then Automatically validate current mode as BOOST

    Examples: 
      | Boost Temperature |
      | 22.0                |
      