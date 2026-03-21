# AprilTag Pipelines and Localization Concepts

This page connects the AprilTag-related official docs into one model: 2D targeting, 3D tag tracking, field localization, coordinate systems, and maps.

## Three Levels of AprilTag Use

### 1. 2D Targeting

Use:

- `tv`
- `tx`
- `ty`
- `ta`

This is the easiest migration path from old retroreflective pipelines. The official docs explicitly note that an AprilTag pipeline can still be used with standard `tx`/`ty` tracking logic.

### 2. Full 3D Tag Tracking

Use per-tag transforms such as:

- camera in target space
- target in camera space
- target in robot space

This is the right layer when you care about the robot relative to a single known tag.

### 3. Robot Localization

Use field-space robot pose outputs:

- `botpose_wpiblue` for MegaTag1
- `botpose_orb_wpiblue` for MegaTag2

This is the right layer when the robot needs an absolute field pose.

## Recommended FRC AprilTag Settings

From the official AprilTag quick-start guidance:

- Pipeline type: `Fiducial Markers`
- Family: `AprilTag Classic 36h11`
- Marker size: `165.1 mm` for current FRC tags
- Black level: `0`
- Use as high a resolution as your latency budget allows for 3D work
- Reduce exposure to fight motion blur
- Increase downscale only when the FPS gain is worth the range loss

## The Tuning Knobs That Actually Matter

### Resolution

- higher = better 3D accuracy and range
- lower = more FPS

### Exposure

- lower = less blur while moving
- too low = tags become unreadable in dim light

### Gain

- compensates for lower exposure
- too much gain adds noise and can hurt stability

### Detector Downscale

- more downscale = faster
- too much = worse range

### Crop

- huge performance win if you know where tags can appear

## Priority ID and Point-of-Interest Tracking

When doing both 2D and 3D work:

- you can set a priority ID so `tx`/`ty` are tied to the tag you care about most
- you can also define a **3D point of interest** relative to a tag and then track that point using `tx`/`ty`

That is useful when the game objective is offset from the tag itself.

## MegaTag1 vs MegaTag2

### MegaTag1

- older field pose estimator
- still usable
- more sensitive to ambiguity, especially single-tag cases
- usually needs more rejection logic

### MegaTag2

- modern recommendation
- better with single-tag views
- ambiguity-resistant
- expects robot heading input
- usually reduces custom filtering burden

For new FRC work, default to MegaTag2.

## Coordinate Systems You Must Keep Straight

### Camera Space

- origin at the camera lens
- `+X` right
- `+Y` down
- `+Z` out of the camera

### Target Space

- origin at the target center
- `+X` right from the target’s perspective
- `+Y` down
- `+Z` out of the tag plane

### Robot Space

- origin at the robot center projected to the floor
- `+X` forward
- `+Y` robot-right
- `+Z` up

### FRC Field Space

Preferred FRC convention:

- use **WPI Blue origin**

The official docs are explicit here: FRC teams should use the blue-origin field space for modern WPILib/pathplanning workflows.

## Maps and `.fmap` Files

Limelight field localization uses `.fmap` files.

What a map contains:

- tag family
- tag ID
- tag size in mm
- 4x4 transform for each tag
- map type such as `frc`

Use cases:

- official FRC field maps
- FTC maps
- custom practice fields
- tagged objects or workcells

You can build or edit maps with the Limelight map builder tool.

## When to Filter Tags

Do not assume “more tags always helps.”

Filter aggressively when:

- only certain tags are relevant to the task
- custom fields contain questionable tag placement
- you want the localizer to ignore irrelevant or low-quality tags

The official docs specifically call out dynamic filter support for MegaTag2.

## Choosing Outputs

### Use these for servoing

- `tx`
- `ty`
- `ta`
- `tid`

### Use these for field localization

- `botpose_orb_wpiblue`
- `stddevs`
- tag count and related metadata

### Use these for relative geometry

- `targetpose_cameraspace`
- `targetpose_robotspace`
- `camerapose_targetspace`
- `botpose_targetspace`

## High-Value Pitfalls

- Wrong map for the season or field build
- Wrong camera pose on the robot
- Forgetting that camera-space `+Y` is down while robot-space `+Z` is up
- Mixing robot yaw conventions
- Using WPIRed outputs in a blue-origin codebase
- Treating a pretty image as more important than low-blur AprilTag capture

## Related Pages

- [FRC Java AprilTag Localization](./04-frc-java-apriltag-localization.md)
- [Calibration and Coordinate Systems](./08-calibration-and-coordinate-systems.md)
- [APIs and Programming Reference](./07-apis-and-programming.md)
