Feature: Validate the schedules for the central heating end point in the boiler module

  @SC-CH-SH10-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App @WholeWeek 
  Scenario Outline: SC-CH-SH10-01_Set the given customized 'six' event schedule for all day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
      | 23.0               | 22:00      |
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

  @SC-CH-SH10-01 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH10-02_Set the given customized 'four' event schedule for all day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
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

  @SC-CH-SH10-01 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App @WholeWeek
  Scenario Outline: SC-CH-SH10-03_Set the given customized 'two' event schedule for all day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 16:30      |
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

  @SC-CH-SH11-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH11-01_Set the 'six' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-SH11-01 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App @WholeWeek
  Scenario Outline: SC-CH-SH11-02_Set the 'four' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-SH12-01 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App @WholeWeek
  Scenario Outline: SC-CH-SH11-03_Set the 'two' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
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

  @SC-CH-SH12-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @V6_App @WholeWeek
  Scenario Outline: SC-CH-SH12_Set the 'six, four or two' event random schedule for all days of the week and verify the same for Central Heating
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
