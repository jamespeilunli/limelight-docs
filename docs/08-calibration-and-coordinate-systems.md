# Calibration and Coordinate Systems

Most Limelight failures that look like “vision is bad” are actually one of these:

- the camera is poorly calibrated for the task
- the camera pose on the robot is wrong
- the team is mixing coordinate frames

## Crosshair Calibration

Crosshair calibration changes the origin for `tx` and `ty`.

Use it when:

- the camera is not the same aiming line as the mechanism
- you want the robot to center on an offset point without changing code math

The official docs support:

- single-crosshair mode
- dual-crosshair mode

Use dual mode only if you have a real use case for switching between two aim points. Otherwise keep it simple.

## ChArUco Calibration

### Why you should care

For simple 2D servoing, default calibration is often fine.

For serious 3D AprilTag work and localization, custom calibration improves:

- camera intrinsics accuracy
- distortion modeling
- 3D pose quality
- consistency across the image

### What the calibration estimates

- camera matrix
- distortion coefficients

### Official workflow

1. Build or print a flat ChArUco board.
2. Measure square and marker sizes accurately with calipers.
3. Create a ChArUco preview pipeline in the web UI.
4. Confirm board settings match the physical board.
5. Capture at least `25` images; `50+` is better.
6. Ensure images vary in position, depth, and perspective.
7. Calibrate from the Calibration tab.
8. Inspect reprojection error and coverage.
9. Upload the resulting calibration back to the camera.

### Quality targets

- reprojection error ideally under `1 pixel`
- pixel aspect ratio close to `1.0`
- broad coverage across the full image

### Important official note

The docs recommend calibrating at one high resolution:

- LL3: `1280x960`
- LL3G: `1280x800`

Limelight then scales intrinsics for matching aspect ratios automatically.

## Coordinate Frames

### Camera Space

- origin: lens center
- `+X`: right
- `+Y`: down
- `+Z`: forward out of the camera

### Target Space

- origin: center of the target
- `+X`: target-right
- `+Y`: down
- `+Z`: normal out of the target

### Robot Space

- origin: robot center projected to the floor
- `+X`: forward
- `+Y`: robot-right
- `+Z`: up

### Field Space

For FRC, prefer:

- **WPI Blue** field space

Do not casually mix:

- centered field-space definitions
- blue-corner field-space definitions
- red-corner field-space definitions

## The Most Important Distinction

Camera-space and target-space use a vision-centric convention where `+Y` points down.

Robot-space uses the robot convention where `+Z` points up.

If you skip this distinction, your transforms will look plausible but still be wrong.

## Practical Localization Guidance

- First get robot-space camera pose correct.
- Then verify tag detections.
- Then verify field map correctness.
- Only then spend time tuning estimator covariances.

## When To Recalibrate

- lens changed
- focus changed substantially
- camera physically damaged
- persistent 3D inconsistencies across the image
- you upgraded workflow and now care about higher-accuracy localization

## Related Pages

- [FRC Java AprilTag Localization](./04-frc-java-apriltag-localization.md)
- [AprilTag Pipelines and Localization Concepts](./05-apriltag-pipelines-and-localization.md)
