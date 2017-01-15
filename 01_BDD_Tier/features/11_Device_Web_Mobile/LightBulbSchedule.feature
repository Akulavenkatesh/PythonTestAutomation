Feature: Verify the schedules for the Light bulbs


@FixedLightBulb @SC_LB_SM01
  Scenario Outline: SC_LB_SM01_Set the default event schedule for all day of the week and verify the same for fixed Light bulb
    Given The Hive product is paired and setup for <LightBulb> 
    When The below schedule for Light bulb is set for <Day> on the client
      | Brightness         | Start Time |
      | 100                | 06:30      |
      | 5                  | 08:30      |
      | 100                | 16:00      |
      | 5                  | 21:30      |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | LightBulb | ActiveLightName |
      | Today	  | FWBulb01  | Warm white light|

@FixedLightBulb @SC_LB_SM02
  Scenario Outline: SC_LB_SM02_Set the given customized 'four' event schedule for all day of the week and verify the same for fixed Light bulb
    Given The Hive product is paired and setup for <LightBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time |
      | 5                  | 06:30      |
      | 30                 | 08:30      |
      | 70                 | 16:00      |
      | 100                | 21:30      |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | LightBulb | ActiveLightName |
      | Today	  | FWBulb01  | Warm white light|
      
      
@FixedLightBulb @SC_LB_SM03
  Scenario Outline: SC_LB_SM03_Set the full brightness event schedule for all day of the week and verify the same for fixed Light bulb
    Given The Hive product is paired and setup for <LightBulb> 
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time |
      | 100                | 06:30      |
      | 100                | 08:30      |
      | 100                | 16:00      |
      | 100                | 21:30      |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | LightBulb | ActiveLightName |
      | Today	  | FWBulb01  | Warm white light|
      
@FixedLightBulb @SC_LB_SM04
  Scenario Outline: SC_LB_SM04_Set the minimum brightness event schedule for all day of the week and verify the same for fixed Light bulb
    Given The Hive product is paired and setup for <LightBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time |
      | 5                  | 06:30      |
      | 5                  | 08:30      |
      | 5                  | 16:00      |
      | 5                  | 21:30      |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | LightBulb | ActiveLightName |
      | Today	  | FWBulb01  | Warm white light|
        
@FixedLightBulb @SC_LB_SM05
  Scenario Outline: SC_LB_SM05_Set the customised brightness and time event schedule for all day of the week and verify the same for fixed Light bulb
    Given The Hive product is paired and setup for <LightBulb> 
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time |
      | 5                  | 09:30      |
      | 20                 | 13:30      |
      | 50                 | 18:30      |
      | 90                 | 21:00      |
      | 60				   | 22:00		|
      | 70				   | 22:30      |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | LightBulb | ActiveLightName |
      | Today	  | FWBulb01  | Warm white light|

 
 @ColourLightBulb  @SC_LB_SM06
  Scenario Outline: SC_LB_SM06_Set the default event schedule for all day of the week and verify the same for colour bulb
    Given The Hive product is paired and setup for <ColourBulb> 
    When The below schedule for Light bulb is set for <Day> on the client
      | Brightness         | Start Time | Target Colour |
      | 100                | 06:30      | Red			|
      | 5                  | 08:30      | Off			|
      | 100                | 16:00      | Red			|
      | 5                  | 21:30      | Off			|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | ColourBulb    | ActiveLightName |
      | Today	  | RGBBulb01UK   | Colour light    |

@ColourLightBulb @SC_LB_SM07
  Scenario Outline: SC_LB_SM07_Set the given customized 'two' event schedule for all day of the week and verify the same for colour bulb
    Given The Hive product is paired and setup for <ColourBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 06:30      |  Blue			|
      | 30                 | 08:30      |  Red			|

      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | ColourBulb    | ActiveLightName |
      | Today	  | RGBBulb01UK   | Colour light    |
      
      
@ColourLightBulb  @SC_LB_SM08
  Scenario Outline: SC_LB_SM08_Set the full brightness event schedule for all day of the week and verify the same for colour bulb
    Given The Hive product is paired and setup for <ColourBulb> 
    When The below schedule is set for <Day> on the Client
    
      | Brightness		   | Start Time | Target Colour |
      | 100                | 06:30      | Red			|
      | 100                | 08:30      | Yellow		|
      | 100                | 16:00      | Green			|
      | 100                | 21:30      | Yellow 		|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | ColourBulb    | ActiveLightName |
      | Today	  | RGBBulb01UK  | Colour light    |
      
