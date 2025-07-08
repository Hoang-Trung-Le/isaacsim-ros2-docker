# Omniverse Warehouse Scene Description

## Overview
This document describes a 3D warehouse scene in Omniverse, stored in the USD file `full_warehouse.usd`. The scene represents a large indoor warehouse with structural elements (walls, floors, ceilings), lighting (rectangular and distant lights), navigation components (navmesh), and inventory items (cardboxes, forklifts). The scene is designed for simulation, rendering, or robotic navigation tasks, with a detailed hierarchy and material assignments.

- **Root Prim**: `full_warehouse.usd`
- **Default Prim**: `/Root`
- **World Bounds**: 
  - Min: (-28.86, -41.40, -2.93)
  - Max: (8.06, 33.59, 10.23)
  - Size: (36.91, 74.99, 13.16)
- **Time Range**: 0.0 to 100.0
- **Purpose**: Likely used for warehouse simulation, inventory management, or robotic navigation (e.g., forklift operations).

## Scene Objects
The scene contains various object types, including structural components, inventory items, lights, and cameras. Below are the significant objects, with details on their properties and roles.

### Cardboxes
Cardboxes are inventory items scattered throughout the warehouse, likely representing stored goods. They are identified by paths like `/Root/Box_*` (e.g., `/Root/Box_42696`, `/Root/Box_43528`).

- **Count**: Hundreds (e.g., paths from `Box_42696` to `Box_44096` suggest at least 1400+ instances).
- **Types**:
  - `SM_CardBoxC_01`: Smaller cardboard boxes.
  - `SM_CardBoxD_03`, `SM_CardBoxD_04`: Larger or variant cardboard boxes.
  - `SM_CardBoxB_02`: Another variant, possibly different in size or texture.
- **Properties**:
  - **Materials**: Assigned materials like `MI_CardBoxC_01`, `MI_CardBoxD_04` (cardboard textures).
  - **Hierarchy**: Each box is under `/Root/Box_*/SM_CardBox*`, with a `Looks` scope for material bindings.
  - **Transforms**: Positioned across the warehouse floor, possibly stacked or arranged on racks.
- **Role**: Represent stored inventory, likely for robotic picking or forklift transport.
- **Example**:
  - Path: `/Root/Box_42712/SM_CardBoxD_04`
  - Material: `/Root/Box_42712/SM_CardBoxD_04/Looks/MI_CardBoxD_04`
  - Description: A large cardboard box, possibly containing heavy goods.

### Forklifts
Forklifts are vehicles used for moving cardboxes within the warehouse. Identified under `/Root/forklift`.

- **Count**: At least 1 (path `/Root/forklift`).
- **Components**:
  - `S_ForkliftBody`: Main body of the forklift.
  - `S_ForkliftFork`: Fork component for lifting pallets.
- **Properties**:
  - **Materials**: Assigned materials under `/Root/forklift/Materials` and `/Root/forklift/S_ForkliftFork/Materials`.
  - **GeomSubset**: Contains subsets for body and fork, indicating complex geometry.
  - **Transforms**: Positioned on the warehouse floor, likely near cardboxes or racks.
- **Role**: Used for transporting cardboxes or pallets, critical for warehouse logistics simulations.
- **Example**:
  - Path: `/Root/forklift/S_ForkliftBody`
  - Material: `/Root/forklift/Materials/*`
  - Description: A forklift with a metallic body and forks for lifting cardboxes.

### Floors
Floors form the warehouse’s ground surface, identified by paths like `/Root/SM_floor*`.

- **Count**: At least 6 (e.g., `SM_floor27` to `SM_floor32`).
- **Properties**:
  - **Geometry**: Each floor is a mesh (`SM_floor02`) with 16 vertices, indicating a simple rectangular plane.
  - **Materials**: Assigned materials like `MI_Floor_01`, `MI_Floor_02b` (concrete or tiled textures).
  - **Hierarchy**: Under `/Root/SM_floor*/SM_floor02`, with `Looks` scope for materials.
- **Role**: Provides the walkable surface for forklifts and robots.
- **Example**:
  - Path: `/Root/SM_floor27/SM_floor02/SM_floor02`
  - Material: `/Root/SM_floor27/SM_floor02/Looks/MI_Floor_01`
  - Description: A concrete floor section, part of the warehouse’s ground plane.

### Ceilings
Ceilings form the warehouse’s roof, identified by paths like `/Root/SM_CeilingA_*`.

- **Count**: At least 6 (e.g., `SM_CeilingA_6X14` to `SM_CeilingA_6X19`).
- **Properties**:
  - **Geometry**: Each ceiling is a mesh (`SM_CeilingA_6X6`) with 4 vertices, indicating a simple plane.
  - **Materials**: Assigned materials like `MI_WallB_01`, `MI_CeilingA_06b` (industrial ceiling textures).
  - **Hierarchy**: Under `/Root/SM_CeilingA_*/SM_CeilingA_6X6`, with `Looks` scope.
- **Role**: Forms the warehouse’s roof, possibly supporting ceiling lights.
- **Example**:
  - Path: `/Root/SM_CeilingA_6X14/SM_CeilingA_6X6/SM_CeilingA_6X6`
  - Material: `/Root/SM_CeilingA_6X14/SM_CeilingA_6X6/Looks/MI_WallB_01`
  - Description: A section of the warehouse ceiling, likely metallic or paneled.

### Walls
Walls define the warehouse’s boundaries and internal partitions, identified by paths like `/Root/SM_WallA_*`.

- **Count**: Multiple (e.g., `SM_WallA_InnerCorner9_88`, `SM_WallA_6M3_94`).
- **Types**:
  - `SM_WallA_InnerCorner`: Corner wall sections.
  - `SM_WallA_6M`, `SM_WallB_6M`: Straight wall sections.
