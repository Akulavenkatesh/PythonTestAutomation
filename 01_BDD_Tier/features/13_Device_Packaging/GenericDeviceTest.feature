Feature: Contains all the Generic scenarios for the devices

  @SC-GT-SC01-01 @Generic
  Scenario: SC-GT-SC01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | Generic    | 000D6F000AE154DF |

  @SC-GT-SC01-02 @Generic
  Scenario: SC-GT-SC01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | Generic    | 000D6F000B99FC75 |

  @SC-GT-SC02-01 @Generic
  Scenario: SC-GT-SC02-01_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the Device is downloaded with the clusters and attributes list via telegesis stick
      | DeviceName | DeviceType | MacID            |
      | SP         | Generic    | 000D6F000B99FC75 |
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceName | DeviceType | MacID            |
      | SP         | Generic    | 000D6F000B99FC75 |

  @SC-GT-SC03-01 @Generic
  Scenario: SC-GT-SC03-01_The smart plug state is changed and validated the using zigbee attribute and repeated infinitely.
    Given The telegesis is paired with given devices
    When the smartplug state is changed to below states and validated using the zigbee attribute and repeated infinitely
      | DeviceName | DeviceType | State | MacID            |
      | SP         | Generic    | ON    | 000D6F000B99FC75 |
      | SP         | Generic    | OFF   | 000D6F000B99FC75 |

  @SC-GT-SC04-01 @Generic
  Scenario: SC-GT-SC04-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType |
      | SP         | Generic    |
      | SP         | Generic    |

      
   @SC-GT-SC05-01 @Generic
  Scenario: SC-GT-SC05-01_Verify if the sensor checks in every five mins
    Given The telegesis is paired with given devices
    When the below <Device> Sensor Checkin is verifiied every five mins infinitely via Telegisis
      | Device |
      | MOT003 |
      
      
   @SC-GT-SC05-02 @Generic
  Scenario: SC-GT-SC05-02_Verify if the sensor checks in every five mins
    Given The telegesis is paired with given devices
    When the below <Device> Sensor Checkin is verifiied every five mins infinitely via Telegisis
      | Device |
      | DWS003 |