Feature: Verify the random schedule set scenarios for the central heating end point in the boiler module

  @SC-CH-RM01-01 @Heating @ScheduleTest @6_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM01-01_Set the given 'six' event random schedule with given Target Temperature list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Target Temperature |
      | 21.0               |
      | 29.0               |
      | 1.0                |
      | 15.0               |
      | 1.0                |
      | 15.0               |
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

  @SC-CH-RM01-02 @Heating @ScheduleTest @4_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM01-02_Set the given 'four' event random schedule with given Target Temperature list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Target Temperature |
      | 21.0               |
      | 29.0               |
      | 1.0                |
      | 15.0               |
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

  @SC-CH-RM01-03 @Heating @ScheduleTest @2_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM01-03_Set the given 'two' event random schedule with given Target Temperature list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Below event Random schedule is generated and set for <Day> on the Client
      | Target Temperature |
      | 1.0                |
      | 31.0               |
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
      
  @SC-CH-RM02-01 @Heating @ScheduleTest @6_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM02-01_Set the given 'six' event random schedule with given Start Time list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-RM02-02 @Heating @ScheduleTest @4_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM02-02_Set the given 'four' event random schedule with given Start Time list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-RM02-03 @Heating @ScheduleTest @2_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM02-03_Set the given 'two' event random schedule with given Start Time list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-RM03 @Heating @ScheduleTest @6_Event @Random @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH-RM03_Set the 'six, four or two' event random schedule for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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
