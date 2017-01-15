Feature: Contains all the Regression scenarios for Smart Plugs testing

  @SC-AL-RG01 @ActiveLight @Telegesis
  Scenario Outline: SC-AL-03_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The telegesis is paired with given devices
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values for <TIme Duration  in minutes> via telegesis
      | BrightnessValue | TimeLapse |
      | ON              | 1         |
      | 20              | 1         |
      | 00              | 1         |
      | 40              | 1         |
      | 00              | 1         |
      | 60              | 1         |
      | 00              | 1         |
      | 80              | 1         |
      | 00              | 1         |
      | 100             | 1         |
      | OFF             | 1         |

    Examples: 
      | TIme Duration  in minutes |
      | 1                        |

  @SC-AL-RG02 @ActiveLight @API
  Scenario: SC-AL-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
    Given The Active Lights are paired with the Hive Hub
    When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via Hub
      | BrightnessValue |
      | 0               |
      | 20              |
      | 0               |
      | 40              |
      | 0               |
      | 60              |
      | 0               |
      | 80              |
      | 0               |
      | 100             |

  @SC-AL-RGSH01-01 @ActiveLight @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-AL-SH01-01_Set the given default 'six' event schedule for the given day and verify the same for Active Light
    Given The Active Light are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State | Brightness |
      | 06:30      | ON              | 70         |
      | 08:30      | OFF             | 100        |
      | 12:00      | ON              | 50         |
      | 14:00      | OFF             | 90         |
      | 16:00      | ON              | 100        |
      | 21:30      | OFF             | 0          |
    Then Verify if the Schedule is set

    Examples: 
      | Device     | Day   |
      | FWBulb01_1 | Today |
