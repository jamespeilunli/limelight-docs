# Hardware and Bring-Up

This page is about getting a Limelight 3 or 4 physically installed, powered, reachable on the network, and updated.

## LL3 vs LL4 at a Glance

| Topic | Limelight 3 | Limelight 4 |
| --- | --- | --- |
| Sensor | OV5647 color rolling shutter | OV9281 monochrome global shutter |
| Ethernet | 10/100 | Gigabit |
| Illumination | Built-in green LEDs | No built-in aiming LEDs |
| AprilTag performance | Good | Better |
| IMU | No | Yes, internal |
| Neural acceleration | External Google Coral | Optional Hailo 8 / 8L |
| Typical localization recommendation | MegaTag2 with external robot heading | MegaTag2 with external heading, optionally IMU assist |

## Mounting

### General rules

- Mount the camera rigidly. Flex shows up as localization noise.
- Protect the Ethernet cable with strain relief.
- Record the exact camera pose relative to the robot. You will need this for localization.
- Avoid mounting at the exact same height as the tags when you care about stable AprilTag pose; some vertical offset and tilt help.

### LL3

- Footprint: `3.174in x 1.930in`
- Use `#10` or `M4` through-hardware
- Built-in LEDs help for retro/color pipelines

### LL4

- Footprint: `3.154in x 1.894in`
- Use `#10`/`M4` through-hardware or `M3` threaded points
- Global shutter makes it the stronger choice for motion-heavy AprilTag work

## Power

### LL3

- Input: `4.1V-16V`
- Red-button 2025 LL3 variant: `4.1V-24V` with `30V` absolute max
- Use a `5A` breaker
- Official docs strongly recommend a **dedicated VRM** for older pre-2025 white-button LL3 units because of load-dump risk from swerve regen plus battery disconnect events

### LL4

- Buck-boost input: `5V-26V`, `3.5V-35V` absolute range
- Use a `5A` or `10A` breaker
- Official docs say LL4 no longer needs a dedicated VRM for the battery disconnect / regen problem that affected older generations
- **PoE is not supported**

## Ethernet and USB

### Match usage

- In FRC, the normal path is Ethernet from Limelight to the robot radio/network.
- Set team number in the Limelight UI so the camera can auto-connect to the robot’s NT4 server.

### USB

- LL4 supports USB-C connectivity and USB-Ethernet for setup and bench work.
- USB is useful for flashing, bench configuration, and quick access to the web UI.
- Do not treat USB as the default competition integration path for FRC robot code.

## Accessing the Web UI

Common methods:

- Limelight Hardware Manager
- `http://limelight.local:5801`
- Static-IP form like `http://10.TE.AM.11:5801`
- LL4 USB-Ethernet:
  - Windows: `http://172.28.0.1:5801`
  - Linux/Mac: `http://172.29.0.1:5801`

## FRC Network Settings

### Required

- Team number

### Recommended

- Static IP
- Unique hostname if you run multiple cameras

### Common static-IP pattern

- Limelight: `10.TE.AM.11`
- Netmask: `255.255.255.0`
- Gateway: `10.TE.AM.1`

The official docs explicitly recommend static IPs because DHCP and mDNS have historically been less reliable on real FRC fields than they are in the shop.

## Updating Limelight OS

Important: **updating Limelight OS erases pipelines and scripts**. Export them first.

High-level process:

1. Download the latest Limelight Hardware Manager and OS image from the Downloads page.
2. Put the camera into flash mode.
3. Flash the image with the vendor tooling.
4. Reboot and restore pipelines/scripts.

### LL3 notes

- USB-C is primarily for flashing on LL3.
- While the USB cable is connected for imaging, LL3 is in a special flash mode and the normal web UI is unavailable.

### LL4 notes

- Hold the config button while connecting USB-C to enter flash mode.
- LL4 can also be powered over USB while flashing, but normal robot power is still recommended for bench use.

## Bring-Up Checklist

- Mechanically mounted
- Power wired correctly
- Ethernet connected with strain relief
- Latest suitable Limelight OS installed
- Team number set
- Static IP set
- Hostname set if multiple cameras
- Web UI reachable from a laptop on the robot network
- Camera pose on the robot measured and written down

## Immediate Next Step

Once the camera is reachable, go to [Web UI and Pipeline Setup](./03-web-ui-and-pipelines.md).
