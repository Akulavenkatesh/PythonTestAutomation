Feature: Validate the schedules for the Hot Water end point in the boiler module

  @SC-HW-SH03-01 @HotWater @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-01_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | OFF             |
      | ON              |
      | OFF             |
      | ON              |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-02 @HotWater @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-02_Set the given 'six' event schedule with Hot Water State of 'all' events as 'OFF' and 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | OFF             |
      | OFF             |
      | OFF             |
      | OFF             |
      | OFF             |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-03 @HotWater @ScheduleTest @6_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-03_Set the given 'six' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The schedule for below 'Hot Water State' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Hot Water State |
      | OFF             |
      | ON              |
      | OFF             |
      | ON              |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |
      | Today | Third          |
      | Today | Fourth         |
      | Today | Fifth          |
      | Today | Sixth          |

  @SC-HW-SH03-04 @HotWater @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-04_Set the given 'four' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF             |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-05 @HotWater @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-05_Set the given 'four' event schedule with Hot Water State of 'all' events as 'OFF' and 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | OFF             |
      | OFF             |
      | OFF             |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-06 @HotWater @ScheduleTest @4_Event @Validate @All_Client @All_App 
  Scenario Outline: SC-HW-SH03-06_Set the given 'four' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The schedule for below 'Hot Water State' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF             |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |
      | Today | Third          |
      | Today | Fourth         |

  @SC-HW-SH03-07 @HotWater @ScheduleTest @2_Event @Validate @All_Client @V6_App 
  Scenario Outline: SC-HW-SH03-07_Set the given 'two' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-08 @HotWater @ScheduleTest @2_Event @Validate @All_Client @V6_App 
  Scenario Outline: SC-HW-SH03-08_Set the given 'two' event schedule with Hot Water State of 'all' events as 'OFF' and 15 minutes time difference between events for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State |
      | OFF             |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH03-09 @HotWater @ScheduleTest @6_Event @Validate @All_Client @V6_App 
  Scenario Outline: SC-HW-SH03-09_Set the given 'two' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The schedule for below 'Hot Water State' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Hot Water State |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples: 
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |
