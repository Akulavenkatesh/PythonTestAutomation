#Created on 10 August 2016

#@authors: 
#iOS        - rajeshwaran
#Android    - TBD
#Web        - TBD

###################Variable Definitions#######################################################
#Motion Sensor 	- Name given for the Motion Sensor in the Kit
#Contact Sensor - Name given for the Contact Sensor in the Kit
#Plug 			- Name given for the Plug in the Kit
#Bulb 			- Name given for the Bulb in the Kit
#Sensor 		- The producer of the recipe - Motion/Contact sensor
#SensorState 	- The state of the contact sensor for trigerring the recipe - Open / Close / Detects Motion
#TypeOf 		- The type of notification to be set for the producer - Push / Email
#Device 		- The consumer of the recipe - Plug/Bulb
#DeviceState 	- The state of the consumer to be set - On / Off
#Duration 		- The duration for which the recipe should be set - 30 secs to Indefinitely
##############################################################################################


Feature: Validate the various recipes available for the sensors

    @RecipeBasics_01 @Recipes
    Scenario Outline: SC-RB-MC01_Validate all existing recipes are removed and recipe template is verified 
    #Here we are removing the existing recipes to validate the recipe template and begin testing from the initial state
    Given The <Motion Sensor> / <Contact Sensor> / <Plug> / <Bulb> are paired with the hub
    When User removes all of the existing recipes
    Then Verify if the recipe template has all available options

    Examples: 
      |	Motion Sensor  	|	Contact Sensor	|	Plug	|	Bulb	|
      |	Motion sensor  	|	Contact sensor	|	Plug	|	Bulb	|
      
    @RecipeBasics_02 @Recipes
    Scenario Outline: SC-RB-MC02_Validate legacy recipes are set as expected       
    #Verify if we are able to set the desired notification recipe
    Given The <Sensor> is paired with the hub
	When User sets Push notification recipe for <Sensor> when <SensorState> in the Client
	Then Verify if the Push notification recipe is displayed for <Sensor> when <SensorState> in the device recipe screen
	When User sets Push&Email notification recipe for <Sensor> when <SensorState> in the Client
	Then Verify if the Push&Email notification recipe is displayed for <Sensor> when <SensorState> in the device recipe screen
	When User sets Email notification recipe for <Sensor> when <SensorState> in the Client
	Then Verify if the Email notification recipe is displayed for <Sensor> when <SensorState> in the device recipe screen

    Examples: 
      |Sensor			|	SensorState		|
      |Motion sensor  	|	detects motion	| 
      |Contact sensor	|	opened			| 
      |Contact sensor   |	closed			| 
     
    @RecipeBasics_03
    Scenario Outline: SC-RB-MC03_Set Plug / Bulb Recipes for the Motion sensors 
    #Verify if the user can set Plug / Bulb Recipes for motion sensors
    Given The <Sensor> and <Device> are paired with the hub
	When User sets <Device> to <DeviceState> for <Duration> recipe for <Sensor>
	Then Verify if the recipe is saved successfully in <Sensor> recipe screen

    Examples: 
      |	Sensor  		|	Device		|	DeviceState	|	Duration		|
      |	Motion sensor  	|	Plug		|	ON			|	Indefinitely	|
      |	Motion sensor	|	Bulb		|	OFF			|	Indefinitely	|
      
      
    @RecipeBasics_04 
    Scenario Outline: SC-RB-MC04_Set Plug / Bulb Recipes for the Contact sensors 
    #Verify if the user can set Plug / Bulb Recipes for contact sensors
    Given The <Sensor> and <Device> is paired with the hub
    When User sets <Device> to <DeviceState> for <Duration> recipe when <Sensor> is <SensorState>
	Then Verify if the recipe is saved successfully in <Sensor> recipe screen
      
    Examples: 
      |	Sensor  		|	SensorState	|	Device	|	DeviceState	|	Duration	|
      |	Contact sensor  |	OPENED		|	Plug	|	ON			|	30 secs		|
      |	Contact sensor  |	OPENED		|	Bulb	|	OFF			|	30 secs		|
      |	Contact sensor	|	CLOSED		|	Plug	|	ON			|	15 mins		|
      |	Contact sensor	|	CLOSED		|	Bulb	|	OFF			|	15 mins		|

    @RecipeBasics_05 
    Scenario Outline: SC-RB-MC05_Edit existing Plug / Bulb Recipes for the Motion sensors 
    #Verify if the user can edit the Plug / Bulb Recipes for motion sensors that was set earlier
    Given The <Sensor> and <Device> is paired with the hub
	When User edits <Device> to <DeviceState> for <Duration> recipe for <Sensor>
	Then Verify if the recipe is saved successfully in <Sensor> recipe screen

    Examples: 
      |	Sensor  		|	Device		|	DeviceState	|	Duration		|
      |	Motion sensor  	|	Plug		|	OFF			|	1 min			|
      |	Motion sensor	|	Bulb		|	ON			|	3 mins			|
      
      
    @RecipeBasics_06 
    Scenario Outline: SC-RB-MC06_Edit Plug / Bulb Recipes for the Contact sensors 
    #Verify if the user can edit Plug / Bulb Recipes for contact sensors that was set earlier
    Given The <Sensor> and <Device> is paired with the hub
    When User edits <Device> to <DeviceState> for <Duration> recipe when <Sensor> is <SensorState>
	Then Verify if the recipe is saved successfully in <Sensor> recipe screen
      
    Examples: 
      |	Sensor  		|	SensorState	|	Device	|	DeviceState	|	Duration	|
      |	Contact sensor  |	OPENED		|	Plug	|	OFF			|	30 secs		|
      |	Contact sensor  |	OPENED		|	Bulb	|	ON			|	30 secs		|
      |	Contact sensor	|	CLOSED		|	Plug	|	OFF			|	15 mins		|
      |	Contact sensor	|	CLOSED		|	Bulb	|	ON			|	15 mins		|
      