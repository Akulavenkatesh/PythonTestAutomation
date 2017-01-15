Feature: Contains Miscilaniuos scenarios

  Scenario Outline: SC-MS01_Validate Login & Logout functionality
    Given The Hive product is paired and setup for Central Heating with API Validation
    When User Login to the Client with <UserName> and <Password>
    Then Validate if user is Loged in
    When User Logout of the Client
    Then Validate if user is Logged out

    Examples: 
      | UserName | Password  |
      | auto1_V6 | password1 |

@Test_Batch
  Scenario Outline: SC-MS01_Validate Login & Logout functionality
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client

    Examples: 
      | UserName | Password  |
      | auto1_V6 | password1 |
