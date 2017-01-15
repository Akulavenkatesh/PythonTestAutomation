Feature: Contains all the scenario related to  Text Control validations

  @SC-TC-01 @TextControl
  Scenario: SC-TC-01_Adding a new user for Text controls options and validating maximum no of user
   	Given User is navigated to Text Control page 
    When  User adds the below list of UserName and Mobile number in Text Control Page
    
    |UserName | MobileNo |
	|ANK      |07441111111|
	|SRI      |07477777777|
	|ARUN     |07455555555|
	|RUD      |07448888394|
	|Test5    |07471204044|
	|Test6    |07466666666|	
	
    Then Validate maximum limit of new users for Text control options
	
	
	
