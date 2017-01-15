Feature: Validate the schedules for the hot water end point in the boiler module

  @SC-HW-SH10-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-HW-SH10-01_Set the given customized 'six' event schedule for all day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 06:30      |
      | ON              | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:30      |
      | ON              | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH10-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-HW-SH10-02_Set the given customized 'four' event schedule for all day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH10-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App @WholeWeek 
  Scenario Outline: SC-HW-SH10-03_Set the given customized 'two' event schedule for all day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH11-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-HW-SH11-01_Set the 'six' event random schedule for all days of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When 6 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH11-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-HW-SH11-02_Set the 'four' event random schedule for all days of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When 4 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH11-01 @HotWater @ScheduleTest @2_Event @Verify @V6_Client @V6_App @WholeWeek 
  Scenario Outline: SC-HW-SH11-03_Set the 'two' event random schedule for all days of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When 2 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-HW-SH12 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-HW-SH12_Set the 'six, four or two' event random schedule for all days of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Any event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples: 
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |
