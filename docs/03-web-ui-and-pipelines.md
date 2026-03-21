# Web UI and Pipeline Setup

Limelight stores up to **10 pipelines**. Think of each pipeline as a saved vision program with its own camera settings, processing mode, and outputs.

## Core Workflow

1. Connect to the web UI.
2. Create or select a pipeline.
3. Choose a pipeline type.
4. Tune input settings.
5. Tune pipeline-specific settings.
6. Validate outputs in the stream, 3D view, and live data.
7. Save or export the pipeline.

## Critical Workflow Detail

If you want to edit multiple pipelines without robot code immediately switching them back, enable:

- `Ignore NetworkTables Index`

That makes the camera ignore robot-side pipeline switching while you are tuning.

## Input Tab

The Input tab controls the raw image before the main tracker runs.

### Pipeline Type

Available families include:

- AprilTags / fiducials
- color / retroreflective
- neural detector
- neural classifier
- Python SnapScript
- barcode
- focus / viewfinder utilities

### Source Image

Usually:

- `Camera` for live work
- `Snapshot` for repeatable offline tuning

Snapshots are useful when you want deterministic tuning instead of chasing a moving robot or lighting conditions.

### Resolution and Zoom

Important tradeoff:

- lower resolution = higher FPS
- higher resolution = better 3D AprilTag accuracy and range

Official guidance:

- use lower resolutions like `320x240` when you care about simple 2D speed
- use the highest practical resolution when you care about 3D AprilTag tracking/localization

### Exposure

Lower exposure reduces motion blur and is one of the most important AprilTag tuning levers.

Rule of thumb:

- lower exposure until tags start to become unreliable
- add brightness back with gain only as needed

### Black Level and Gain

- `Black Level` darkens the image at the sensor level
- `Gain` brightens the image but adds noise

For AprilTags, the usual goal is a short exposure with just enough gain to keep the tag readable.

### LEDs

- pipeline default can be overridden later via NetworkTables/API
- LL3 has built-in LED control relevant to retro/color work
- LL4 does not have LL3-style integrated aiming illumination

### Stream Orientation

- affects the displayed stream
- does **not** change result math

## Good Pipeline Discipline

- Use one pipeline per task, not one pipeline for everything.
- Name pipelines by intent, not by slot number.
- Back them up before OS updates.
- Keep one known-good pipeline untouched during competition.
- Use snapshots to tune difficult lighting conditions off the field.

## Performance Controls That Matter Most

### Crop

Cropping can provide very large performance gains by reducing the part of the image you search.

Use it when:

- you know the target can only appear in part of the image
- you want higher throughput without lowering full-frame resolution

### Detector Downscale

This is especially important for AprilTags:

- higher downscale = more FPS
- too much downscale = less range

Per the official docs, detector downscale usually hurts range more than 3D stability, so it is often a good trade when tags are expected nearby.

## Crosshair and Output

Limelight can report results relative to a configurable crosshair.

Use this when:

- your shooter or manipulator is intentionally offset from camera center
- you want a “servo-to-this-point” workflow without changing robot code math

See [Calibration and Coordinate Systems](./08-calibration-and-coordinate-systems.md) for crosshair details.

## Pipeline Types

### AprilTag

Use for:

- `tx`/`ty` target servoing
- 3D tag pose
- full robot localization

Read next:

- [FRC Java AprilTag Localization](./04-frc-java-apriltag-localization.md)
- [AprilTag Pipelines and Localization Concepts](./05-apriltag-pipelines-and-localization.md)

### Color / Retroreflective

Use when:

- the target is easy to light or segment
- maximum speed matters more than semantic understanding

### Neural

Use when:

- the target is not well-described by simple color/shape rules
- you need piece detection or classification

### Python SnapScript

Use when:

- you want custom OpenCV logic on-camera
- built-in pipeline types are not expressive enough

### Barcode

Use when:

- you need QR/DataMatrix/UPC/EAN/Code128/PDF417 decoding

## Recommended Competition Habits

- Verify the active pipeline before every test session.
- Check live data, not just the video stream.
- Tune exposure for motion, not for the prettiest image.
- Re-verify camera pose after any mechanical change.
