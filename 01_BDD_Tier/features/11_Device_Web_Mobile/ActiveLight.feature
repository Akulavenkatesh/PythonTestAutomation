Feature: Contains the scenario to test the Active Light

  @SC-AL-01 @ActiveLight
  Scenario: SC-AL-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The Active Lights are paired with the Hive Hub
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via Hub
      | BrightnessValue |
      |               0 |
      |              20 |
      |               0 |
      |              40 |
      |               0 |
      |              60 |
      |               0 |
      |              80 |
      |               0 |
      |             100 |

  @SC-AL-01-01 @ActiveLight
  Scenario Outline: SC-AL-01-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The Active Lights are paired with the Hive Hub
    When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via Hub
      | BrightnessValue |
      |               0 |
      |              20 |
      |               0 |
      |              40 |
      |               0 |
      |              60 |
      |               0 |
      |              80 |
      |               0 |
      |             100 |

    Examples: 
      | ActiveLightDevice |
      | FWBulb01US_1      |

  @SC-AL-04-01 @ActiveLight
  Scenario Outline: SC-AL-04-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The Active Lights are paired with the Hive Hub
    When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied and validated for <TimePeriod> for the below brightness values infinitely via Hub
      | BrightnessValue |
      |              40 |
      |              60 |
      |              80 |
      |             100 |

    Examples: 
      | ActiveLightDevice | TimePeriod |
      | FWBulb01_1        |        120 |

  @SC-AL-02 @ActiveLight
  Scenario: SC-AL-02_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The telegesis is paired with given devices
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via telegesis
      | BrightnessValue | TimeLapse |
      |              00 |         1 |
      |              25 |         1 |
      |              00 |         1 |
      |              50 |         1 |
      |              00 |         1 |
      |              75 |         1 |
      |              00 |         1 |
      |              99 |         1 |
      |              00 |         1 |

  @SC-AL-03 @ActiveLight
  Scenario: SC-AL-03_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The telegesis is paired with given devices
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values for infinitely via telegesis
      | BrightnessValue | TimeLapse |
      | ON              |         1 |
      |              00 |         1 |
      |              20 |         1 |
      |              00 |         1 |
      |              40 |         1 |
      |              00 |         1 |
      |              60 |         1 |
      |              00 |         1 |
      |              80 |         1 |
      |              00 |         1 |
      |             100 |         1 |
      | OFF             |         1 |

	@SC-AL-04 @ActiveLight
  Scenario: SC-AL-04_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The telegesis is paired with given devices
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied to 50 and validated infinitely with timelapse of 1 second via telegesis
      
  @SC-AL-SH01-01 @ActiveLight @ScheduleTestAPI @6_Event @Verify @APITest
  Scenario Outline: SC-AL-SH01-01_Set the given default 'six' event schedule for the given day and verify the same for Active Light
    Given The Active Light are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State | Brightness |
      | 06:30      | ON              |         70 |
      | 08:30      | OFF             |        100 |
      | 12:00      | ON              |         50 |
      | 14:00      | OFF             |         90 |
      | 16:00      | ON              |        100 |
      | 21:30      | OFF             |          0 |
    Then Verify if the Schedule is set

    Examples: 
      | Device       | Day   |
      | FWBulb01US_1 | Today |

  @SC-AL-SH01-02 @ActiveLight @ScheduleTestAPI @6_Event @Verify @APITest @Tunable
  Scenario Outline: SC-AL-SH01-02_Set the given default 'six' event schedule for the given day and verify the same for Active Light
    Given The Active Light are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State | Brightness |
      | 06:30      | ON              |         70 |
      | 08:30      | OFF             |        100 |
      | 12:00      | ON              |         50 |
      | 14:00      | OFF             |         90 |
      | 16:00      | ON              |        100 |
      | 21:30      | OFF             |          0 |
    Then Verify if the Schedule is set
    And Validate if the Schedule is set for the whole week on the <Device>

    Examples: 
      | Device       | Day   |
      | TWBulb01US_1 | Today |

  @SC-AL-SHW01-01 @ActiveLight @ScheduleTest @Week @Validate @APITest
  Scenario Outline: SC-CH-SH01-01_Set the given custom schedule for the whole week and verify the same for Active Light
    Given The Active Light are paired with the Hive Hub
    When The below schedule is set for the whole week on the <Device> via Hub API
      | Day | Event1       | Event2       | Event3       | Event4       | Event5       | Event6      |
      | Mon | 06:30,ON,100 | 08:30,OFF,20 | 10:30,ON,100 | 13:00,OFF,10 | 15:30,ON,70  | 22:30,OFF,0 |
      | Tue | 06:30,ON,16  | 08:30,OFF,29 | 10:30,ON,10  | 13:00,OFF,90 | 15:30,ON,100 | 22:30,OFF,0 |
      | Wed | 00:30,ON,17  | 04:30,OFF,30 | 10:45,ON,1   | 13:00,OFF,0  |              |             |
      | Thu | 15:30,ON,18  | 18:30,OFF,31 | 20:30,ON,1   | 23:00,OFF,8  | 23:30,ON,40  | 23:45,OFF,0 |
      | Fri | 06:30,ON,19  | 08:30,OFF,32 |              |              |              |             |
      | Sat | 06:30,ON,20  | 08:30,OFF,28 | 10:30,ON,1   | 13:00,OFF,07 | 15:30,ON,30  | 22:30,OFF,0 |
      | Sun | 12:30,ON,14  | 15:30,OFF,0  | 19:15,OFF,0  | 20:00,ON,6   | 22:30,ON,31  | 23:30,OFF,0 |
    Then Verify if the Schedule is set
    Then Validate if the Schedule is set for the whole week on the <Device>

    Examples: 
      | Device     |
      | FWBulb01_1 |

  @SC-AL-SHW01-02 @ActiveLight @ScheduleTest @Week @Validate @APITest
  Scenario Outline: SC-CH-SH01-02_Set the given custom schedule for the whole week and verify the same for Active Light
    Given The Active Light are paired with the Hive Hub
    When The below schedule is set for the whole week on the <Device> via Hub API
      | Day | Event1       | Event2       | Event3       | Event4       | Event5       | Event6      |
      | Mon | 06:30,ON,100 | 08:30,OFF,20 | 10:30,ON,100 | 13:00,OFF,10 | 15:30,ON,70  | 22:30,OFF,0 |
      | Tue | 06:30,ON,16  | 08:30,OFF,29 | 10:30,ON,10  | 13:00,OFF,90 | 15:30,ON,100 | 22:30,OFF,0 |
      | Wed | 00:30,ON,17  | 04:30,OFF,30 | 10:45,ON,1   | 13:00,OFF,0  |              |             |
      | Thu | 15:30,ON,18  | 18:30,OFF,31 | 20:30,ON,1   | 23:00,OFF,8  | 23:30,ON,40  | 23:45,OFF,0 |
      | Fri | 06:30,ON,19  | 08:30,OFF,32 |              |              |              |             |
      | Sat | 06:30,ON,20  | 08:30,OFF,28 | 10:30,ON,1   | 13:00,OFF,07 | 15:30,ON,30  | 22:30,OFF,0 |
      | Sun | 22:15,ON,100 | 22:30,OFF,0  | 22:45,ON,100 | 23:00,OFF,6  | 23:15,ON,31  | 23:30,ON,70 |
    Then Validate if the Schedule is set for the whole week on the <Device>

    Examples: 
      | Device     |
      | FWBulb01_1 |

  @SC-AL-CL-01 @RGB
  Scenario: SC-AL-CL-01_Switch between colors in a RGB Bulb by changing the Hue
    Given The telegesis is paired with given devices
    When The hue value of the bulb is changed and validated for the given hue value infinitely via telegesis
      | HueValue | TimeLapse |
      | 00       |         1 |
      |       01 |         1 |
      |       21 |         1 |
      |       31 |         1 |
      |       41 |         1 |
      |       51 |         1 |
      |       61 |         1 |
      |       71 |         1 |
      |       81 |         1 |
      |       91 |         1 |
      | A1       |         1 |
