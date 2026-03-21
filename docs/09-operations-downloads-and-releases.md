# Operations, Downloads, and Current Releases

This page covers what matters operationally: what to download, what changed recently, and what to verify before an event.

## Current Release Snapshot

From the official Downloads and Change Log pages reviewed on **March 21, 2026**:

- Latest listed **Limelight OS** release: **2026.0**, dated **January 23, 2026** on the Downloads page
- Change log entry for **2026.0** is dated **January 22, 2026**
- Prior major listed final release: **2025.1 (Final Release)** on **February 24, 2025**

## What 2026.0 Matters For

### Rewind

LL4-only feature that stores:

- reduced-resolution full-rate video
- frame-aligned JSON results
- boot logs

This is a major debugging improvement for missed autos and non-reproducible vision failures.

### Calibration Overhaul

2026.0 improves:

- ChArUco corner detection
- calibration workflow
- live preview before image capture
- visualization of point clouds and mosaic coverage

### Capture Latency Accuracy

The official changelog states capture timestamps are now aligned to the middle of exposure, which matters when you are doing time-sensitive sensor fusion.

### Live Data View

You can inspect complete per-frame output in the web UI without writing custom dashboard code.

### Skewed Crop Windows

AprilTag pipelines can now use skewed crop windows, including over NT.

### Neural / Hailo Updates

2026.0 adds or improves:

- Hailo 8L support
- faster model execution
- new trainer-produced Hailo models

## Downloads You Will Actually Use

- Limelight Hardware Manager
- Limelight OS image
- official field maps / AprilTag maps
- ChArUco calibration board
- CAD models for mounting

Use the official Downloads page when preparing:

- a fresh camera
- an OS update
- a new season field-map upload
- a mount redesign

## Pre-Event Checklist

- Confirm camera is on the OS version you expect
- Export pipelines before any upgrade
- Re-upload the correct season field map
- Verify team number, hostname, and static IP
- Verify the active pipeline index and contents
- Validate camera pose on the robot after any mechanical work
- Bench-check tag detection and `tagCount`
- Verify pose estimates with the robot in known field locations

## On-Field Debug Checklist

- Is the pipeline actually the one you think is active?
- Is `tagCount` nonzero?
- Is exposure too high for current lighting and speed?
- Did the camera pose change after impact?
- Is the field map for the correct year and field build?
- Are you reading WPIBlue outputs consistently?
- Are you rejecting vision during extreme angular velocity?

## When To Use Rewind

Use Rewind when:

- autonomous missed a path correction
- localization jumped unexpectedly
- the robot saw tags in the pit but not on the field
- you need evidence for support or for your own post-match debugging

## Support and Example Material

The official docs also point to:

- example projects repo
- question / feedback resources

Those are useful once your baseline setup works, but they should not replace a disciplined bring-up and validation process.
