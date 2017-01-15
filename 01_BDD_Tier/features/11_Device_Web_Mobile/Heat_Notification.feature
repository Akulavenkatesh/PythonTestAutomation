Feature: Validate the Heating Notification functionality

    @SC-HN-01 @Heat_Notification @RegressionTest
  Scenario Outline: SC-HN-001_Validate the heating notifications
    Given The Hive product is paired and setup for Heating Notification with API Validation
    When heating notification is set automatically for HIGH Temperature alert with Target Temperature as <HighTargetTemperature1> on the Client
	Then Automatically validate HIGH Temperature alert as active with Target Temperature as <HighTargetTemperature1>
	When heating notification is set automatically for LOW Temperature alert with Target Temperature as <LowTargetTemperature1> on the Client
	Then Automatically validate LOW temperature alert as active with Target Temperature as <LowTargetTemperature1>
	When heating notification is turned OFF automatically for HIGH Temperature alert and LOW Temperature alert on the Client
	Then Automatically validate the alerts as turned OFF
	When heating notification is set automatically for HIGH Temperature alert with Target Temperature as <HighTargetTemperature2> and LOW Temperature alert with Target Temperature as <LowTargetTemperature2> on the Client
	Then Automatically validate HIGH temperature alert as active with Target Temperature as <HighTargetTemperature2> and LOW temperature alert as active with Target Temperature as <LowTargetTemperature2>
    
	Examples:
		| HighTargetTemperature1 | LowTargetTemperature1 | HighTargetTemperature2 | LowTargetTemperature2 |
  	    | 25.5        			 | 13.5       			 | 31.0       		 	  | 9.0         		  |
    
	 