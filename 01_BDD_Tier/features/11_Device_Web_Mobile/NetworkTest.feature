Feature: Consists of scenario that validates the network between devices

  @SC-NT-JN01-01 @PairingTest
  Scenario: SC-NT-JN01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB1       | 001E5E09020F6AE0 |
      | SP         | SLP2       | 001E5E09020F2F4C |

  @SC-NT-JN01-02 @PairingTest
  Scenario: SC-NT-JN01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | SLL1       | 000D6F000B99FC75 |
      
   
@SC-NT-JN01-03 @PairingTest
  Scenario: SC-NT-JN01-03_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | FWBulb01US       | 00158D00012E4C02 |
      
    @SC-NT-JN01-04 @PairingTest
  Scenario: SC-NT-JN01-04_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2       | 000D6F000BC650BD |
   
   @SC-NT-JN01-06 @PairingTest
  Scenario: SC-NT-JN01-06_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB3       | 000D6F000AE147F6 |
      
   @SC-NT-JN01-05 @PairingTest
  Scenario: SC-NT-JN01-05_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB3       | 000D6F000AE154DF |
      
  @SC-NT-JN02-01 @PairingTest
  Scenario: SC-NT-JN02-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Hub
      | DeviceName | DeviceType      |
      | AL         | LDS_DimmerLight |

  @SC-NT-JN02-02 @PairingTest
  Scenario: SC-NT-JN02-02_The given devices are paired and unpaired sequentially and validated
    Given The Clipin are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | CB         | CL01_1     |

  @SC-NT-JN03-01 @PairingTest
  Scenario: SC-NT-JN03-01_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | AL         | FWBulb01_1     |
      
  @SC-NT-JN03-02 @PairingTest
  Scenario: SC-NT-JN03-02_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO1 Hub
      | DeviceName | DeviceType |
      | AL         | FWBulb01_1     |
      
        @SC-NT-JN03-03 @PairingTest
  Scenario: SC-NT-JN03-01_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO1 Hub
      | DeviceName | DeviceType |
      | AL         | TWBulb01UK_1     |
      
        @SC-NT-JN04-01 @PairingTest
  Scenario: SC-NT-JN04-01_The given devices are paired and unpaired sequentially and validated
    Given The Smart Plugs are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | SB         | SLB1_1     |