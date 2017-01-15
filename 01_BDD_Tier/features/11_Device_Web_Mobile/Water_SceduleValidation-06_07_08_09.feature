Feature: Verify the schedules for the Hot Water and hot water end points in the boiler module

  @SC-CH-SH06-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH06-01_Set the given 'six' event schedule with 'two' consicutive 'OFF' Hot Water State for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | ON              | 14:00      |
      | OFF             | 16:30      |
      | OFF             | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH06-02_Set the given 'four' event schedule with 'two' consicutive 'OFF' Hot Water State for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-HW-SH06-03_Set the given 'two' event schedule with 'two' consicutive 'OFF' Hot Water State for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-HW-SH07-01_Set the given 'six' event schedule with 'all' Hot Water State as 'OFF' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | OFF             | 16:30      |
      | OFF             | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH07-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH07-02_Set the given 'four' event schedule with 'all' Hot Water State as 'OFF' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH07-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-HW-SH07-03_Set the given 'two' event schedule with 'all' Hot Water State as 'OFF' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 08:30      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH08-01_Set the given 'six' event schedule with 'two' consicutive Hot Water State 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | ON              | 08:30      |
      | OFF             | 12:00      |
      | ON              | 14:00      |
      | ON              | 16:30      |
      | OFF             | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH08-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH08-02_Set the given 'four' event schedule with 'two' consicutive Hot Water State 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 08:30      |
      | ON              | 12:00      |
      | ON              | 14:00      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH08-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-HW-SH08-03_Set the given 'two' event schedule with 'two' consicutive Hot Water State 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 12:00      |
      | ON              | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH09-01_Set the given 'six' event schedule with 'all' Hot Water State 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | ON              | 08:30      |
      | ON              | 12:00      |
      | ON              | 14:00      |
      | ON              | 16:30      |
      | ON              | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH09-02_Set the given 'four' event schedule with 'all' Hot Water State 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | ON              | 12:00      |
      | ON              | 14:00      |
      | ON              | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-HW-SH09-03_Set the given 'two' event schedule with 'all' Hot Water State as 'ON' for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | ON              | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |
