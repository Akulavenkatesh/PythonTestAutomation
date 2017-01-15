Feature: Validate the various mode changes for Hot Water

   @BasicSmokeTest  @SC-HW-MC01 @HotWater @ModeTest @All_Client @V6_App @NGD
  Scenario Outline: SC-HW-MC01_Validate the Mode change for Hot Water on the Boiler Module
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF

    Examples: 
      | Duration | CheckInterval |
      | 120      | 20            |

  @ModeTest_Water1
  Scenario Outline: SC-HW-MC01_Validate the Mode change for Hot Water on the Boiler Module
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to BOOST_CANCEL on the Client
    Then Automatically validate current mode as Always OFF

    Examples: 
      | Duration | CheckInterval |
      | 9        | 3             |

   @SC-HW-MC01-01
  Scenario Outline: SC-HW-MC01_Validate the Mode change for Hot Water on the Boiler Module
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON

    Examples: 
      | Duration | CheckInterval |
      | 120      | 20            |
