#Created on 16 July 2016
#@authors:
#iOS        - rajeshwaran
#Android    - TBD
#Web        - TBD
Feature: Validate the functionalities of Motion Sensors

  @MotionSensorBasics
  Scenario Outline: SC-MS-MC01_Validate the basic operations for Motion Sensor
    Given The <Motion Sensor> is paired with the hub
    When User navigates to the <Motion Sensor> screen in the Client
    Then Validate the current status of the <Motion Sensor>
    When User navigates to the event logs in the Client
    Then Validate the motion event logs are displayed
    When User views <NumberOf> days back in the event logs in the Client
    Then Validate the motion event logs are displayed
    When User navigates to the Recipes of the motion sensor in the Client
    Then Validate the current status of Recipes of the <Motion Sensor>

    Examples: 
      | Motion Sensor | NumberOf |
      | Motion Sensor |        3 |
