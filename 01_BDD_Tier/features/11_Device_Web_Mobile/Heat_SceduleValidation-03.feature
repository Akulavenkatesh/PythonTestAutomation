Feature: Validate the schedules for the central heating end point in the boiler module

  @SC-CH-SH03-01 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-01_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 21.0               |
      | 29.0               |
      | 1.0                |
      | 31.0               |
      | 1.0                |
      | 15.0               |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-02 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-02_Set the given 'six' event schedule with target temperature of 'all' events as 'Frost' and 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 1.0                |
      | 1.0                |
      | 1.0                |
      | 1.0                |
      | 1.0                |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-03 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-03_Set the given 'six' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The schedule for below 'Target Temperature' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Target Temperature |
      | 21.0               |
      | 29.0               |
      | 1.0                |
      | 31.0               |
      | 1.0                |
      | 15.0               |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | Third          |
      | Today | Fifth          |

  @SC-CH-SH03-04 @Heating @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-04_Set the given 'four' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 29.0               |
      | 1.0                |
      | 31.0               |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-05 @Heating @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-05_Set the given 'four' event schedule with target temperature of 'all' events as 'Frost' and 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 1.0                |
      | 1.0                |
      | 1.0                |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-06 @Heating @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-CH-SH03-06_Set the given 'four' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The schedule for below 'Target Temperature' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Target Temperature |
      | 29.0               |
      | 1.0                |
      | 31.0               |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |
      | Today | Third          |
      | Today | Fourth         |

  @SC-CH-SH03-07 @Heating @ScheduleTest @2_Event @Validate @All_Client @V6_App 
  Scenario Outline: SC-CH-SH03-07_Set the given 'two' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 29.0               |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-08 @Heating @ScheduleTest @2_Event @Validate @All_Client @V6_App
  Scenario Outline: SC-CH-SH03-08_Set the given 'two' event schedule with target temperature of 'all' events as 'Frost' and 15 minutes time difference between events for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature |
      | 1.0                |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH03-09 @Heating @ScheduleTest @2_Event @Validate @All_Client @V6_App
  Scenario Outline: SC-CH-SH03-09_Set the given 'two' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The schedule for below 'Target Temperature' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Target Temperature |
      | 31.0               |
      | 1.0                |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |

  @ScheduleTest_Heat77
  Scenario Outline: SC-CH-SH-RM02-01_Set the given 'six' event random schedule with given Start Time list for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Random schedule is generated and set for <Day> on the Client
      | Start Time |
      | 06:30      |
      | 08:30      |
      | 12:00      |
      | 14:00      |
      | 16:30      |
      | 22:00      |
    Then Validate the schedule that is set

    Examples: 
      | Day |
      | fri |
