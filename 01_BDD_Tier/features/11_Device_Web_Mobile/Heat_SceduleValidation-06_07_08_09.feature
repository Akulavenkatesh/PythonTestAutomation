Feature: Verify the schedules for the central heating end point in the boiler module

  @SC-CH-SH06-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH06-01_Set the given 'six' event schedule with 'two' consicutive 'frost' Target Temperature for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 30.0               | 16:30      |
      | 23.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH06-02_Set the given 'four' event schedule with 'two' consicutive 'frost' Target Temperature for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 30.0               | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH06-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-CH-SH06-03_Set the given 'two' event schedule with 'two' consicutive 'frost' Target Temperature for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH07-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH07-01_Set the given 'six' event schedule with 'all' Target Temperature as 'frost' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 1.0                | 16:30      |
      | 1.0                | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH07-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH07-02_Set the given 'four' event schedule with 'all' Target Temperature as 'frost' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH07-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-CH-SH07-03_Set the given 'two' event schedule with 'all' Target Temperature as 'frost' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 08:30      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH08-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH08-01_Set the given 'six' event schedule with 'two' consicutive Target Temperature 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 1.0                | 08:30      |
      | 30.0               | 12:00      |
      | 31.0               | 14:00      |
      | 1.0                | 16:30      |
      | 23.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH08-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH08-02_Set the given 'four' event schedule with 'two' consicutive Target Temperature 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 08:30      |
      | 30.0               | 12:00      |
      | 31.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH08-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-CH-SH08-03_Set the given 'two' event schedule with 'two' consicutive Target Temperature 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 30.0               | 12:00      |
      | 31.0               | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH09-01_Set the given 'six' event schedule with 'all' Target Temperature 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 31.0               | 06:30      |
      | 32.0               | 08:30      |
      | 29.0               | 12:00      |
      | 28.0               | 14:00      |
      | 30.0               | 16:30      |
      | 31.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH09-02_Set the given 'four' event schedule with 'all' Target Temperature 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 32.0               | 08:30      |
      | 29.0               | 12:00      |
      | 28.0               | 14:00      |
      | 30.0               | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH09-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-CH-SH09-03_Set the given 'two' event schedule with 'all' Target Temperature as 'greater than Room Temperature' for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 32.0               | 08:30      |
      | 31.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |
