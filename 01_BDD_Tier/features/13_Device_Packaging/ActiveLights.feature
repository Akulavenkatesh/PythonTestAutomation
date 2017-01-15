Feature: Contains all the scenario related to Smart Plugs

  @SC-AL-DP01-01 @ActiveLight
  Scenario: SC-AL-DP01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | FWBulb01       | 000D6F000AE154DF |

  @SC-AL-DP01-02 @ActiveLight
  Scenario: SC-AL-DP01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | FWBulb01       | 000D6F000B99FC75 |

  @SC-AL-DP01-03 @ZigbeeDumpTet
  Scenario: SC-ZT-03_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | FWBulb01       |

  @SC-AL-DP01-04 @ZigbeeDumpTet
  Scenario: SC-ZT-04_The smart plug state is changed and validated the using zigbee attribute and repeated infinitely.
    Given The telegesis is paired with given devices
    When the ActiveLight state is changed to below states and validated using the zigbee attribute and repeated infinitely
      | State |
      | ON    |
      | OFF   |
