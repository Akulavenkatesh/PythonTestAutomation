Feature: Verify the random schedule set scenarios for the Hot Water end point in the boiler module

  @SC-HW-RM01-01 @HotWater @ScheduleTest @6_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM01-01_Set the given 'six' event random schedule with given Hot Water State list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF               |
      | ON                |
      | ON               |
      | OFF                |
      | ON               |
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

  @SC-HW-SH-RM01-02 @HotWater @ScheduleTest @4_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM01-02_Set the given 'four' event random schedule with given Hot Water State list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF               |
      | ON                |
      | OFF               |
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

  @SC-HW-SH-RM01-03 @HotWater @ScheduleTest @2_Event @Random @Verify @All_Client @V6_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM01-03_Set the given 'two' event random schedule with given Hot Water State list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Hot Water State |
      | ON                |
      | OFF               |
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
      
  @SC-HW-RM02-01 @HotWater @ScheduleTest @6_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM02-01_Set the given 'six' event random schedule with given Start Time list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Start Time |
      | 06:30      |
      | 08:30      |
      | 12:00      |
      | 14:00      |
      | 16:30      |
      | 22:00      |
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

  @SC-HW-RM02-02 @HotWater @ScheduleTest @4_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM02-02_Set the given 'four' event random schedule with given Start Time list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Start Time |
      | 06:30      |
      | 08:30      |
      | 12:00      |
      | 14:00      |
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

  @SC-HW-RM02-03 @HotWater @ScheduleTest @2_Event @Random @Verify @V6_Client @All_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM02-03_Set the given 'two' event random schedule with given Start Time list for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Start Time |
      | 16:30      |
      | 22:00      |
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

  @SC-HW-RM03 @HotWater @ScheduleTest @6_Event @Random @Verify @All_Client @V6_App @WholeWeek
  Scenario Outline: SC-HW-SH-RM03_Set the 'six, four or two' event random schedule for the given day of the week and verify the same for Hot Water
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
