Feature: Validate the change password feature on the client

    @Rudhran  
    Scenario: SC-OB-CP01_Validate the ChangePassword
    Given The Hive product is paired to a hub and navigated to Change Password screen
	When User is changing password on the Client
	Then Validate user is able to login with the password changed