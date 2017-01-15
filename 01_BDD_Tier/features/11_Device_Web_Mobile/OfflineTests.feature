Feature: Consists of scenario that validates the Offline tests

  @SC-OFF-RS01 @OfflineTest
  Scenario: SC-OFF-RS01_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online and repeated infinitely
      | DeviceName | DeviceType |
      | BM         | SLR2       |

  @SC-OFF-RS02 @OfflineTest
  Scenario: SC-OFF-RS02_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online and repeated infinitely
      | DeviceName | DeviceType |
      | SP         | SLP2       |

  @SC-OFF-RS03 @OfflineTest
  Scenario: SC-OFF-RS03_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLR2       |

  @SC-OFF-RS04 @OfflineTest
  Scenario: SC-OFF-RS04_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLP2       |

  @SC-OFF-RS05 @OfflineTest
  Scenario: SC-OFF-RS05_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLB1       |

  @SC-OFF-RS06 @OfflineTest
  Scenario: SC-OFF-RS06_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLB3       |

  @SC-OFF-RS07 @OfflineTest
  Scenario: SC-OFF-RS07_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLP2C      |

  @SC-OFF-RS08 @OfflineTest
  Scenario: SC-OFF-RS08_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLT3       |

  @SC-OFF-RS09 @OfflineTest
  Scenario: SC-OFF-RS09_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLT4       |

  @SC-OFF-CS10 @OfflineTest
  Scenario: SC-OFF-CS10_Validate the device presence via Hub
    Given The Devices are paired with the Hive Hub
    When The device is untouched and validate the presence status of the devices infinitely
      | DeviceName | DeviceType |
      | SB         | SLB3       |
