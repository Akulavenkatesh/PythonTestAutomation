Feature: Validate the various mode changes for Hot Water

   @Kingsold   @SC-OB-AC01 @All_Client @V6_App
  Scenario: SC-OB-AC01_Validate the account details
    Given The Hive product is paired and setup for Central Heating with API Validation
	When I navigate to the account details screen on the Client
	Then I should be able to view the account details and the app version on the Client
	
