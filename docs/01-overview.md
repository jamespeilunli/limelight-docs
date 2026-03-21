# Overview

Limelight is a smart camera platform that combines an image sensor, onboard compute, Limelight OS, a browser-based configuration UI, and several runtime APIs. For FRC, the core value is simple:

- You can ship working vision without building an entire camera pipeline stack yourself.
- You can scale from simple `tx`/`ty` aiming to full AprilTag-based robot localization.
- You can integrate through NetworkTables and WPILib without adding a heavyweight service on the robot.

## Supported Cameras in This Repo

### Limelight 3

- Color rolling-shutter camera
- 10/100 Ethernet
- Built-in green LEDs
- Strong general-purpose FRC camera
- Supports AprilTags, MegaTag, MegaTag2, Python pipelines, barcodes, and neural pipelines
- Neural acceleration is through an external Google Coral

### Limelight 4

- Monochrome global-shutter camera
- Gigabit Ethernet
- Internal IMU
- Optional Hailo acceleration
- Better AprilTag throughput and motion performance than LL3
- Adds LL4-only features like Rewind

## Practical Model Choice

- Choose **LL4** if AprilTag localization is a first-class subsystem and you care about motion robustness, IMU-assisted MegaTag2, or higher-end neural support.
- Choose **LL3** if you want a lower-cost FRC-ready camera and can tolerate lower AprilTag performance.
- LL3 is still good enough for modern localization if you mount it well, expose correctly, configure your robot-space pose correctly, and feed MegaTag2 a trustworthy robot heading every frame.

## Capability Tiers

### Tier 1: 2D Targeting

Use `tv`, `tx`, `ty`, and `ta`.

Good for:

- auto-aim
- simple alignment
- target centering
- quick servoing

### Tier 2: 3D Tag Tracking

Use AprilTag pose outputs such as:

- `targetpose_cameraspace`
- `targetpose_robotspace`
- `camerapose_targetspace`

Good for:

- relative measurements to a tag
- point-of-interest targeting
- target-space reasoning

### Tier 3: Full Robot Localization

Use:

- MegaTag (`botpose_wpiblue`)
- MegaTag2 (`botpose_orb_wpiblue`)

Good for:

- field pose estimation
- fusing vision into WPILib pose estimators
- autonomous path correction
- multi-tag or single-tag field localization

MegaTag2 is the modern recommendation whenever you can supply a reliable robot heading.

## Runtime Interfaces

Limelight publishes through:

- NetworkTables 4
- JSON
- REST/HTTP
- WebSocket
- Modbus TCP

For **FRC Java**, the default recommendation is:

1. Configure in the web UI.
2. Use **LimelightHelpers / LimelightLib** in robot code.
3. Fall back to raw NetworkTables or JSON only when you need lower-level control.

## Suggested Reading Order

1. [Hardware and Bring-Up](./02-hardware-and-bringup.md)
2. [Web UI and Pipeline Setup](./03-web-ui-and-pipelines.md)
3. [FRC Java AprilTag Localization](./04-frc-java-apriltag-localization.md)
4. [AprilTag Pipelines and Localization Concepts](./05-apriltag-pipelines-and-localization.md)
5. [APIs and Programming Reference](./07-apis-and-programming.md)
