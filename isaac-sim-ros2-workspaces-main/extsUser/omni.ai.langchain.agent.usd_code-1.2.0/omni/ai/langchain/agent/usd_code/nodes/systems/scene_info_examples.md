Example 1:

> Create a chair next to the table.

```python
print("Found the following chairs and tables:")
for prim_path in usdcode.search_visible_prims_by_name(stage, ["chair", "table"]):
    translate = usdcode.get_translate(stage, prim_path)
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"Prim: {prim_path}, Position: {translate}; World bound {bbox_world}; Local bound {bbox_local}")
```

Example 2:

> Delete the smallest mesh in the current scene.

```python
print("Found the following meshes in the scene:")
for prim_path in usdcode.search_visible_prims_by_type(stage, ["Mesh"]):
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"{prim_path}: World bound {bbox_world}; Local bound {bbox_local}")
```

Example 3:

> Set the closest camera to the sphere as the active camera.

```python
# The user is asking about objects and doesn't provide the exact path. It's very important to find them by BOTH type and name.
print("Found the following cameras and spheres:")
prim_paths = usdcode.search_visible_prims_by_type(stage, ["camera", "sphere"]) + usdcode.search_visible_prims_by_name(stage, ["sphere"])
for prim_path in prim_paths:
    prim = stage.GetPrimAtPath(prim_path)
    xformable = UsdGeom.Xformable(prim)
    transform = xformable.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    translation = Gf.Vec3d(transform.ExtractTranslation())
    rotation_quat = transform.ExtractRotationQuat()
    rotation = Gf.Rotation(rotation_quat)
    angles = rotation.Decompose(Gf.Vec3d(1, 0, 0), Gf.Vec3d(0, 1, 0), Gf.Vec3d(0, 0, 1))
    rotation_vec3 = Gf.Vec3d(angles[0], angles[1], angles[2])
    print(f"Type: {prim.GetTypeName()}, Path: {prim.GetPath()}, World Space Position: {translation}, Rotation: {rotation_vec3}")
```

Example 4:

> Select all the tables

```python
print("Found the following tables:")
print(usdcode.search_visible_prims_by_name(stage, ["table"]))
```

Example 5:

> There is a cube in the scene. Create a copy of this cube.

```python
# The user is asking about objects and doesn't provide the exact path. It's very important to find them by BOTH type and name.
print("Found the following cubes in the scene:")
print(usdcode.search_visible_prims_by_type(stage, ["cube"]))
print(usdcode.search_visible_prims_by_name(stage, ["cube"]))
```

Example 6:

> Place a table on the floor

```python
# Search BOTH table and floor
print("Found the following tables and floors:")
for prim_path in usdcode.search_visible_prims_by_name(stage, ["table", "floor"]):
    translate = usdcode.get_translate(stage, prim_path)
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"Prim: {prim_path}, Position: {translate}; World bound {bbox_world}; Local bound {bbox_local}")
```

Example 7:

> Place a kitchen table on the living room floor

```python
# Search all the possible combination. "kitchen table" cannot be a name because USD doesn't allow spaces in paths
print("Found the following kitchen, table, living room and floor objects:")
for prim_path in usdcode.search_visible_prims_by_name(stage, ["kitchen", "table", "living", "room", "floor"]):
    translate = usdcode.get_translate(stage, prim_path)
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"Prim: {prim_path}, Position: {translate}; World bound {bbox_world}; Local bound {bbox_local}")
```

Example 8:

> Move the sphere up

```python
# The user is asking about objects and doesn't provide the exact path. It's very important to find them by BOTH type and name.
print("Found the following spheres:")
for prim_path in usdcode.search_visible_prims_by_type(stage, ["sphere"]) + usdcode.search_visible_prims_by_name(stage, ["sphere"]):
    translate = usdcode.get_translate(stage, prim_path)
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"Prim: {prim_path}, Position: {translate}; World bound {bbox_world}; Local bound {bbox_local}")
```

Example 9:

> Stack the selected boxes on the selected shelf

```python
# Get selected prims
print("The selection has the following objects:")
selected_prims = usdcode.get_selection()
for prim_path in selected_prims:
    prim = stage.GetPrimAtPath(prim_path)
    translate = usdcode.get_translate(stage, prim_path)
    bbox_world = usdcode.get_bbox_world(stage, prim_path)
    bbox_local = usdcode.get_bbox_local(stage, prim_path)
    print(f"Type: {prim.GetTypeName()}, Path: {prim_path}, Position: {translate}; World bound {bbox_world}; Local bound {bbox_local}")
```
