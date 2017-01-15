Feature: Set the Bindings between Nodes and validate the same

  @SC-BT-SB01 @BindingTest
  Scenario Outline: SC-BT-SB01_Set the given Bindings between Nodes and validate the same
    Given The Hive product with the existing Bindings cleared on the <Node>
    When the Bindings are set for the below Clusters on the <Node>
      | End Point | Cluster ID |
      | 05        | 0000       |
      | 06        | 0000       |
      | 05        | 0201       |
      | 06        | 0201       |
      | 05        | FD00       |
      | 06        | FD00       |
      | 05        | 0202       |
      | 06        | 0202       |
      | 05        | FD01       |
      | 06        | FD01       |
      | 05        | FD02       |
      | 06        | FD02       |
    Then validate if the Bindings are set correctly

    Examples: 
      | Node |
      | BM   |

  @SC-BT-SB03 @BindingTest
  Scenario Outline: SC-BT-SB01_Set the given Bindings between Nodes and validate the same
    Given The Hive product with the existing Bindings cleared

    Examples: 
      | Node ID |
      | 885E    |

      
   @SC-MSC-01 @Validatedevice
  Scenario: SC-BT-SB01_Set the given Bindings between Nodes and validate the same
    Given The telegesis is paired with given devices
    When The the nodedesc AT command is passed the return message is validated infinitely

    
    @SC-MSC-02 @Install
  Scenario: SC-MSC-02_Install and uninstall the app with latest and older version of the app and verify if 32C temperature spike happens
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The the app is unstalled and installed with latest version then the 32C temperature spike is verified
    
