#Created on 10 August 2016
#@authors: 
#iOS        - rajeshwaran
#Android    - TBD
#Web        - TBD
Feature: Validate various Light Bulb features

    @BulbBasics01 @BulbControl
    Scenario Outline: SC-RB-DC01_Validate if the user is able to set all possible settings for the Color Light
    #Here we set all the possible settings for the Colour Light
    #Other colours that can be set are Red Orange,Orange Yellow,Yellow Green,Green Cyan, Cyan Blue,Blue Magenta, Magenta Pink,Pink Red
    Given The colour light <ActiveLightName> is paired with the hub and navigate to Client
    When User sets the tone as cool white on the Client
    Then Verify if the tone is set as expected in API for <ActiveLightID>
    When User sets the tone as mid white on the Client
    Then Verify if the tone is set as expected in API for <ActiveLightID>
    When User sets the brightness as 5 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>
    When User sets the brightness as 60 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>
    When User sets the colour as Red on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Orange on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Yellow on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Green on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Cyan on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Blue on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Magenta on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
    When User sets the colour as Pink on the Client
    Then Verify if the colour is set as expected in API for <ActiveLightID>
   
    
    Examples: 
		|ActiveLightName	|ActiveLightID  	|	
		|Colour light		|RGBBulb01UK 		|	
      

    @BulbBasics02 @BulbControl
    Scenario Outline: SC-RB-DC02_Validate if the user is able to set all possible settings for the Warm White Light
    #Here we set all the possible settings for the Warm White Light
    Given The tuneable light <ActiveLightName> is paired with the hub
    When User sets the tone as coolest white on the Client
    Then Verify if the tone is set as expected in API for <ActiveLightID>
    When User sets the tone as warmest white on the Client
    Then Verify if the tone is set as expected in API for <ActiveLightID>
    When User sets the brightness as 30 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>
    When User sets the brightness as 40 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>     
    
    
    Examples: 
		|ActiveLightName	|ActiveLightID  	|	
		|Tuneable light		|TWBulb01UK 		|	
      

    @BulbBasics03 @BulbControl
    Scenario Outline: SC-RB-DC03_Validate if the user is able to set all possible settings for the Fixed White Light
    #Here we set all the possible settings for the Fixed White Light
    Given The fixed light <ActiveLightName> is paired with the hub
    When User sets the brightness as 50 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>
    When User sets the brightness as 10 on the Client
    Then Verify if the brightness is set as expected in API for <ActiveLightID>     
    
    
    Examples: 
		|ActiveLightName	|ActiveLightID  	|	
		|Warm white light	|FWBulb01	 		|	
