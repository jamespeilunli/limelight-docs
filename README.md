# Limelight 3 and 4 Documentation

This repo is a condensed, task-oriented rewrite of the official Limelight documentation for teams using **Limelight 3** and **Limelight 4**, with special emphasis on **modern FRC AprilTag localization in a Java WPILib codebase**.

It is based on a scrape of the official Limelight documentation corpus under `docs.limelightvision.io` as of **March 21, 2026**, then reorganized for clarity and faster execution.

## Start Here

- If you need to get robot localization working in WPILib Java: [FRC Java AprilTag Localization](./docs/04-frc-java-apriltag-localization.md)
- If you need to choose between LL3 and LL4 or wire one correctly: [Hardware and Bring-Up](./docs/02-hardware-and-bringup.md)
- If you need to understand the web UI and pipeline workflow: [Web UI and Pipeline Setup](./docs/03-web-ui-and-pipelines.md)
- If you need a mental model for AprilTag tracking, MegaTag, MegaTag2, maps, and coordinate frames: [AprilTag Pipelines and Localization Concepts](./docs/05-apriltag-pipelines-and-localization.md)
- If you need programming/API details: [APIs and Programming Reference](./docs/07-apis-and-programming.md)
- If you need calibration and frame conventions: [Calibration and Coordinate Systems](./docs/08-calibration-and-coordinate-systems.md)
- If you need updates, downloads, and operational guidance: [Operations, Downloads, and Current Releases](./docs/09-operations-downloads-and-releases.md)
- If you want full traceability back to the official source pages: [Official Source Inventory](./docs/sources.md)

## What This Covers

- Limelight 3 and Limelight 4 hardware
- FRC networking and web UI bring-up
- Pipeline setup and tuning
- AprilTag 2D tracking, 3D tracking, and full robot localization
- MegaTag and MegaTag2
- WPILib Java integration through LimelightLib and NetworkTables
- JSON, REST, WebSocket, and Modbus interfaces
- ChArUco calibration and crosshair calibration
- Color/retroreflective, neural, Python SnapScript, and barcode pipelines
- Current Limelight OS release information relevant to LL3 and LL4

## What This Does Not Try To Do

- Reproduce the official docs page-for-page
- Cover Limelight 1 or 2 beyond occasional comparison context
- Replace official downloads, release notes, or vendor-maintained APIs

Use this repo as the fast path, then jump to the official sources when you need exact field names, route names, or vendor downloads.