- **Properties**:
  - **Geometry**: Meshes with sections (e.g., `Section0`, `Section1`) for complex walls.
  - **Materials**: Assigned materials like `MI_WallA_01`, `MI_BeamsA_02`, `MI_CeilingA_01`.
  - **Hierarchy**: Under `/Root/SM_WallA_*/SM_Wall*`, with `Looks` scope.
- **Role**: Encloses the warehouse and divides internal spaces.
- **Example**:
  - Path: `/Root/SM_WallA_6M3_94/SM_WallA_6M/SM_WallA_6M/Section0`
  - Material: `/Root/SM_WallA_6M3_94/SM_WallA_6M/Looks/MI_WallA_01`
  - Description: A 6-meter wall section, possibly concrete or metal.

### Lights
Lights illuminate the warehouse, identified by paths like `/Root/SM_LampCeilingA_*` and `/Root/RectLight*`.

- **Count**: 39
- **Types**:
  - `RectLight`: 37 (ceiling-mounted rectangular lights).
  - `DistantLight`: 2 (ambient or directional lights).
- **Properties**:
  - **Hierarchy**: Under `/Root/SM_LampCeilingA_*/RectLight` or direct `/Root/RectLight*`.
  - **Role**: Provides illumination for visibility and rendering.
- **Example**:
  - Path: `/Root/SM_LampCeilingA_15/RectLight`
  - Type: `RectLight`
  - Description: A ceiling-mounted rectangular light, likely fluorescent.

### Cameras
Cameras are used for rendering or simulation viewpoints.

- **Count**: 4
- **Properties**:
  - **Type**: `Camera`
  - **Hierarchy**: Direct children of `/Root` or scattered within the scene.
- **Role**: Captures views for rendering or monitoring warehouse activities.
- **Example**:
  - Path: (Not explicitly listed, but inferred as `/Root/Camera*`)
  - Description: A camera positioned to oversee warehouse operations.

### Racks and Pallets
Racks and pallets support cardboxes, identified by paths like `/Root/SM_RackPile_*`, `/Root/SM_PaletteA_*`.

- **Count**: At least 2 racks (`SM_RackPile_110`, `SM_RackPile_111`), 1 palette (`SM_PaletteA_272`).
- **Properties**:
  - **Materials**: Likely metallic or wooden textures.
  - **Hierarchy**: Under `/Root/SM_RackPile_*` or `/Root/SM_PaletteA_*`.
- **Role**: Organizes cardboxes for storage and access by forklifts.
- **Example**:
  - Path: `/Root/SM_RackPile_110`
  - Description: A rack pile holding multiple cardboxes.

### Navigation Mesh
A navigation mesh supports robotic pathfinding.

- **Count**: 1 (`/Navmesh/NavMeshVolume`)
- **Properties**:
  - **Type**: `NavMeshVolume`
  - **Hierarchy**: Under `/Navmesh`.
- **Role**: Guides forklifts or robots through the warehouse.
- **Example**:
  - Path: `/Navmesh/NavMeshVolume`
  - Description: A volume defining navigable areas for robots.

## Scene Hierarchy
The scene is organized under the default prim `/Root`, with a clear hierarchy:

- **/Root**:
  - **Structural Elements**:
    - `/Root/SM_floor*`: Floor sections.
    - `/Root/SM_CeilingA_*`: Ceiling sections.
    - `/Root/SM_WallA_*`, `/Root/SM_WallB_*`: Wall sections.
  - **Inventory**:
    - `/Root/Box_*`: Cardboxes (e.g., `/Root/Box_42696/SM_CardBoxC_01`).
    - `/Root/forklift`: Forklift with body and fork components.
    - `/Root/SM_RackPile_*`, `/Root/SM_PaletteA_*`: Racks and pallets.
  - **Lighting**:
    - `/Root/SM_LampCeilingA_*/RectLight`: Ceiling lights.
    - `/Root/RectLight*`, `/Root/DistantLight*`: Additional lights.
  - **Navigation**:
    - `/Navmesh/NavMeshVolume`: Navigation mesh.
  - **Other**:
    - `/PhysicsScene`: Physics simulation settings.
    - `/Render`: Rendering settings (e.g., `RenderProduct`, `RenderVar`).

Each object has a `Looks` scope for material assignments, and transforms (`Xform`) organize the hierarchy.

## Statistics
- **Total Prims**: 26,347
- **Meshes**: 3,475
- **Materials**: 11,830
- **Lights**: 39
- **Cameras**: 4
- **Xforms**: 5,617
- **Scopes**: 5,373
- **Other Prims**:
  - `PhysicsScene`: 1
  - `NavMeshVolume`: 1
  - `Plane`: 1 (ground collision plane)
  - `RenderProduct`: 1
  - `RenderVar`: 1
  - `GeomSubset`: 2

## Notes for Querying
- **Cardboxes**: Query by `Box_*`, `SM_CardBox*`, or material names (`MI_CardBox*`) to find specific boxes or their properties.
- **Forklifts**: Query `/Root/forklift` or `S_Forklift*` for details on forklift components or transforms.
- **Structural Elements**: Use `SM_floor*`, `SM_Ceiling*`, `SM_Wall*` for floors, ceilings, or walls.
- **Lights and Cameras**: Query `RectLight`, `DistantLight`, or `Camera` for lighting and viewpoint details.
- **Navigation**: Query `/Navmesh` for robotic pathfinding data.

This document enables an LLM to answer questions about the warehouse scene, such as:
- "How many cardboxes are in the scene?"
- "Where is the forklift located?"
- "What materials are used for the warehouse floor?"
- "Describe the lighting setup."