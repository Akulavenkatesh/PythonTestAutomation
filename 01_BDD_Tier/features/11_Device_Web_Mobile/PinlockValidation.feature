Feature: Validate the pin lock feature on the client

    @Rudhran  
    Scenario: SC-OB-PL01_Validate the PinLock
	Given The Hive product is paired to a hub and navigated to Pin Lock screen’
    When User Sets Pin Lock on the Client
    Then Validate user is able to Succesfully set Pin
    When User Changes Pin on the Client
    Then Validate the User is able to Successfully change pin
    When user forgot Pin on client
    Then Validate user is able to logout of the app and login again  