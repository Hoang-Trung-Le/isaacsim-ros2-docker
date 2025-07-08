from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pxr import Gf, Sdf, Usd, UsdGeom, UsdLux, UsdShade


def get_translate(stage: Usd.Stage, prim_path: str) -> Tuple[float, float, float]:
    """Get the translation for a prim. Animation and keyframes are not supported."""
    if isinstance(prim_path, Usd.Prim):
        # Sometimes it passes a prim instead of a path
        prim = prim_path
    else:
        prim = stage.GetPrimAtPath(prim_path)

    if not prim.IsValid():
        raise ValueError(f"Prim at path {prim_path} does not exist.")

    xformable = UsdGeom.Xformable(prim)
    if not xformable:
        raise ValueError(f"Prim at path {prim_path} is not transformable.")

    translate_ops = [op for op in xformable.GetOrderedXformOps() if op.GetOpType() == UsdGeom.XformOp.TypeTranslate]
    if not translate_ops:
        return (0.0, 0.0, 0.0)

    translate_op = translate_ops[0]
    translation = translate_op.Get(Usd.TimeCode.Default())

    if translation is None:
        # The attribute is there but not assighed a value
        return (0.0, 0.0, 0.0)

    return (translation[0], translation[1], translation[2])


def get_scale(stage: Usd.Stage, prim_path: str) -> Tuple[float, float, float]:
    """Get the scale for a prim. Animation and keyframes are not supported."""
    if isinstance(prim_path, Usd.Prim):
        # Sometimes it passes a prim instead of a path
        prim = prim_path
    else:
        prim = stage.GetPrimAtPath(prim_path)

    if not prim.IsValid():
        raise ValueError(f"Prim at path {prim_path} does not exist.")

    xformable = UsdGeom.Xformable(prim)
    if not xformable:
        raise ValueError(f"Prim at path {prim_path} is not transformable.")

    scale_ops = [op for op in xformable.GetOrderedXformOps() if op.GetOpType() == UsdGeom.XformOp.TypeScale]
    if not scale_ops:
        return (1.0, 1.0, 1.0)

    scale_op = scale_ops[0]
    scale = scale_op.Get(Usd.TimeCode.Default())

    if scale is None:
        # The attribute is there but not assighed a value
        return (1.0, 1.0, 1.0)

    return (scale[0], scale[1], scale[2])


def get_rotate(stage: Usd.Stage, prim_path: str) -> Tuple[float, float, float]:
    """Get the rotation for a prim. Animation and keyframes are not supported."""
    if isinstance(prim_path, Usd.Prim):
        # Sometimes it passes a prim instead of a path
        prim = prim_path
    else:
        prim = stage.GetPrimAtPath(prim_path)

    if not prim.IsValid():
        raise ValueError(f"Prim at path {prim_path} does not exist.")

    xformable = UsdGeom.Xformable(prim)
    if not xformable:
        raise ValueError(f"Prim at path {prim_path} is not transformable.")

    rotation_ops = [
        op
        for op in xformable.GetOrderedXformOps()
        if op.GetOpType()
        in [
            UsdGeom.XformOp.TypeRotateX,
            UsdGeom.XformOp.TypeRotateY,
            UsdGeom.XformOp.TypeRotateZ,
            UsdGeom.XformOp.TypeRotateXYZ,
            UsdGeom.XformOp.TypeRotateXZY,
            UsdGeom.XformOp.TypeRotateYXZ,
            UsdGeom.XformOp.TypeRotateYZX,
            UsdGeom.XformOp.TypeRotateZXY,
            UsdGeom.XformOp.TypeRotateZYX,
        ]
    ]

    if not rotation_ops:
        return (0.0, 0.0, 0.0)

    # Assuming the prim has a single rotate operation in Euler angles or composite rotate
    rotation_op = rotation_ops[0]
    rotation = rotation_op.Get(Usd.TimeCode.Default())

    if rotation is None:
        # The attribute is there but not assighed a value
        return (0.0, 0.0, 0.0)

    return (rotation[0], rotation[1], rotation[2])


def get_bbox_world(stage: Usd.Stage, prim_path: str, time: Usd.TimeCode = Usd.TimeCode.Default()) -> Gf.Range2d:
    """Get the world space bounding box of a prim."""
    if isinstance(prim_path, Usd.Prim):
        # Sometimes it passes a prim instead of a path
        prim = prim_path
    else:
        prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        raise ValueError(f"Prim not found at path: {prim_path}")

    bbox_cache = UsdGeom.BBoxCache(time, includedPurposes=[UsdGeom.Tokens.default_])
    bbox_world = bbox_cache.ComputeWorldBound(prim)
    return bbox_world.ComputeAlignedRange()


