# Copilot Instructions for Open Simulation Interface (OSI)

## Overview

OSI is a Protocol Buffers (proto2) interface specification for environmental perception of automated driving functions. All `.proto` files use `syntax = "proto2"`, `option optimize_for = SPEED`, and belong to `package osi3`.

## Build & Test

**Run all tests:**

```sh
pip install pyyaml
python -m unittest discover tests
```

**Run a single test file or test case:**

```sh
python -m unittest tests.test_rules
python -m unittest tests.test_rules.TestRules.test_rules_compliance
```

**Validate proto compilation** (requires `grpcio-tools`):

```sh
python -m grpc_tools.protoc --proto_path=. --python_out=. osi_common.proto osi_occupant.proto
```

**Build Doxygen docs** (requires CMake, Doxygen, proto2cpp):

```sh
mkdir build && cd build
cmake -D FILTER_PROTO2CPP_PY_PATH=<path-to-proto2cpp> ../
cmake --build . --config Release
```

## Architecture

### Proto Dependency Hierarchy

```
osi_version.proto.in  (template → osi_version.proto via CMake)
        ↓
osi_common.proto      (primitives: Vector3d, Timestamp, Identifier, BoundingBox, etc.)
        ↓
building blocks       (osi_object, osi_lane, osi_environment, osi_trafficsign, osi_trafficlight,
                       osi_roadmarking, osi_occupant, osi_logicallane, osi_referenceline, osi_route, …)
        ↓
top-level containers  (see below)
```

### Top-Level Container Messages

| Message | File | Role |
|---------|------|------|
| `GroundTruth` | `osi_groundtruth.proto` | Complete simulated environment state |
| `SensorView` | `osi_sensorview.proto` | Input to a sensor model (GroundTruth + config) |
| `SensorData` | `osi_sensordata.proto` | Output of a sensor model (detected entities) |
| `HostVehicleData` | `osi_hostvehicledata.proto` | Vehicle's own internal state perception |
| `StreamingUpdate` | `osi_streamingupdate.proto` | Partial/incremental updates |
| `SensorDataSeries` | `osi_datarecording.proto` | Time-series recording wrapper |

### Detected vs Ground Truth Pattern

Ground truth entities (e.g. `MovingObject`, `Occupant`, `Lane`) live in `GroundTruth`. Each has a corresponding `Detected*` message (e.g. `DetectedMovingObject`, `DetectedOccupant`, `DetectedLane`) in `SensorData` that wraps a list of candidates with probabilities.

## Proto Commenting Conventions

Every message, enum, and field **must** have a comment. CI tests enforce this.

### Messages and Enums

Must start with `\brief` on a separate comment line:

```proto
//
// \brief A cartesian 3D vector for positions, velocities or accelerations.
//
// The coordinate system is defined as right-handed.
//
message Vector3d
{
```

### Fields

Minimum 2 comment lines (content + blank `//`). Units on a separate line:

```proto
    // The number of seconds since start.
    //
    // Unit: s
    //
    optional int64 seconds = 1;
```

### Validation Rules

Wrap in `\rules` / `\endrules` blocks. Available rules are defined in `rules.yml`:

```proto
    // \rules
    // is_greater_than_or_equal_to: 0
    // is_less_than_or_equal_to: 999999999
    // \endrules
```

Available rule keywords: `is_greater_than`, `is_greater_than_or_equal_to`, `is_less_than`, `is_less_than_or_equal_to`, `is_equal_to`, `is_different_to`, `is_globally_unique`, `refers_to`, `is_iso_country_code`, `first_element`, `last_element`, `check_if ... else do_check`, `is_set`, `minimum_length`, `maximum_length`.

### Other Doxygen Markers

- `\note` — important notes
- `\attention` — deprecation warnings
- `\c TypeName` — inline code/type reference
- `\image html filename.svg "caption" width=550px` — image reference
- `\b text` — bold

## Code Style

Defined in `.clang-format`: Google base style, 4-space indent, 80-column limit, Allman braces (`{` on new line), no tabs.

## Versioning

`VERSION` file holds `VERSION_MAJOR`, `VERSION_MINOR`, `VERSION_PATCH`. CMake substitutes these into `osi_version.proto.in` → `osi_version.proto`. Current version: **3.8.0**.

## CI Pipeline

GitHub Actions (`protobuf.yml`) runs on push/PR to master:
1. **Spellcheck** — aspell via pyspelling (custom wordlist at `.github/spelling_custom_words_en_US.txt`)
2. **Tests** — `python -m unittest discover tests`
3. **Doxygen build** — generates API docs from proto comments

## Key Conventions

- All proto field numbers are stable — never reuse or renumber existing fields.
- `repeated` fields use singular names (e.g. `repeated WheelData wheel_data`, not `wheel_datas`).
- Enum values are prefixed with the enum type in UPPER_SNAKE_CASE (e.g. enum `Seat` → `SEAT_FRONT_LEFT`).
- IDs use the `Identifier` message type and are typically `is_globally_unique`.
- Cross-references between entities use `refers_to` rules (e.g. `refers_to: MovingObject`).
- Coordinate system is right-handed, following ISO 8855 for vehicles.
- Bounding box offsets follow the `bbcenter_to_*` naming pattern (e.g. `bbcenter_to_rear`, `bbcenter_to_root`).
- PRs require DCO sign-off and "ReadyForCCBReview" label for Change Control Board review.
