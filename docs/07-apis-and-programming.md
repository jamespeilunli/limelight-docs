# APIs and Programming Reference

For FRC Java, the recommendation is simple:

1. Configure cameras and pipelines in the web UI.
2. Use `LimelightHelpers.java` in robot code.
3. Drop to raw NetworkTables or REST only when you need lower-level access.

## Integration Layers

### LimelightLib / LimelightHelpers

Best default for:

- FRC Java
- WPILib pose estimation
- readable robot code
- low-friction access to pose estimates and helpers

### NetworkTables

Best default transport for:

- normal FRC runtime communication
- dashboard integration
- low-latency robot reads and writes

### JSON

Best when:

- you want structured multi-result data
- you need per-target arrays across multiple pipeline types
- you want a language-neutral payload format

### REST/HTTP

Best when:

- scripting configuration or uploads
- bench tools
- diagnostics
- non-FRC integrations

### WebSocket

Best when:

- you want a full-framerate JSON results stream outside of robot code

### Modbus

Mostly relevant for:

- industrial automation
- PLC-style integrations

Not the normal FRC path.

## Important NetworkTables Reads

### Basic target data

- `tv`: target valid
- `tx`: horizontal error from crosshair
- `ty`: vertical error from crosshair
- `txnc`: horizontal error from principal pixel
- `tync`: vertical error from principal pixel
- `ta`: target area
- `tl`: targeting latency
- `cl`: capture latency
- `getpipe`: active pipeline index
- `json`: full JSON dump if enabled

### AprilTag and 3D data

- `tid`: primary tag ID
- `targetpose_cameraspace`
- `targetpose_robotspace`
- `camerapose_targetspace`
- `botpose_wpiblue`
- `botpose_orb_wpiblue`
- `stddevs`

### System and utility data

- `hw`: hardware stats array
- `crosshairs`
- `hb`: heartbeat
- `tcclass`: classifier class name
- `tdclass`: detector class name
- `rawfiducials`
- `rawdetections`
- `rawbarcodes`

## Important NetworkTables Writes

- `pipeline`: switch pipelines
- `ledMode`: LED override
- `priorityid`: prioritize a specific tag for `tx`/`ty`
- `crop`: dynamic crop window
- `robot_orientation_set`: robot yaw and rates
- `fiducial_id_filters_set`: allowed tag IDs
- `camerapose_robotspace_set`: camera pose on robot
- `imumode_set`: IMU behavior mode
- `imuassistalpha_set`: IMU complementary filter alpha
- `throttle_set`: skip frames for thermal management
- `rewind_enable_set`, `capture_rewind`: Rewind controls

## FRC Java: Typical Helper Calls

Common read-side methods:

- `getTV(...)`
- `getTX(...)`
- `getTY(...)`
- `getTA(...)`
- `getBotPoseEstimate_wpiBlue(...)`
- `getBotPoseEstimate_wpiBlue_MegaTag2(...)`

Common write-side methods:

- `SetRobotOrientation(...)`
- `SetFiducialIDFiltersOverride(...)`
- `SetIMUMode(...)`
- `SetIMUAssistAlpha(...)`

## JSON Results

The JSON results payload is Limelight’s most complete structured result object.

Important top-level data includes:

- validity
- timestamps
- frame index
- pipeline index and type
- `tx`, `ty`, `ta`
- `botpose*`
- `botpose_orb*`
- `stdev_mt1`
- `stdev_mt2`
- `imu`
- `hw`
- `rewind`

Important result arrays:

- `Retro`
- `Fiducial`
- `Detector`
- `Classifier`
- `Barcode`

Use JSON when you need all valid targets, not just the primary result.

## JSON Status

Status JSON is more about diagnostics than targeting.

Use it for:

- pipeline index/type checks
- interface state
- image source state
- thermal / performance inspection
- general health monitoring

## REST API

REST server:

- `http://<ip>:5807`

High-value routes:

- `GET /results`
- `GET /status`
- `GET /hwreport`
- `POST /pipeline-switch`
- `POST /update-pipeline`
- `POST /upload-fieldmap`
- `POST /upload-python`
- `POST /upload-nn`
- `POST /update-robotorientation`
- calibration routes under `/cal-*`
- snapshot routes
- Rewind recording routes

Use REST when you want tooling, automation, uploads, or scripted diagnostics.

## WebSocket API

WebSocket server:

- `ws://<ip>:5806`

Purpose:

- full-framerate streaming JSON results

This is useful for custom viewers, offboard logging, or non-WPILib dashboards.

## Modbus API

Modbus server:

- `<ip>:502`

It exposes:

- read-only registers for current outputs and diagnostics
- write registers for pipeline index and Python inputs

Treat this as industrial support, not the primary FRC integration surface.

## Recommendation Matrix

| Need | Best interface |
| --- | --- |
| FRC robot code | LimelightHelpers + NetworkTables |
| All per-frame data in a typed blob | JSON |
| Bench automation or uploads | REST |
| Non-FRC live result streaming | WebSocket |
| PLC / industrial control | Modbus |

## Practical Guidance

- Do not start by hand-parsing JSON if LimelightHelpers already exposes what you need.
- Do not start with REST for runtime FRC pose estimation.
- Use NetworkTables for control loops and pose fusion.
- Use JSON/REST/WebSocket for tooling, debugging, and custom integrations.
