Feature: This feature file contains scenarios to validate the Zigbee bindings

  @SC-BT-01 @ZigbeeBindingTest
  Scenario Outline: SC-BT-01_To set bindings and validate the binding table on the device via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the reportable attributes are set to report for the given timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the specified timeperiod
    And the values of the reportable attributes should be the set value
    When the reportable attributes are set to report for the default timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the default timeperiod
    Then the values of the reportable attributes should be the default value
    When the device state is changed to OFF
    Then the telegesis stick is mornitored and verified whether the attributes report for the change immediately
    When the device state is changed to ON
    Then the telegesis stick is mornitored and verified whether the attributes report for the change immediately
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries

    Examples: 
      | DeviceType |
      | TWBulb01UK |

  @SC-BT-02 @ZigbeeBindingTest
  Scenario Outline: SC-BT-02_To set bindings and validate the binding table on the device via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the reportable attributes are set to report for the given timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the specified timeperiod
    And the values of the reportable attributes should be the set value
    When the reportable attributes are set to report for the default timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the default timeperiod
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries

    Examples: 
      | DeviceType |
      | SLR2B      |