def get_bbox_local(stage: Usd.Stage, prim_path: str, time: Usd.TimeCode = Usd.TimeCode.Default()) -> Gf.Range2d:
    """Get the local space bounding box of a prim."""
    if isinstance(prim_path, Usd.Prim):
        # Sometimes it passes a prim instead of a path
        prim = prim_path
    else:
        prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        raise ValueError(f"Prim not found at path: {prim_path}")

    bbox_cache = UsdGeom.BBoxCache(time, includedPurposes=[UsdGeom.Tokens.default_])
    bbox_local = bbox_cache.ComputeLocalBound(prim)
    return bbox_local.GetRange()


def filter_valid_and_visible(prim: Usd.Prim) -> bool:
    """
    Filter function to use in search_prims_by_type and search_prims_by_name that returns True if the prim is valid and visible.
    """
    if not prim.IsValid():
        return False
    imageable = UsdGeom.Imageable(prim)
    if imageable:
        return imageable.ComputeVisibility() == UsdGeom.Tokens.inherited
    return True


def search_prims_by_type(
    stage: Usd.Stage,
    types: List[str],
    filter_func: Optional[Callable[[Usd.Prim], bool]] = None,
    prune_subtree: bool = False,
) -> List[str]:
    """
    Iterates over all prims in the stage and returns the paths of prims that match the given types.
    Optionally, a custom filter function can be provided, and pruning of subtrees can be enabled.

    This function is 100% compatible with the original behavior when `filter_func` and `prune_subtree` are not provided.

    Attention: "Box" is not a type in USD, it is a shape. The type is "Xform" or "Mesh".

    Args:
        stage (Usd.Stage): The stage to traverse.
        types (List[str]): A list of type names to match against the prims' types.
        filter_func (Callable[[Usd.Prim], bool], optional): An optional function that takes a `Usd.Prim` and returns `True` if the prim should be included. Defaults to `None`.
        prune_subtree (bool, optional): If `True`, and `filter_func` is provided, when `filter_func(prim)` returns `False`, its children are not traversed. Defaults to `False`.

    Returns:
        List[str]: A list of paths of prims that match the types (and optionally pass the filter function).
    """
    result = []
    iterator = iter(stage.TraverseAll())
    for prim in iterator:
        match_type = any(t.lower() in prim.GetTypeName().lower() for t in types)
        match_filter = filter_func(prim) if filter_func else True

        if match_type and match_filter:
            result.append(str(prim.GetPath()))
        if not match_filter and prune_subtree:
            iterator.PruneChildren()
    return result


def search_prims_by_name(
    stage: Usd.Stage,
    names: List[str],
    filter_func: Optional[Callable[[Usd.Prim], bool]] = None,
    prune_subtree: bool = False,
    return_only_xformable: bool = False,
) -> List[str]:
    """
    Iterates over all prims in the stage and returns the paths of prims that match the given names.
    Optionally, a custom filter function can be provided, and pruning of subtrees can be enabled.

    This function is 100% compatible with the original behavior when `filter_func` and `prune_subtree` are not provided.

    Args:
        stage (Usd.Stage): The stage to traverse.
        names (List[str]): A list of names to match against the prims' names.
        filter_func (Callable[[Usd.Prim], bool], optional): An optional function that takes a `Usd.Prim` and returns `True` if the prim should be included. Defaults to `None`.
        prune_subtree (bool, optional): If `True`, and `filter_func` is provided, when `filter_func(prim)` returns `False`, its children are not traversed. Defaults to `False`.
        return_only_xformable (bool, optional): If `True`, only returns prims that are `UsdGeom.Xformable`. Defaults to `False`.

    Returns:
        List[str]: A list of paths of prims that match the names (and optionally pass the filter function).
    """
    result = []
    iterator = iter(stage.TraverseAll())
    for prim in iterator:
        match_name = any(name.lower() in prim.GetName().lower() for name in names)
        match_filter = filter_func(prim) if filter_func else True
        xformable = not return_only_xformable or UsdGeom.Xformable(prim)

        if match_name and match_filter and xformable:
            result.append(str(prim.GetPath()))
        if not match_filter and prune_subtree:
            iterator.PruneChildren()
    return result


def search_visible_prims_by_type(
    stage: Usd.Stage,
    types: List[str],
) -> List[str]:
    """
    Iterates over all prims in the stage and returns the paths of prims that match the given types and are visible.

    Attention: "Box" is not a type in USD, it is a shape. The type is "Xform" or "Mesh".

    Args:
        stage (Usd.Stage): The stage to traverse.
        types (List[str]): A list of type names to match against the prims' types.

    Returns:
        List[str]: A list of paths of prims that match the types and are visible.
    """
    return search_prims_by_type(stage, types, filter_valid_and_visible, True)