@ColourLightBulb @SC_LB_SM09
  Scenario Outline: SC_LB_SM09_Set the minimum brightness event schedule for all day of the week and verify the same for colour bulb
    Given The Hive product is paired and setup for <ColourBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 06:30      | Red			|
      | 5                  | 08:30      | Red			|
      | 5                  | 16:00      | Red			|
      | 5                  | 21:30      | Red			|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | ColourBulb    | ActiveLightName |
      | Today	  | RGBBulb01UK  | Colour light    |
        
@ColourLightBulb @SC_LB_SM10
  Scenario Outline: SC_LB_SM10_Set the customised brightness and time event schedule for all day of the week and verify the same for colour bulb
    Given The Hive product is paired and setup for <ColourBulb> 
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 08:30      | Red			|
      | 20                 | 10:30      | Off			|
      | 50                 | 17:00      | Red			|
      | 90                 | 21:00      | Off			|
      | 60				   | 22:00		| Red			|
      | 70				   | 22:30      | Off			|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | ColourBulb    | ActiveLightName |
      | Today	  | RGBBulb01UK  | Colour light    |
      
      
      
@TuneableLightBulb @SC_LB_SM11
  Scenario Outline: SC_LB_SM11_Set the default event schedule for all day of the week and verify the same for tuneable bulb
    Given The Hive product is paired and setup for <TuneableBulb> 
    When The below schedule for Light bulb is set for <Day> on the client
      | Brightness         | Start Time | Target Colour |
      | 100                | 06:30      | Coolest White	|
      | 5                  | 08:30      | Off			|
      | 100                | 16:00      | Coolest White	|
      | 5                  | 21:30      | Off			|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | TuneableBulb    | ActiveLightName |
      | Today	  | TWBulb01UK    | tuneable light    |

@TuneableLightBulb @SC_LB_SM12
  Scenario Outline: SC_LB_SM12_Set the given customized 'four' event schedule for all day of the week and verify the same for tuneable bulb
    Given The Hive product is paired and setup for <TuneableBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 06:30      |  Coolest White|
      | 30                 | 08:30      |  Off			|
      | 70                 | 16:00      |  Coolest White|
      | 100                | 21:30      |  Off		    |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | TuneableBulb    | ActiveLightName |
      | Today	  | TWBulb01UK   | tuneable light    |
      
      
@TuneableLightBulb @SC_LB_SM13
  Scenario Outline: SC_LB_SM13_Set the full brightness event schedule for all day of the week and verify the same for tuneable bulb
    Given The Hive product is paired and setup for <TuneableBulb> 
    When The below schedule is set for <Day> on the Client
    
      | Brightness		   | Start Time | Target Colour |
      | 100                | 06:30      | Coolest White	|
      | 100                | 08:30      | Off		    |
      | 100                | 16:00      | Coolest White |
      | 100                | 21:30      | Off 		    |
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | TuneableBulb    | ActiveLightName |
      | Today	  | TWBulb01UK   | tuneable light    |
      
@TuneableLightBulb @SC_LB_SM14
  Scenario Outline: @SC_LB_SM14_Set the minimum brightness event schedule for all day of the week and verify the same for tuneable bulb
    Given The Hive product is paired and setup for <TuneableBulb>
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 06:30      | Coolest White	|
      | 5                  | 08:30      | Off			|
      | 5                  | 16:00      | Coolest White	|
      | 5                  | 21:30      | Off			|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | TuneableBulb    | ActiveLightName |
      | Today	  | TWBulb01UK   | tuneable light     |
      
        
@TuneableLightBulb @SC_LB_SM15
  Scenario Outline: SC_LB_SM15_Set the customised brightness and time event schedule for all day of the week and verify the same for tuneable bulb
    Given The Hive product is paired and setup for <TuneableBulb> 
    When The below schedule is set for <Day> on the Client
      | Brightness		   | Start Time | Target Colour |
      | 5                  | 08:30      | Coolest White	|
      | 20                 | 10:30      | Mid White		|
      | 50                 | 17:00      | Warm White	|
      | 90                 | 21:00      | Coolest White	|
      | 60				   | 22:00		| Mid White		|
      | 70				   | 22:30      | Warm White	|
      
    Then Verify if the Schedule is set

    Examples: 
      | Day       | TuneableBulb    | ActiveLightName |
      | Today	  | TWBulb01UK      | tuneable light  |