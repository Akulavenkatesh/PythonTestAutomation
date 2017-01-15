Feature: Validate the forgotten password functionality 

  @SC-FP-01
 Scenario Outline: SC-FP-01_Validate the positive flow of forgotten password functionality
 Given The Hive product is paired and forgotten password screen is displayed on the Client
 When <Username> is automatically entered and submitted on the Client
 Then Validate if <New password> can be set for the <Username> and login is successful using <New password>
 
 
  Examples:
  | Username                  | New password      |
  | user01_prod               | Password12        |