def search_visible_prims_by_name(
    stage: Usd.Stage,
    names: List[str],
) -> List[str]:
    """
    Iterates over all prims in the stage and returns the paths of prims that match the given names and are visible.

    Args:
        stage (Usd.Stage): The stage to traverse.
        names (List[str]): A list of names to match against the prims' names.

    Returns:
        List[str]: A list of paths of prims that match the names and are visible.
    """
    return search_prims_by_name(stage, names, filter_valid_and_visible, True, True)


def get_selection() -> List[str]:
    import omni.usd

    usd_context = omni.usd.get_context()
    selection = usd_context.get_selection()
    return selection.get_selected_prim_paths()


def get_current_camera_path() -> str:
    import omni.kit.viewport

    viewport = omni.kit.viewport.utility.get_active_viewport()
    return str(viewport.get_active_camera())


def get_camera_directions(stage: Usd.Stage, camera_path: Optional[str] = None) -> Dict[str, Tuple[float, float, float]]:
    """
    Returns the direction vectors (left, right, up, down) relative to the specified USD camera.

    Parameters:
    - stage (Usd.Stage): The USD stage containing the camera.
    - camera_path (str): The SdfPath of the camera in the stage. If None, uses the current camera.

    Returns:
    - dict: A dictionary containing the direction vectors with keys 'left', 'right', 'up', 'down', 'forward', 'backward'.
    """
    # If stage is None, get the current stage
    if stage is None:
        raise ValueError("Stage is not specified.")

    # If camera_path is None, get it from get_current_camera()
    if camera_path is None:
        camera_path = get_current_camera_path()
        if not camera_path:
            raise ValueError("Unable to obtain the current camera path.")

    # Get the camera prim
    camera = stage.GetPrimAtPath(camera_path)
    if not camera:
        raise ValueError(f"Camera not found at path {camera_path}")

    # Get the camera's transformation matrix at the default time
    time = Usd.TimeCode.Default()
    camera_xform = UsdGeom.Xformable(camera)
    world_transform = camera_xform.ComputeLocalToWorldTransform(time)

    # Extract the rotation matrix (upper-left 3x3 part of the 4x4 matrix)
    rotation_matrix = world_transform.ExtractRotationMatrix()

    # Define the camera's local axes (right, up, forward) in camera space
    local_right = Gf.Vec3d(1, 0, 0)
    local_up = Gf.Vec3d(0, 1, 0)
    local_forward = Gf.Vec3d(0, 0, -1)  # Cameras in USD look along the negative Z-axis

    # Transform the local axes to world space using the rotation matrix
    right_vector = local_right * rotation_matrix
    up_vector = local_up * rotation_matrix
    forward_vector = local_forward * rotation_matrix

    # Compute the left and down vectors by negating the right and up vectors
    left_vector = -right_vector
    down_vector = -up_vector
    backward_vector = -forward_vector

    # Normalize them
    left_vector.Normalize()
    right_vector.Normalize()
    up_vector.Normalize()
    down_vector.Normalize()
    forward_vector.Normalize()
    backward_vector.Normalize()

    # Return the direction vectors as a dictionary
    return {
        "left": (left_vector[0], left_vector[1], left_vector[2]),
        "right": (right_vector[0], right_vector[1], right_vector[2]),
        "up": (up_vector[0], up_vector[1], up_vector[2]),
        "down": (down_vector[0], down_vector[1], down_vector[2]),
        "forward": (forward_vector[0], forward_vector[1], forward_vector[2]),
        "backward": (backward_vector[0], backward_vector[1], backward_vector[2]),
    }


