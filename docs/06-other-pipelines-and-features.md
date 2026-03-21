# Other Pipelines and Features

AprilTags are the main FRC localization use case, but Limelight also covers several other vision problems well.

## Color and Retroreflective Pipelines

These remain useful when you want very fast, deterministic tracking with minimal compute cost.

### When they are a good fit

- highly controllable target color
- retroreflective tape
- simple game pieces under predictable lighting
- maximum FPS matters more than semantic recognition

### Important concepts

- HSV thresholding is the main gate
- contour filtering selects candidate blobs
- sort mode chooses the winning contour
- grouping can combine multiple blobs into one target

### Tuning rules that matter

- keep hue bounds as tight as possible
- raise minimum value so black pixels do not leak through
- use erosion/dilation only to clean up thresholding, not to compensate for bad color settings
- use area/fullness/aspect-ratio filters to reject junk
- enable raw corners or JSON only if you actually need them

## Neural Pipelines

### Detector

Use for:

- finding objects and their locations
- game piece detection
- semantic target acquisition

### Classifier

Use for:

- categorizing a cropped view
- state recognition
- possession detection

### Hardware notes

- LL3-class neural pipelines historically rely on an external **Google Coral**
- LL4 supports newer Hailo-based workflows
- the 2026.0 release notes call out Hailo 8L support and new trainer-generated Hailo models

### Training flow

- collect a diverse dataset
- annotate consistently
- keep class labels simple
- use the Limelight neural trainer for detectors
- use Teachable Machine for simple classifiers

## Python SnapScript

SnapScript is the “I need custom vision logic on the camera” option.

Key properties from the official docs:

- write one `runPipeline(image, llrobot)` function
- access OpenCV and NumPy on-camera
- receive robot inputs through `llrobot`
- send custom outputs back through `llpython`
- return a contour to make Limelight’s normal crosshair/`tx`/`ty` pipeline latch onto your custom result

Use SnapScript when:

- built-in pipeline types are close but not enough
- you want custom overlays or pre/post-processing
- you want robot-state-aware image logic

## Barcode Pipelines

Limelight supports:

- QR Code
- DataMatrix
- UPC
- EAN
- Code128
- PDF417

Barcode strings appear in:

- `rawbarcodes` over NetworkTables
- the `Barcode` array in JSON results

Barcode pipelines also populate normal 2D metrics like `tx`, `ty`, and `ta`.

## Rewind

Rewind is an LL4-only operational feature introduced in Limelight OS 2026.0.

It records:

- video
- frame-by-frame targeting JSON
- boot logs

This is not a runtime control feature so much as a debugging feature. It is extremely useful when a team says “vision failed in auto” but cannot reproduce the exact lighting, occlusion, or motion case live.

## When To Use What

| Problem | Best starting point |
| --- | --- |
| Field localization | AprilTag + MegaTag2 |
| Auto-aim at a known target | AprilTag `tx`/`ty` or retroreflective pipeline |
| Fast game-piece tracking with obvious color cues | Color pipeline |
| Game-piece detection with cluttered backgrounds | Neural detector |
| Custom per-frame CV logic | Python SnapScript |
| Read encoded IDs/data | Barcode pipeline |
