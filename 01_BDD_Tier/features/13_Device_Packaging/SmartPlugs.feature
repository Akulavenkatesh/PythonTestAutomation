Feature: Contains all the scenario related to Smart Plugs

  @SC-SP-DP01-01 @SmartPlug
  Scenario: SC-SP-DP01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2       | 000D6F000AE154DF |

  @SC-SP-DP01-02 @SmartPlug
  Scenario: SC-SP-DP01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2       | 000D6F000B99FC75 |

  @SC-SP-DP01-03 @ZigbeeDumpTet
  Scenario: SC-ZT-03_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLP2       |

  @SC-SP-DP01-04 @ZigbeeDumpTet
  Scenario: SC-ZT-04_The smart plug state is changed and validated the using zigbee attribute and repeated infinitely.
    Given The telegesis is paired with given devices
    When the smartplug state is changed to below states and validated using the zigbee attribute and repeated infinitely
      | State |
      | ON    |
      | OFF   |