def get_camera_direction_left(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the left of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["left"]


def get_camera_direction_right(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the right of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["right"]


def get_camera_direction_up(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the up of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["up"]


def get_camera_direction_down(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the down of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["down"]


def get_camera_direction_forward(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the forward of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["forward"]


def get_camera_direction_backward(stage: Usd.Stage, camera_path: Optional[str] = None) -> Tuple[float, float, float]:
    """
    Returns the direction vectors relative to the backward of the specified USD camera.
    """
    return get_camera_directions(stage, camera_path)["backward"]


def get_direction_up(stage: Usd.Stage) -> Tuple[float, float, float]:
    """
    Returns the up vector for the stage considering its up axis.
    """
    up_axis = UsdGeom.GetStageUpAxis(stage) or "Y"
    if up_axis == "X":
        return (1.0, 0.0, 0.0)
    if up_axis == "Z":
        return (0.0, 0.0, 1.0)
    return (0.0, 1.0, 0.0)


def get_direction_down(stage: Usd.Stage) -> Tuple[float, float, float]:
    """
    Returns the down vector for the stage considering its up axis.
    """
    up_axis = UsdGeom.GetStageUpAxis(stage) or "Y"
    if up_axis == "X":
        return (-1.0, 0.0, 0.0)
    if up_axis == "Z":
        return (0.0, 0.0, -1.0)
    return (0.0, -1.0, 0.0)


def get_assigned_material(stage: Usd.Stage, prim_path: str) -> Optional[UsdShade.Material]:
    """
    Get the assigned material for a given prim.

    Args:
        stage (Usd.Stage): The USD stage containing the prim.
        prim_path (str): The path to the prim.

    Returns:
        Optional[UsdShade.Material]: The assigned material, or None if no material is assigned.
    """
    prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        return None

    binding_api = UsdShade.MaterialBindingAPI(prim)
    material, _ = binding_api.ComputeBoundMaterial()

    return material


def get_prim_color(
    stage: Usd.Stage, prim_path: str, color_attribute: str = "diffuse_reflection_color"
) -> Optional[Tuple[float, float, float]]:
    """
    Get the color of a prim, first checking for an assigned material, then falling back to display color.

    Args:
        stage (Usd.Stage): The USD stage containing the prim.
        prim_path (str): The path to the prim.
        color_attribute (str): The name of the color attribute to retrieve from the material (default: "diffuse_reflection_color").

    Returns:
        Optional[Tuple[float, float, float]]: The color as an RGB tuple, or None if no color is found.
    """
    prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        return None

    # First, try to get color from assigned material
    material = UsdShade.MaterialBindingAPI(prim).GetDirectBinding().GetMaterial()
    if material:
        shader = material.GetPrim().GetChild("Shader")
        if shader:
            color_input = shader.GetAttribute(f"inputs:{color_attribute}")
            if color_input:
                color_value = color_input.Get()
                if color_value is not None:
                    return tuple(color_value)

    # If no material color found, try to get display color
    gprim = UsdGeom.Gprim(prim)
    if gprim:
        display_color_attr = gprim.GetDisplayColorAttr()
        if display_color_attr:
            display_colors = display_color_attr.Get()
            if display_colors and len(display_colors) > 0:
                return tuple(display_colors[0])

    # If no color found, return None
    return None


def list_variants(stage: Usd.Stage, prim: Union[Usd.Prim, str], variant_set_name: str):
    """
    Lists all variant names available in a variant set on the specified prim.

    Parameters:
        stage (Usd.Stage): The USD stage to operate on.
        prim (Union[Usd.Prim, str]): The USD prim containing the variant set.
        variant_set_name (str): The name of the variant set.

    Returns:
        List[str]: A list of variant names.
    """
    if isinstance(prim, str) or isinstance(prim, Sdf.Path):
        prim = stage.GetPrimAtPath(prim)

    variant_sets = prim.GetVariantSets()
    variant_set = variant_sets.GetVariantSet(variant_set_name)
    if variant_set:
        return variant_set.GetVariantNames()
    else:
        raise ValueError(f"Variant set '{variant_set_name}' does not exist on prim '{prim.GetPath()}'.")


def get_current_variant_selection(stage: Usd.Stage, prim: Union[Usd.Prim, str], variant_set_name: str):
    """
    Retrieves the currently selected variant name from a variant set on the specified prim.

    Parameters:
        stage (Usd.Stage): The USD stage to operate on.
        prim (Union[Usd.Prim, str]): The USD prim containing the variant set.
        variant_set_name (str): The name of the variant set.

    Returns:
        str: The name of the currently selected variant, or None if no selection is made.
    """
    if isinstance(prim, str) or isinstance(prim, Sdf.Path):
        prim = stage.GetPrimAtPath(prim)

    variant_sets = prim.GetVariantSets()
    variant_set = variant_sets.GetVariantSet(variant_set_name)
    if variant_set:
        return variant_set.GetVariantSelection()
    else:
        raise ValueError(f"Variant set '{variant_set_name}' does not exist on prim '{prim.GetPath()}'.")


def get_variant_sets(stage: Usd.Stage, prim: Union[Usd.Prim, str]):
    """
    Returns a dictionary of variant sets on the specified prim.

    Parameters:
        stage (Usd.Stage): The USD stage to operate on.
        prim (Usd.Prim): The USD prim from which to retrieve variant sets.

    Returns:
        dict: A dictionary where keys are variant set names and values are lists of variant names.
    """
    if isinstance(prim, str) or isinstance(prim, Sdf.Path):
        prim = stage.GetPrimAtPath(prim)

    variant_sets = prim.GetVariantSets()
    variant_set_names = variant_sets.GetNames()
    variant_sets_dict = {}
    for vs_name in variant_set_names:
        vs = variant_sets.GetVariantSet(vs_name)
        variant_names = vs.GetVariantNames()
        variant_sets_dict[vs_name] = variant_names
    return variant_sets_dict
