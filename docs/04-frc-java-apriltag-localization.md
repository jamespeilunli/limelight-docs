# FRC Java AprilTag Localization

This is the shortest path from “camera installed” to “pose estimator receiving useful Limelight measurements” in a modern Java WPILib robot.

## Recommended Architecture

- **Camera**: LL4 preferred, LL3 acceptable
- **Pipeline**: AprilTag / fiducial
- **Field pose output**: **MegaTag2**
- **Robot heading source**:
  - LL3: external robot gyro required in practice
  - LL4: external robot gyro still recommended; LL4 internal IMU assist is optional and useful
- **Robot code integration**: `LimelightHelpers.java` + WPILib pose estimator
- **Field origin**: **WPI Blue origin**

For FRC 2024 and beyond, always prefer:

- `botpose_orb_wpiblue`
- or the helper wrapper that returns the same thing

Do **not** build new code around WPIRed pose outputs.

## Step 1: Get the Camera Operational

Before writing robot code, confirm:

- latest appropriate Limelight OS is installed
- team number is set
- static IP is set
- web UI is reachable
- camera is rigidly mounted

If not, do [Hardware and Bring-Up](./02-hardware-and-bringup.md) first.

## Step 2: Create an AprilTag Pipeline

In the web UI:

1. Set `Pipeline Type` to `Fiducial Markers`.
2. Use `AprilTag Classic 36h11` for FRC.
3. Set marker size to `165.1 mm` for current FRC tags.
4. Start with a relatively low exposure and only add gain as needed.
5. Use the highest practical resolution if localization accuracy matters more than raw FPS.
6. Raise detector downscale only if you need more throughput and can afford some range loss.

The official docs also recommend:

- black level at `0`
- gain around `15` as a starting point
- reducing exposure until motion-blur losses improve, then backing off if lighting becomes insufficient

## Step 3: Upload a Field Map

Localization depends on an `.fmap` AprilTag field map being loaded onto the camera.

Use:

- the official field map download for your season, or
- a custom map from the Limelight map builder

Without the field map, you will not get useful field-space robot pose outputs.

## Step 4: Configure Camera Pose on the Robot

In the Limelight UI, configure the camera pose in **robot space**:

- forward
- right
- up
- roll
- pitch
- yaw

This is one of the most common failure points. If these values are wrong, localization will be wrong even if tag detection is perfect.

Robot-space axes:

- `+X` forward
- `+Y` robot-right
- `+Z` up

## Step 5: Add LimelightHelpers to the Robot Codebase

The official Limelight Java flow is intentionally simple:

- download the latest `LimelightHelpers.java`
- place it in your robot project

That gives you:

- direct getters for common NT values
- typed pose estimate helpers
- setters for robot orientation, filters, IMU mode, and other controls

## Step 6: Feed Robot Heading to MegaTag2 Every Frame

MegaTag2 assumes you know the robot heading. In robot code, call `SetRobotOrientation(...)` every cycle using your current robot yaw.

This is mandatory for modern MegaTag2 usage.

## Step 7: Pull MegaTag2 Pose and Fuse It into WPILib

Typical pattern:

1. Update your drivetrain pose estimator from wheel odometry + gyro.
2. Send current robot yaw to Limelight.
3. Read the current MegaTag2 estimate from Limelight.
4. Reject obviously bad updates.
5. Add accepted measurements to the pose estimator with suitable standard deviations.

## Java Example

```java
public void updateOdometry() {
    poseEstimator.update(
        gyro.getRotation2d(),
        new SwerveModulePosition[] {
            frontLeft.getPosition(),
            frontRight.getPosition(),
            backLeft.getPosition(),
            backRight.getPosition()
        }
    );

    boolean reject = false;

    LimelightHelpers.SetRobotOrientation(
        "limelight",
        poseEstimator.getEstimatedPosition().getRotation().getDegrees(),
        0, 0, 0, 0, 0
    );

    LimelightHelpers.PoseEstimate mt2 =
        LimelightHelpers.getBotPoseEstimate_wpiBlue_MegaTag2("limelight");

    if (Math.abs(gyro.getRate()) > 360.0) {
        reject = true;
    }

    if (mt2.tagCount == 0) {
        reject = true;
    }

    if (!reject) {
        poseEstimator.setVisionMeasurementStdDevs(
            VecBuilder.fill(0.7, 0.7, 9999999)
        );
        poseEstimator.addVisionMeasurement(mt2.pose, mt2.timestampSeconds);
    }
}
```

This is intentionally conservative:

- it trusts the robot gyro for heading
- it ignores frames with no tags
- it ignores updates during very fast rotation

Tune the rejection logic and covariance to match your drivetrain and field conditions.

## MegaTag vs MegaTag2

### Use MegaTag2 by default

MegaTag2 was introduced to:

- eliminate pose ambiguity issues
- improve robustness with single-tag views
- reduce the amount of filtering teams need to write

### Use MegaTag1 only if needed

MegaTag1 can still work, but it usually needs more filtering, especially with single-tag ambiguity.

If you must use MT1:

- reject `tagCount == 0`
- reject ambiguous single-tag results
- reject distant single-tag results more aggressively

## LL4 Internal IMU Usage

LL4 has a built-in IMU. The official docs recommend this general pattern:

- while disabled / pre-match: use IMU mode `1` to seed the internal IMU from your external gyro
- while enabled: use mode `4` if you want internal IMU plus external IMU assist

High-level idea:

- external gyro gives drift correction
- LL4 internal IMU gives high-rate frame-to-frame motion information

That said, you do **not** need LL4 IMU integration to get good MegaTag2 localization working. Start without it, then add it after your baseline pipeline and pose fusion are stable.

## Dynamic Tag Filtering

MegaTag2 is viable even with single tags, so you should not feel forced to use every visible tag.

Use ID filtering when appropriate:

- limit the active tag set to tags relevant to the current task
- reject known bad or irrelevant tags
- reduce false positives or field-layout contamination in custom environments

## Common Failure Modes

- No field map uploaded
- Wrong tag family
- Wrong tag size
- Wrong robot-space camera pose
- Not calling `SetRobotOrientation(...)` every frame
- Using red-origin outputs in a blue-origin codebase
- Exposure too high, causing motion blur
- Detector downscale too aggressive for the distances you need
- Fusion covariance too optimistic

## Minimal Validation Checklist

- You can see tag IDs in the Limelight UI
- The 3D visualizer moves correctly as the robot moves
- `tagCount > 0` when you face known tags
- Estimated robot pose appears in the expected field location
- Vision corrections reduce drift instead of creating jumps

## After This Page

- For deeper theory and tuning: [AprilTag Pipelines and Localization Concepts](./05-apriltag-pipelines-and-localization.md)
- For fields, APIs, and low-level values: [APIs and Programming Reference](./07-apis-and-programming.md)
- For calibration and frame conventions: [Calibration and Coordinate Systems](./08-calibration-and-coordinate-systems.md)
