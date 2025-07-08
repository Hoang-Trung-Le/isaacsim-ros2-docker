from pxr import Usd, UsdGeom, UsdShade, UsdLux, UsdPhysics, Gf, Sdf
import omni.usd
import carb
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
import json
import os
from collections import defaultdict

class SceneScanner:
    """
    Advanced USD scene scanner that extracts rich natural descriptions of scene components
    for consumption by LLM models in the Ivyverse extension.
    """
    
    def __init__(self):
        self._usd_context = omni.usd.get_context()
        self._stage = None
        self._prim_cache = {}
        self._material_cache = {}
        self._scan_time = None
    
    def scan_scene(self, detailed: bool = True) -> Dict[str, Any]:
        """
        Performs a comprehensive scan of the current USD stage and returns information
        in a format optimized for LLM consumption.
        
        Args:
            detailed: Whether to include detailed attribute information for each prim
            
        Returns:
            Dictionary containing hierarchical scene information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            carb.log_warn("No stage is loaded")
            return {"error": "No stage is loaded"}
        
        self._prim_cache = {}
        self._material_cache = {}
        self._scan_time = self._stage.GetTimeCode()
        
        scene_info = {
            "scene_metadata": self._extract_scene_metadata(),
            "scene_summary": self._generate_scene_summary(),
            "scene_hierarchy": self._extract_hierarchy(),
            "physics_setup": self._extract_physics(),
            "material_library": self._extract_materials(),
            "lighting_setup": self._extract_lighting(),
            "camera_setup": self._extract_cameras(),
            "special_prims": self._extract_special_prims(),
        }
        
        if detailed:
            scene_info["detailed_prims"] = self._extract_detailed_prim_info()
            
        return scene_info
    
    def get_prim_info(self, prim_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific prim
        
        Args:
            prim_path: USD path to the desired prim
            
        Returns:
            Dictionary containing detailed prim information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            return {"error": "No stage is loaded"}
            
        prim = self._stage.GetPrimAtPath(prim_path)
        if not prim:
            return {"error": f"No prim found at path: {prim_path}"}
            
        return self._extract_prim_data(prim, detailed=True)
    
    def get_natural_scene_description(self) -> str:
        """
        Generate a natural language description of the current scene
        
        Returns:
            String containing a natural language description of the scene
        """
        scene_data = self.scan_scene(detailed=False)
        
        # Extract key metrics
        meta = scene_data["scene_metadata"]
        summary = scene_data["scene_summary"]
        
        # Generate natural description
        description = f"""
This USD scene '{os.path.basename(meta.get('file_name', 'Untitled'))}' contains {summary['total_prims']} prims organized in a hierarchy.

The scene contains:
- {summary.get('mesh_count', 0)} meshes/geometric objects
- {summary.get('material_count', 0)} materials
- {summary.get('light_count', 0)} light sources
- {summary.get('camera_count', 0)} cameras
- {summary.get('physics_prims', 0)} physics-enabled objects

The world bounds span from {meta.get('bounds_min', 'unknown')} to {meta.get('bounds_max', 'unknown')}.

Main objects in the scene:
"""
        
        # Add important prims by type
        if scene_data.get("special_prims", {}).get("important_objects"):
            for obj in scene_data["special_prims"]["important_objects"][:10]:  # Limit to 10
                description += f"- {obj['path']}: {obj['type']}"
                if "semantic_label" in obj:
                    description += f" (labeled as '{obj['semantic_label']}')"
                description += "\n"
        
        # Add physics information
        if scene_data.get("physics_setup", {}).get("enabled", False):
            description += "\nThe scene has physics enabled with "
            description += f"gravity set to {scene_data['physics_setup'].get('gravity', 'default')}. "
            description += f"There are {scene_data['physics_setup'].get('rigid_body_count', 0)} rigid bodies "
            description += f"and {scene_data['physics_setup'].get('collider_count', 0)} colliders.\n"
        
        return description
    
    def search_prims(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for prims matching a query string in name or type
        
        Args:
            query: Search string to match against prim names or types
            
        Returns:
            List of matching prims with their information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            return [{"error": "No stage is loaded"}]
            
        query = query.lower()
        results = []
        
        for prim in self._stage.Traverse():
            path = str(prim.GetPath())
            prim_type = prim.GetTypeName()
            
            if query in path.lower() or query in str(prim_type).lower():
                results.append(self._extract_prim_data(prim, detailed=False))
                
        return results
    
    def _extract_scene_metadata(self) -> Dict[str, Any]:
        """Extract high-level scene metadata"""
        metadata = {
            "file_name": self._stage.GetRootLayer().GetDisplayName(),
            "default_prim": str(self._stage.GetDefaultPrim().GetPath()) if self._stage.GetDefaultPrim() else "None",
            "up_axis": UsdGeom.GetStageUpAxis(self._stage),
            "meters_per_unit": UsdGeom.GetStageMetersPerUnit(self._stage),
            "time_code_range": (self._stage.GetStartTimeCode(), self._stage.GetEndTimeCode()),
            "current_time_code": self._stage.GetTimeCode(),
        }
        
        # Get world bounds
        bboxcache = UsdGeom.BBoxCache(self._scan_time, ['default', 'render'])
        bounds = bboxcache.ComputeWorldBound(self._stage.GetPseudoRoot())
        if isinstance(bounds, UsdGeom.BBox3d):
            min_extent = bounds.GetBox().GetMin()
            max_extent = bounds.GetBox().GetMax()
            metadata["bounds_min"] = f"({min_extent[0]:.2f}, {min_extent[1]:.2f}, {min_extent[2]:.2f})"
            metadata["bounds_max"] = f"({max_extent[0]:.2f}, {max_extent[1]:.2f}, {max_extent[2]:.2f})"
            metadata["bounds_size"] = f"({max_extent[0] - min_extent[0]:.2f} × {max_extent[1] - min_extent[1]:.2f} × {max_extent[2] - min_extent[2]:.2f})"
        
        return metadata
    
    def _generate_scene_summary(self) -> Dict[str, Any]:
        """Generate numerical summary of scene contents"""
        summary = {}
        
        # Count by primitive type
        all_prims = list(self._stage.Traverse())
        summary["total_prims"] = len(all_prims)
        
        type_counts = defaultdict(int)
        for prim in all_prims:
            type_counts[prim.GetTypeName()] += 1
        summary["prim_types"] = {str(k): v for k, v in type_counts.items() if k}
        
        # Count specific important types
        summary["mesh_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Mesh))
        summary["material_count"] = sum(1 for prim in all_prims if prim.IsA(UsdShade.Material))
        summary["light_count"] = sum(1 for prim in all_prims if prim.IsA(UsdLux.Light))
        summary["camera_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Camera))
        summary["xform_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Xform) and not prim.IsA(UsdGeom.Camera))
        summary["physics_prims"] = sum(1 for prim in all_prims if prim.HasAPI(UsdPhysics.RigidBodyAPI) or prim.HasAPI(UsdPhysics.CollisionAPI))
        
        # Layer analysis
        summary["layer_stack_count"] = len(self._stage.GetLayerStack())
        
        return summary
    
    def _extract_hierarchy(self) -> Dict[str, Any]:
        """Extract scene hierarchy information"""
        def build_hierarchy(prim):
            if not prim:
                return None
                
            children = {}
            for child in prim.GetFilteredChildren(Usd.PrimIsDefined and not Usd.PrimIsAbstract):
                children[child.GetName()] = build_hierarchy(child)
                
            return {
                "type": str(prim.GetTypeName()),
                "path": str(prim.GetPath()),
                "metadata": self._get_important_metadata(prim),
                "children": children
            }
            
        # Start from root or default prim
        default_prim = self._stage.GetDefaultPrim()
        root = default_prim if default_prim else self._stage.GetPseudoRoot()
        
        return build_hierarchy(root)
    
    def _extract_physics(self) -> Dict[str, Any]:
        """Extract physics setup information"""
        physics_info = {
            "enabled": False,
            "gravity": "9.8 m/s² (default)",
            "rigid_body_count": 0,
            "collider_count": 0,
            "joints": []
        }
        
        # Check for physics scene
        physics_scene = None
        for prim in self._stage.Traverse():
            if prim.IsA(UsdPhysics.Scene):
                physics_scene = prim
                physics_info["enabled"] = True
                break
                
        # Get gravity
        if physics_scene:
            gravity_attr = UsdPhysics.Scene(physics_scene).GetGravityDirectionAttr()
            magnitude_attr = UsdPhysics.Scene(physics_scene).GetGravityMagnitudeAttr()
            if gravity_attr and gravity_attr.IsValid() and magnitude_attr and magnitude_attr.IsValid():
                direction = gravity_attr.Get(self._scan_time)
                magnitude = magnitude_attr.Get(self._scan_time)
                if direction is not None and magnitude is not None:
                    physics_info["gravity"] = f"{magnitude} m/s² in direction ({direction[0]}, {direction[1]}, {direction[2]})"
        
        # Count physics objects
        rigid_bodies = []
        colliders = []
        joints = []
        
        for prim in self._stage.Traverse():
            if prim.HasAPI(UsdPhysics.RigidBodyAPI):
                rigid_bodies.append(str(prim.GetPath()))
                
            if prim.HasAPI(UsdPhysics.CollisionAPI) or prim.IsA(UsdPhysics.CollisionAPI):
                colliders.append(str(prim.GetPath()))
                
            if prim.IsA(UsdPhysics.Joint):
                joints.append({
                    "path": str(prim.GetPath()),
                    "type": str(prim.GetTypeName()),
                    "body0": UsdPhysics.Joint(prim).GetBody0Rel().GetTargets()[0] if UsdPhysics.Joint(prim).GetBody0Rel().GetTargets() else "",
                    "body1": UsdPhysics.Joint(prim).GetBody1Rel().GetTargets()[0] if UsdPhysics.Joint(prim).GetBody1Rel().GetTargets() else ""
                })
        
        physics_info["rigid_body_count"] = len(rigid_bodies)
        physics_info["collider_count"] = len(colliders)
        physics_info["rigid_bodies"] = rigid_bodies[:20] if len(rigid_bodies) <= 20 else rigid_bodies[:20] + [f"... {len(rigid_bodies) - 20} more"]
        physics_info["colliders"] = colliders[:20] if len(colliders) <= 20 else colliders[:20] + [f"... {len(colliders) - 20} more"]
        physics_info["joints"] = joints[:20] if len(joints) <= 20 else joints[:20] + [{"note": f"{len(joints) - 20} more joints"}]
        
        return physics_info
    
    def _extract_materials(self) -> Dict[str, Any]:
        """Extract material information"""
        materials = {}
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdShade.Material):
                mat_path = str(prim.GetPath())
                mat_data = self._extract_material_data(prim)
                materials[mat_path] = mat_data
                self._material_cache[mat_path] = mat_data
                
        # Also extract material bindings for all meshes
        binding_info = []
        for prim in self._stage.Traverse():
            if prim.IsA(UsdGeom.Mesh) or prim.IsA(UsdGeom.Scope):
                bindingAPI = UsdShade.MaterialBindingAPI(prim)
                if bindingAPI:
                    direct_binding = bindingAPI.GetDirectBinding().GetMaterial()
                    if direct_binding:
                        binding_info.append({
                            "prim_path": str(prim.GetPath()),
                            "material_path": str(direct_binding.GetPath())
                        })
        
        return {
            "materials": materials,
            "bindings": binding_info[:30]  # Limit to 30 bindings
        }
    
    def _extract_lighting(self) -> Dict[str, Any]:
        """Extract lighting setup information"""
        lights = []
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdLux.Light):
                light_data = {
                    "path": str(prim.GetPath()),
                    "type": str(prim.GetTypeName()),
                    "enabled": UsdLux.Light(prim).GetEnableColorTemperatureAttr().Get(self._scan_time) if UsdLux.Light(prim).GetEnableColorTemperatureAttr() else True,
                }
                
                # Extract common light attributes
                light_schema = UsdLux.Light(prim)
                
                intensity_attr = light_schema.GetIntensityAttr()
                if intensity_attr and intensity_attr.IsValid():
                    light_data["intensity"] = intensity_attr.Get(self._scan_time)
                    
                exposure_attr = light_schema.GetExposureAttr()
                if exposure_attr and exposure_attr.IsValid():
                    light_data["exposure"] = exposure_attr.Get(self._scan_time)
                    
                color_attr = light_schema.GetColorAttr()
                if color_attr and color_attr.IsValid():
                    color = color_attr.Get(self._scan_time)
                    light_data["color"] = f"({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})"
                    
                # Extract type-specific attributes
                if prim.IsA(UsdLux.DistantLight):
                    angle_attr = UsdLux.DistantLight(prim).GetAngleAttr()
                    if angle_attr and angle_attr.IsValid():
                        light_data["angle"] = angle_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.DiskLight) or prim.IsA(UsdLux.SphereLight):
                    radius_attr = (UsdLux.DiskLight(prim) if prim.IsA(UsdLux.DiskLight) else UsdLux.SphereLight(prim)).GetRadiusAttr()
                    if radius_attr and radius_attr.IsValid():
                        light_data["radius"] = radius_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.RectLight):
                    width_attr = UsdLux.RectLight(prim).GetWidthAttr()
                    height_attr = UsdLux.RectLight(prim).GetHeightAttr()
                    if width_attr and width_attr.IsValid() and height_attr and height_attr.IsValid():
                        light_data["width"] = width_attr.Get(self._scan_time)
                        light_data["height"] = height_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.CylinderLight):
                    length_attr = UsdLux.CylinderLight(prim).GetLengthAttr()
                    radius_attr = UsdLux.CylinderLight(prim).GetRadiusAttr()
                    if length_attr and length_attr.IsValid() and radius_attr and radius_attr.IsValid():
                        light_data["length"] = length_attr.Get(self._scan_time)
                        light_data["radius"] = radius_attr.Get(self._scan_time)
                
                # Add transform
                xformable = UsdGeom.Xformable(prim)
                if xformable:
                    matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                    light_data["position"] = self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation()))
                
                lights.append(light_data)
        
        return {
            "lights": lights,
            "dome_light": self._extract_dome_light()
        }
    
    def _extract_dome_light(self) -> Optional[Dict[str, Any]]:
        """Extract dome light information if present"""
        for prim in self._stage.Traverse():
            if prim.IsA(UsdLux.DomeLight):
                dome_light = UsdLux.DomeLight(prim)
                dome_data = {
                    "path": str(prim.GetPath()),
                    "enabled": dome_light.GetEnableColorTemperatureAttr().Get(self._scan_time) if dome_light.GetEnableColorTemperatureAttr() else True,
                }
                
                texture_attr = dome_light.GetTextureFileAttr()
                if texture_attr and texture_attr.IsValid():
                    dome_data["texture"] = texture_attr.Get(self._scan_time)
                    
                exposure_attr = dome_light.GetExposureAttr()
                if exposure_attr and exposure_attr.IsValid():
                    dome_data["exposure"] = exposure_attr.Get(self._scan_time)
                    
                intensity_attr = dome_light.GetIntensityAttr()
                if intensity_attr and intensity_attr.IsValid():
                    dome_data["intensity"] = intensity_attr.Get(self._scan_time)
                    
                return dome_data
                
        return None
    
    def _extract_cameras(self) -> List[Dict[str, Any]]:
        """Extract camera information"""
        cameras = []
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdGeom.Camera):
                camera = UsdGeom.Camera(prim)
                
                # Basic camera info
                camera_data = {
                    "path": str(prim.GetPath()),
                    "active": "activeCamera" in [token.GetString() for token in prim.GetPropertyNames()]
                }
                
                # Get projection
                projection_attr = camera.GetProjectionAttr()
                if projection_attr and projection_attr.IsValid():
                    camera_data["projection"] = projection_attr.Get(self._scan_time)
                
                # Get focal length
                focal_attr = camera.GetFocalLengthAttr()
                if focal_attr and focal_attr.IsValid():
                    camera_data["focal_length"] = focal_attr.Get(self._scan_time)
                
                # Get horizontal aperture
                h_aperture_attr = camera.GetHorizontalApertureAttr()
                if h_aperture_attr and h_aperture_attr.IsValid():
                    camera_data["horizontal_aperture"] = h_aperture_attr.Get(self._scan_time)
                
                # Get vertical aperture
                v_aperture_attr = camera.GetVerticalApertureAttr()
                if v_aperture_attr and v_aperture_attr.IsValid():
                    camera_data["vertical_aperture"] = v_aperture_attr.Get(self._scan_time)
                
                # Get clipping range
                clipping_attr = camera.GetClippingRangeAttr()
                if clipping_attr and clipping_attr.IsValid():
                    clip_range = clipping_attr.Get(self._scan_time)
                    camera_data["clipping_range"] = f"{clip_range[0]} to {clip_range[1]}"
                
                # Add transform
                xformable = UsdGeom.Xformable(prim)
                if xformable:
                    matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                    camera_data["position"] = self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation()))
                    
                    # Decompose rotation
                    rotation = matrix.ExtractRotation()
                    camera_data["forward"] = self._format_vec3(rotation.TransformDir(Gf.Vec3d(0, 0, -1)))
                    camera_data["up"] = self._format_vec3(rotation.TransformDir(Gf.Vec3d(0, 1, 0)))
                
                cameras.append(camera_data)
        
        return cameras
    
    def _extract_special_prims(self) -> Dict[str, Any]:
        """Extract information about special prims like references, instances, etc."""
        special_prims = {
            "references": [],
            "instances": [],
            "variants": [],
            "important_objects": [],
        }
        
        # Find large meshes or objects with semantic information
        for prim in self._stage.Traverse():
            # Check for references
            if prim.HasAuthoredReferences():
                refs = prim.GetReferences()
                ref_list = []
                for i in range(refs.GetNumReferences()):
                    ref = refs.GetItemForEdit(i)
                    ref_list.append(str(ref.GetAssetPath()))
                    
                if ref_list:
                    special_prims["references"].append({
                        "path": str(prim.GetPath()),
                        "references": ref_list
                    })
            
            # Check for instances
            if prim.IsInstanceable() and prim.IsInstance():
                special_prims["instances"].append({
                    "path": str(prim.GetPath()),
                    "master": str(prim.GetMaster().GetPath()) if prim.GetMaster() else "unknown"
                })
            
            # Check for variants
            if prim.HasVariantSets():
                variant_sets = prim.GetVariantSets()
                all_sets = variant_sets.GetNames()
                
                var_data = {
                    "path": str(prim.GetPath()),
                    "variant_sets": {}
                }
                
                for set_name in all_sets:
                    var_set = variant_sets.GetVariantSet(set_name)
                    var_data["variant_sets"][set_name] = {
                        "variants": var_set.GetVariantNames(),
                        "selected": var_set.GetVariantSelection()
                    }
                    
                special_prims["variants"].append(var_data)
            
            # Identify important objects
            importance_score = 0
            
            # Score geometric complexity
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)
                point_count_attr = mesh.GetPointsAttr()
                if point_count_attr and point_count_attr.IsValid():
                    points = point_count_attr.Get(self._scan_time)
                    if points is not None:
                        point_count = len(points)
                        importance_score += min(point_count / 1000, 10)  # Cap at 10 points
            
            # Score by transformations
            if prim.IsA(UsdGeom.Xformable):
                xformable = UsdGeom.Xformable(prim)
                if xformable.TransformMightBeTimeVarying():
                    importance_score += 5  # Animated objects are important
            
            # Score by semantic type
            if prim.HasAttribute("semanticType") or prim.HasAttribute("kind"):
                importance_score += 3
                
                semantic_type = None
                if prim.HasAttribute("semanticType"):
                    semantic_attr = prim.GetAttribute("semanticType")
                    if semantic_attr.IsValid():
                        semantic_type = semantic_attr.Get(self._scan_time)
                elif prim.HasAttribute("kind"):
                    kind_attr = prim.GetAttribute("kind")
                    if kind_attr.IsValid():
                        semantic_type = kind_attr.Get(self._scan_time)
                
                if importance_score >= 2:
                    obj_info = {
                        "path": str(prim.GetPath()),
                        "type": str(prim.GetTypeName()),
                        "importance_score": importance_score
                    }
                    
                    if semantic_type:
                        obj_info["semantic_label"] = semantic_type
                        
                    special_prims["important_objects"].append(obj_info)
        
        # Sort important objects by score
        special_prims["important_objects"] = sorted(
            special_prims["important_objects"], 
            key=lambda x: x["importance_score"], 
            reverse=True
        )
        
        return special_prims
    
    def _extract_detailed_prim_info(self) -> Dict[str, Dict[str, Any]]:
        """Extract detailed information for important prims"""
        detailed_prims = {}
        
        # Process a reasonable number of prims to avoid overwhelming the LLM
        count = 0
        MAX_DETAILED_PRIMS = 100
        
        for prim in self._stage.Traverse():
            # Skip prims that aren't interesting
            if not (prim.IsA(UsdGeom.Mesh) or 
                    prim.IsA(UsdGeom.Camera) or 
                    prim.IsA(UsdLux.Light) or 
                    prim.IsA(UsdPhysics.RigidBodyAPI) or
                    prim.HasAttribute("semanticType")):
                continue
                
            if count >= MAX_DETAILED_PRIMS:
                break
                
            prim_path = str(prim.GetPath())
            detailed_prims[prim_path] = self._extract_prim_data(prim, detailed=True)
            count += 1
            
        return detailed_prims
    
    def _extract_prim_data(self, prim: Usd.Prim, detailed: bool = False) -> Dict[str, Any]:
        """Extract comprehensive data for a single prim"""
        prim_path = str(prim.GetPath())
        
        # Return from cache if available
        if prim_path in self._prim_cache:
            if detailed or self._prim_cache[prim_path].get("detailed", False):
                return self._prim_cache[prim_path]
                
        # Basic prim info
        prim_data = {
            "path": prim_path,
            "name": prim.GetName(),
            "type": str(prim.GetTypeName()),
            "active": prim.IsActive(),
            "defined": prim.IsDefined(),
            "abstract": prim.IsAbstract(),
            "has_children": prim.GetFilteredChildren(Usd.PrimIsDefined).size() > 0,
            "detailed": detailed,
        }
        
        # Extract metadata
        prim_data["metadata"] = self._get_important_metadata(prim)
        
        # Handle transformation
        if prim.IsA(UsdGeom.Xformable):
            xformable = UsdGeom.Xformable(prim)
            
            # Get local transform
            local_transform = self._extract_transform(xformable)
            if local_transform:
                prim_data["transform"] = local_transform
            
            # Get world transform for detailed view
            if detailed:
                matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                prim_data["world_transform"] = {
                    "position": self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation())),
                    "rotation": self._format_rotation(matrix),
                    "scale": self._format_vec3(matrix.ExtractScale()),
                }
        
        # Handle specific prim types
        if prim.IsA(UsdGeom.Mesh):
            mesh_data = self._extract_mesh_data(prim)
            prim_data.update(mesh_data)
            
            # Add material binding
            binding_api = UsdShade.MaterialBindingAPI(prim)
            if binding_api:
                material = binding_api.GetDirectBinding().GetMaterial()
                if material:
                    prim_data["material_path"] = str(material.GetPath())
                    
                    # For detailed view, include material data
                    if detailed and material:
                        mat_data = self._material_cache.get(str(material.GetPath()))
                        if mat_data:
                            prim_data["material"] = mat_data
                        else:
                            prim_data["material"] = self._extract_material_data(material.GetPrim())
                            
        elif prim.IsA(UsdShade.Material):
            material_data = self._extract_material_data(prim)
            prim_data.update(material_data)
            
        elif prim.IsA(UsdLux.Light):
            light_data = self._extract_light_data(prim)
            prim_data.update(light_data)
            
        elif prim.IsA(UsdGeom.Camera):
            camera_data = self._extract_camera_data(prim)
            prim_data.update(camera_data)
            
        # Handle physics
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            physics_data = self._extract_physics_data(prim)
            prim_data.update(physics_data)
            
        # Add attributes for detailed view
        if detailed:
            prim_data["attributes"] = {}
            for attr in prim.GetAttributes():
                if attr.IsValid() and attr.IsAuthored():
                    try:
                        value = attr.Get(self._scan_time)
                        # Convert complex types to strings
                        if isinstance(value, Gf.Vec3f) or isinstance(value, Gf.Vec3d):
                            value = self._format_vec3(value)
                        elif isinstance(value, Gf.Matrix4d):
                            value = "matrix(4x4)"
                        elif isinstance(value, (list, tuple)) and len(value) > 10:
                            value = f"array[{len(value)}]"
                            
                        prim_data["attributes"][attr.GetName()] = str(value)
                    except Exception:
                        prim_data["attributes"][attr.GetName()] = "error"
        
        # Store in cache
        self._prim_cache[prim_path] = prim_data
        return prim_data
        
    def _extract_mesh_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract mesh-specific data"""
        mesh = UsdGeom.Mesh(prim)
        mesh_data = {"geometry_type": "mesh"}
        
        # Get point count
        points_attr = mesh.GetPointsAttr()
        if points_attr and points_attr.IsValid():
            points = points_attr.Get(self._scan_time)
            if points is not None:
                mesh_data["point_count"] = len(points)
                
        # Get face counts
        face_counts_attr = mesh.GetFaceVertexCountsAttr()
        if face_counts_attr and face_counts_attr.IsValid():
            face_counts = face_counts_attr.Get(self._scan_time)
            if face_counts is not None:
                mesh_data["face_count"] = len(face_counts)
                triangle_count = sum(1 for count in face_counts if count == 3)
                quad_count = sum(1 for count in face_counts if count == 4)
                ngon_count = sum(1 for count in face_counts if count > 4)
                mesh_data["topology"] = {
                    "triangles": triangle_count,
                    "quads": quad_count,
                    "ngons": ngon_count,
                }
        
        # Get extent
        extent_attr = mesh.GetExtentAttr()
        if extent_attr and extent_attr.IsValid():
            extent = extent_attr.Get(self._scan_time)
            if extent is not None and len(extent) == 2:
                mesh_data["local_bounds"] = {
                    "min": self._format_vec3(extent[0]),
                    "max": self._format_vec3(extent[1]),
                    "size": self._format_vec3([extent[1][i] - extent[0][i] for i in range(3)])
                }
        
        # Check for texture coordinates
        st_attr = mesh.GetPrimvar("st")
        if st_attr and st_attr.IsValid():
            mesh_data["has_uvs"] = True
            
        # Check for normals
        normals_attr = mesh.GetNormalsAttr()
        if normals_attr and normals_attr.IsValid():
            mesh_data["has_normals"] = True
            
        # Check for color
        displayColor_attr = mesh.GetDisplayColorAttr()
        if displayColor_attr and displayColor_attr.IsValid():
            color = displayColor_attr.Get(self._scan_time)
            if color is not None and len(color) > 0:
                mesh_data["display_color"] = self._format_vec3(color[0])
                
        return mesh_data
        
    def _extract_material_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract material data from a material prim"""
        material_data = {"material_type": "unknown"}
        
        # Get the material
        material = UsdShade.Material(prim)
        
        # Try to determine material type from outputs
        outputs = material.GetOutputs()
        for output in outputs:
            material_data["material_type"] = output.GetFullName()
            break  # Just use the first output to identify material type
        
        # Extract surface color if available
        surface_shader = material.ComputeSurfaceSource()
        if surface_shader:
            shader_prim = surface_shader.GetPrim()
            
            # Try to find a color input
            color_inputs = ["diffuseColor", "baseColor", "color", "emissiveColor"]
            for color_input in color_inputs:
                if shader_prim.HasAttribute(f"inputs:{color_input}"):
                    attr = shader_prim.GetAttribute(f"inputs:{color_input}")
                    if attr and attr.IsValid():
                        color = attr.Get(self._scan_time)
                        if color is not None:
                            material_data["color"] = self._format_vec3(color)
                            break
            
            # Get inputs that are connectable
            inputs = surface_shader.GetInputs()
            material_data["shader_inputs"] = {}
            for input in inputs:
                if input.HasConnectedSource():
                    source = input.GetConnectedSource()
                    if source:
                        material_data["shader_inputs"][input.GetBaseName()] = str(source[0].GetPrim().GetPath())
                else:
                    try:
                        value = input.Get(self._scan_time)
                        if value is not None:
                            if isinstance(value, Gf.Vec3f) or isinstance(value, Gf.Vec3d):
                                value = self._format_vec3(value)
                            elif isinstance(value, str):
                                # Check if it's a texture path
                                if "." in value and "/" in value:
                                    material_data["shader_inputs"][input.GetBaseName()] = f"texture: {os.path.basename(value)}"
                                    continue
                                    
                            material_data["shader_inputs"][input.GetBaseName()] = str(value)
                    except:
                        pass
                        
        # Check for MDL material specifically (common in Isaac Sim)
        if prim.GetTypeName() == "Material" and prim.HasAttribute("info:mdl:sourceAsset"):
            attr = prim.GetAttribute("info:mdl:sourceAsset")
            if attr and attr.IsValid():
                mdl_path = attr.Get(self._scan_time)
                if mdl_path:
                    material_data["material_type"] = "mdl"
                    material_data["mdl_source"] = os.path.basename(mdl_path)
        
        return material_data
        
    def _extract_light_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract light-specific data"""
        light_data = {"light_type": str(prim.GetTypeName())}
        
        # Get common light attributes
        light = UsdLux.Light(prim)
        
        intensity_attr = light.GetIntensityAttr()
        if intensity_attr and intensity_attr.IsValid():
            light_data["intensity"] = intensity_attr.Get(self._scan_time)
            
        exposure_attr = light.GetExposureAttr()
        if exposure_attr and exposure_attr.IsValid():
            light_data["exposure"] = exposure_attr.Get(self._scan_time)
            
        color_attr = light.GetColorAttr()
        if color_attr and color_attr.IsValid():
            color = color_attr.Get(self._scan_time)
            light_data["color"] = self._format_vec3(color)
            
        return light_data
        
    def _extract_camera_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract camera-specific data"""
        camera_data = {"camera_type": "perspective"}
        
        camera = UsdGeom.Camera(prim)
        
        # Get projection
        projection_attr = camera.GetProjectionAttr()
        if projection_attr and projection_attr.IsValid():
            camera_data["camera_type"] = projection_attr.Get(self._scan_time)
        
        # Get focal length and aperture
        focal_attr = camera.GetFocalLengthAttr()
        if focal_attr and focal_attr.IsValid():
            camera_data["focal_length"] = focal_attr.Get(self._scan_time)
            
        h_aperture = camera.GetHorizontalApertureAttr()
        if h_aperture and h_aperture.IsValid():
            camera_data["horizontal_aperture"] = h_aperture.Get(self._scan_time)
            
        v_aperture = camera.GetVerticalApertureAttr()
        if v_aperture and v_aperture.IsValid():
            camera_data["vertical_aperture"] = v_aperture.Get(self._scan_time)
            
        # Get clipping range
        clipping_attr = camera.GetClippingRangeAttr()
        if clipping_attr and clipping_attr.IsValid():
            clip_range = clipping_attr.Get(self._scan_time)
            camera_data["near_clip"] = clip_range[0]
            camera_data["far_clip"] = clip_range[1]
            
        # Calculate FOV
        try:
            if "horizontal_aperture" in camera_data and "focal_length" in camera_data:
                h_fov = 2 * np.arctan(camera_data["horizontal_aperture"] / (2 * camera_data["focal_length"])) * 180 / np.pi
                camera_data["horizontal_fov"] = h_fov
        except:
            pass
            
        return camera_data
        
    def _extract_physics_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract physics data from a prim"""
        physics_data = {}
        
        # Check for rigid body API
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            rigid_body = UsdPhysics.RigidBodyAPI(prim)
            physics_data["physics_type"] = "rigid_body"
            
            # Get mass
            mass_attr = rigid_body.GetMassAttr()
            if mass_attr and mass_attr.IsValid():
                physics_data["mass"] = mass_attr.Get(self._scan_time)
                
            # Get velocity
            vel_attr = rigid_body.GetVelocityAttr()
            if vel_attr and vel_attr.IsValid():
                vel = vel_attr.Get(self._scan_time)
                physics_data["velocity"] = self._format_vec3(vel) if vel is not None else "zero"
                
            # Get angular velocity
            ang_vel_attr = rigid_body.GetAngularVelocityAttr()
            if ang_vel_attr and ang_vel_attr.IsValid():
                ang_vel = ang_vel_attr.Get(self._scan_time)
                physics_data["angular_velocity"] = self._format_vec3(ang_vel) if ang_vel is not None else "zero"
                
            # Check if kinematic
            kinematic_attr = rigid_body.GetKinematicEnabledAttr()
            if kinematic_attr and kinematic_attr.IsValid():
                physics_data["kinematic"] = kinematic_attr.Get(self._scan_time)
                
        # Check for collision API
        if prim.HasAPI(UsdPhysics.CollisionAPI):
            physics_data["has_collisions"] = True
            
            # Try to get collision shape if this is a collider
            if prim.IsA(UsdPhysics.Collider):
                collider = UsdPhysics.Collider(prim)
                approximation_attr = collider.GetApproximationAttr()
                if approximation_attr and approximation_attr.IsValid():
                    physics_data["collision_approximation"] = approximation_attr.Get(self._scan_time)
                    
                # Get specific collider type
                if prim.IsA(UsdPhysics.SphereCollider):
                    physics_data["collider_type"] = "sphere"
                    radius_attr = UsdPhysics.SphereCollider(prim).GetRadiusAttr()
                    if radius_attr and radius_attr.IsValid():
                        physics_data["collider_radius"] = radius_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdPhysics.BoxCollider):
                    physics_data["collider_type"] = "box"
                    size_attr = UsdPhysics.BoxCollider(prim).GetSizeAttr()
                    if size_attr and size_attr.IsValid():
                        size = size_attr.Get(self._scan_time)
                        physics_data["collider_size"] = self._format_vec3(size)
                        
                elif prim.IsA(UsdPhysics.CapsuleCollider):
                    physics_data["collider_type"] = "capsule"
                    radius_attr = UsdPhysics.CapsuleCollider(prim).GetRadiusAttr()
                    height_attr = UsdPhysics.CapsuleCollider(prim).GetHeightAttr()
                    if radius_attr and radius_attr.IsValid() and height_attr and height_attr.IsValid():
                        physics_data["collider_radius"] = radius_attr.Get(self._scan_time)
                        physics_data["collider_height"] = height_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdPhysics.ConvexHullCollider):
                    physics_data["collider_type"] = "convex_hull"
                    
                elif prim.IsA(UsdPhysics.MeshCollider):
                    physics_data["collider_type"] = "mesh"
                    
        return physics_data
    
    def _extract_transform(self, xformable: UsdGeom.Xformable) -> Optional[Dict[str, Any]]:
        """Extract transform data"""
        # Get transform ops
        transform_ops = xformable.GetOrderedXformOps()
        if not transform_ops:
            return None
            
        # Create transform result with defaults
        transform = {
            "position": "0, 0, 0",
            "rotation": "0, 0, 0",
            "scale": "1, 1, 1",
        }
        
        # Process each transform op
        for op in transform_ops:
            op_type = op.GetOpType()
            value = op.Get(self._scan_time)
            
            if not value:
                continue
                
            if op_type == UsdGeom.XformOp.TypeTranslate:
                transform["position"] = self._format_vec3(value)
                
            elif op_type in (UsdGeom.XformOp.TypeRotateXYZ, UsdGeom.XformOp.TypeRotateXZY,
                         UsdGeom.XformOp.TypeRotateYXZ, UsdGeom.XformOp.TypeRotateYZX,
                         UsdGeom.XformOp.TypeRotateZXY, UsdGeom.XformOp.TypeRotateZYX):
                transform["rotation"] = self._format_vec3(value)
                
            elif op_type == UsdGeom.XformOp.TypeScale:
                transform["scale"] = self._format_vec3(value)
                
            elif op_type == UsdGeom.XformOp.TypeTransform:
                # Matrix transform
                matrix = value
                transform["position"] = self._format_vec3(matrix.ExtractTranslation())
                transform["rotation"] = self._format_rotation(matrix)
                transform["scale"] = self._format_vec3(matrix.ExtractScale())
                
        return transform
    
    def _get_important_metadata(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract important metadata from a prim"""
        metadata = {}
        
        # Handle common important metadata
        for key in ["kind", "purpose", "instanceable", "active", "hidden"]:
            if prim.HasMetadata(key):
                metadata[key] = prim.GetMetadata(key)
                
        # Look for USD attributes that might be metadata
        for attr_name in ["semanticLabel", "semanticType", "label", "category", "class"]:
            if prim.HasAttribute(attr_name):
                attr = prim.GetAttribute(attr_name)
                if attr.IsValid():
                    metadata[attr_name] = attr.Get(self._scan_time)
                    
        # Look for Isaac Sim specific semantic data
        if prim.HasAttribute("userProperties:semanticLabel"):
            attr = prim.GetAttribute("userProperties:semanticLabel")
            if attr.IsValid():
                metadata["semantic_label"] = attr.Get(self._scan_time)
                
        return metadata
    
    def _format_vec3(self, vec) -> str:
        """Format a vector3 as a string"""
        if isinstance(vec, (list, tuple)):
            return f"{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}"
        else:
            return f"{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}"# filepath: /home/ubuntu/ivyverse/omni_ivyverse_python/scene_scanner.py
from pxr import Usd, UsdGeom, UsdShade, UsdLux, UsdPhysics, Gf, Sdf
import omni.usd
import carb
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
import json
import os
from collections import defaultdict

class SceneScanner:
    """
    Advanced USD scene scanner that extracts rich natural descriptions of scene components
    for consumption by LLM models in the Ivyverse extension.
    """
    
    def __init__(self):
        self._usd_context = omni.usd.get_context()
        self._stage = None
        self._prim_cache = {}
        self._material_cache = {}
        self._scan_time = None
    
    def scan_scene(self, detailed: bool = True) -> Dict[str, Any]:
        """
        Performs a comprehensive scan of the current USD stage and returns information
        in a format optimized for LLM consumption.
        
        Args:
            detailed: Whether to include detailed attribute information for each prim
            
        Returns:
            Dictionary containing hierarchical scene information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            carb.log_warn("No stage is loaded")
            return {"error": "No stage is loaded"}
        
        self._prim_cache = {}
        self._material_cache = {}
        self._scan_time = self._stage.GetTimeCode()
        
        scene_info = {
            "scene_metadata": self._extract_scene_metadata(),
            "scene_summary": self._generate_scene_summary(),
            "scene_hierarchy": self._extract_hierarchy(),
            "physics_setup": self._extract_physics(),
            "material_library": self._extract_materials(),
            "lighting_setup": self._extract_lighting(),
            "camera_setup": self._extract_cameras(),
            "special_prims": self._extract_special_prims(),
        }
        
        if detailed:
            scene_info["detailed_prims"] = self._extract_detailed_prim_info()
            
        return scene_info
    
    def get_prim_info(self, prim_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific prim
        
        Args:
            prim_path: USD path to the desired prim
            
        Returns:
            Dictionary containing detailed prim information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            return {"error": "No stage is loaded"}
            
        prim = self._stage.GetPrimAtPath(prim_path)
        if not prim:
            return {"error": f"No prim found at path: {prim_path}"}
            
        return self._extract_prim_data(prim, detailed=True)
    
    def get_natural_scene_description(self) -> str:
        """
        Generate a natural language description of the current scene
        
        Returns:
            String containing a natural language description of the scene
        """
        scene_data = self.scan_scene(detailed=False)
        
        # Extract key metrics
        meta = scene_data["scene_metadata"]
        summary = scene_data["scene_summary"]
        
        # Generate natural description
        description = f"""
This USD scene '{os.path.basename(meta.get('file_name', 'Untitled'))}' contains {summary['total_prims']} prims organized in a hierarchy.

The scene contains:
- {summary.get('mesh_count', 0)} meshes/geometric objects
- {summary.get('material_count', 0)} materials
- {summary.get('light_count', 0)} light sources
- {summary.get('camera_count', 0)} cameras
- {summary.get('physics_prims', 0)} physics-enabled objects

The world bounds span from {meta.get('bounds_min', 'unknown')} to {meta.get('bounds_max', 'unknown')}.

Main objects in the scene:
"""
        
        # Add important prims by type
        if scene_data.get("special_prims", {}).get("important_objects"):
            for obj in scene_data["special_prims"]["important_objects"][:10]:  # Limit to 10
                description += f"- {obj['path']}: {obj['type']}"
                if "semantic_label" in obj:
                    description += f" (labeled as '{obj['semantic_label']}')"
                description += "\n"
        
        # Add physics information
        if scene_data.get("physics_setup", {}).get("enabled", False):
            description += "\nThe scene has physics enabled with "
            description += f"gravity set to {scene_data['physics_setup'].get('gravity', 'default')}. "
            description += f"There are {scene_data['physics_setup'].get('rigid_body_count', 0)} rigid bodies "
            description += f"and {scene_data['physics_setup'].get('collider_count', 0)} colliders.\n"
        
        return description
    
    def search_prims(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for prims matching a query string in name or type
        
        Args:
            query: Search string to match against prim names or types
            
        Returns:
            List of matching prims with their information
        """
        self._stage = self._usd_context.get_stage()
        if not self._stage:
            return [{"error": "No stage is loaded"}]
            
        query = query.lower()
        results = []
        
        for prim in self._stage.Traverse():
            path = str(prim.GetPath())
            prim_type = prim.GetTypeName()
            
            if query in path.lower() or query in str(prim_type).lower():
                results.append(self._extract_prim_data(prim, detailed=False))
                
        return results
    
    def _extract_scene_metadata(self) -> Dict[str, Any]:
        """Extract high-level scene metadata"""
        metadata = {
            "file_name": self._stage.GetRootLayer().GetDisplayName(),
            "default_prim": str(self._stage.GetDefaultPrim().GetPath()) if self._stage.GetDefaultPrim() else "None",
            "up_axis": UsdGeom.GetStageUpAxis(self._stage),
            "meters_per_unit": UsdGeom.GetStageMetersPerUnit(self._stage),
            "time_code_range": (self._stage.GetStartTimeCode(), self._stage.GetEndTimeCode()),
            "current_time_code": self._stage.GetTimeCode(),
        }
        
        # Get world bounds
        bboxcache = UsdGeom.BBoxCache(self._scan_time, ['default', 'render'])
        bounds = bboxcache.ComputeWorldBound(self._stage.GetPseudoRoot())
        if isinstance(bounds, UsdGeom.BBox3d):
            min_extent = bounds.GetBox().GetMin()
            max_extent = bounds.GetBox().GetMax()
            metadata["bounds_min"] = f"({min_extent[0]:.2f}, {min_extent[1]:.2f}, {min_extent[2]:.2f})"
            metadata["bounds_max"] = f"({max_extent[0]:.2f}, {max_extent[1]:.2f}, {max_extent[2]:.2f})"
            metadata["bounds_size"] = f"({max_extent[0] - min_extent[0]:.2f} × {max_extent[1] - min_extent[1]:.2f} × {max_extent[2] - min_extent[2]:.2f})"
        
        return metadata
    
    def _generate_scene_summary(self) -> Dict[str, Any]:
        """Generate numerical summary of scene contents"""
        summary = {}
        
        # Count by primitive type
        all_prims = list(self._stage.Traverse())
        summary["total_prims"] = len(all_prims)
        
        type_counts = defaultdict(int)
        for prim in all_prims:
            type_counts[prim.GetTypeName()] += 1
        summary["prim_types"] = {str(k): v for k, v in type_counts.items() if k}
        
        # Count specific important types
        summary["mesh_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Mesh))
        summary["material_count"] = sum(1 for prim in all_prims if prim.IsA(UsdShade.Material))
        summary["light_count"] = sum(1 for prim in all_prims if prim.IsA(UsdLux.Light))
        summary["camera_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Camera))
        summary["xform_count"] = sum(1 for prim in all_prims if prim.IsA(UsdGeom.Xform) and not prim.IsA(UsdGeom.Camera))
        summary["physics_prims"] = sum(1 for prim in all_prims if prim.HasAPI(UsdPhysics.RigidBodyAPI) or prim.HasAPI(UsdPhysics.CollisionAPI))
        
        # Layer analysis
        summary["layer_stack_count"] = len(self._stage.GetLayerStack())
        
        return summary
    
    def _extract_hierarchy(self) -> Dict[str, Any]:
        """Extract scene hierarchy information"""
        def build_hierarchy(prim):
            if not prim:
                return None
                
            children = {}
            for child in prim.GetFilteredChildren(Usd.PrimIsDefined and not Usd.PrimIsAbstract):
                children[child.GetName()] = build_hierarchy(child)
                
            return {
                "type": str(prim.GetTypeName()),
                "path": str(prim.GetPath()),
                "metadata": self._get_important_metadata(prim),
                "children": children
            }
            
        # Start from root or default prim
        default_prim = self._stage.GetDefaultPrim()
        root = default_prim if default_prim else self._stage.GetPseudoRoot()
        
        return build_hierarchy(root)
    
    def _extract_physics(self) -> Dict[str, Any]:
        """Extract physics setup information"""
        physics_info = {
            "enabled": False,
            "gravity": "9.8 m/s² (default)",
            "rigid_body_count": 0,
            "collider_count": 0,
            "joints": []
        }
        
        # Check for physics scene
        physics_scene = None
        for prim in self._stage.Traverse():
            if prim.IsA(UsdPhysics.Scene):
                physics_scene = prim
                physics_info["enabled"] = True
                break
                
        # Get gravity
        if physics_scene:
            gravity_attr = UsdPhysics.Scene(physics_scene).GetGravityDirectionAttr()
            magnitude_attr = UsdPhysics.Scene(physics_scene).GetGravityMagnitudeAttr()
            if gravity_attr and gravity_attr.IsValid() and magnitude_attr and magnitude_attr.IsValid():
                direction = gravity_attr.Get(self._scan_time)
                magnitude = magnitude_attr.Get(self._scan_time)
                if direction is not None and magnitude is not None:
                    physics_info["gravity"] = f"{magnitude} m/s² in direction ({direction[0]}, {direction[1]}, {direction[2]})"
        
        # Count physics objects
        rigid_bodies = []
        colliders = []
        joints = []
        
        for prim in self._stage.Traverse():
            if prim.HasAPI(UsdPhysics.RigidBodyAPI):
                rigid_bodies.append(str(prim.GetPath()))
                
            if prim.HasAPI(UsdPhysics.CollisionAPI) or prim.IsA(UsdPhysics.CollisionAPI):
                colliders.append(str(prim.GetPath()))
                
            if prim.IsA(UsdPhysics.Joint):
                joints.append({
                    "path": str(prim.GetPath()),
                    "type": str(prim.GetTypeName()),
                    "body0": UsdPhysics.Joint(prim).GetBody0Rel().GetTargets()[0] if UsdPhysics.Joint(prim).GetBody0Rel().GetTargets() else "",
                    "body1": UsdPhysics.Joint(prim).GetBody1Rel().GetTargets()[0] if UsdPhysics.Joint(prim).GetBody1Rel().GetTargets() else ""
                })
        
        physics_info["rigid_body_count"] = len(rigid_bodies)
        physics_info["collider_count"] = len(colliders)
        physics_info["rigid_bodies"] = rigid_bodies[:20] if len(rigid_bodies) <= 20 else rigid_bodies[:20] + [f"... {len(rigid_bodies) - 20} more"]
        physics_info["colliders"] = colliders[:20] if len(colliders) <= 20 else colliders[:20] + [f"... {len(colliders) - 20} more"]
        physics_info["joints"] = joints[:20] if len(joints) <= 20 else joints[:20] + [{"note": f"{len(joints) - 20} more joints"}]
        
        return physics_info
    
    def _extract_materials(self) -> Dict[str, Any]:
        """Extract material information"""
        materials = {}
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdShade.Material):
                mat_path = str(prim.GetPath())
                mat_data = self._extract_material_data(prim)
                materials[mat_path] = mat_data
                self._material_cache[mat_path] = mat_data
                
        # Also extract material bindings for all meshes
        binding_info = []
        for prim in self._stage.Traverse():
            if prim.IsA(UsdGeom.Mesh) or prim.IsA(UsdGeom.Scope):
                bindingAPI = UsdShade.MaterialBindingAPI(prim)
                if bindingAPI:
                    direct_binding = bindingAPI.GetDirectBinding().GetMaterial()
                    if direct_binding:
                        binding_info.append({
                            "prim_path": str(prim.GetPath()),
                            "material_path": str(direct_binding.GetPath())
                        })
        
        return {
            "materials": materials,
            "bindings": binding_info[:30]  # Limit to 30 bindings
        }
    
    def _extract_lighting(self) -> Dict[str, Any]:
        """Extract lighting setup information"""
        lights = []
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdLux.Light):
                light_data = {
                    "path": str(prim.GetPath()),
                    "type": str(prim.GetTypeName()),
                    "enabled": UsdLux.Light(prim).GetEnableColorTemperatureAttr().Get(self._scan_time) if UsdLux.Light(prim).GetEnableColorTemperatureAttr() else True,
                }
                
                # Extract common light attributes
                light_schema = UsdLux.Light(prim)
                
                intensity_attr = light_schema.GetIntensityAttr()
                if intensity_attr and intensity_attr.IsValid():
                    light_data["intensity"] = intensity_attr.Get(self._scan_time)
                    
                exposure_attr = light_schema.GetExposureAttr()
                if exposure_attr and exposure_attr.IsValid():
                    light_data["exposure"] = exposure_attr.Get(self._scan_time)
                    
                color_attr = light_schema.GetColorAttr()
                if color_attr and color_attr.IsValid():
                    color = color_attr.Get(self._scan_time)
                    light_data["color"] = f"({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})"
                    
                # Extract type-specific attributes
                if prim.IsA(UsdLux.DistantLight):
                    angle_attr = UsdLux.DistantLight(prim).GetAngleAttr()
                    if angle_attr and angle_attr.IsValid():
                        light_data["angle"] = angle_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.DiskLight) or prim.IsA(UsdLux.SphereLight):
                    radius_attr = (UsdLux.DiskLight(prim) if prim.IsA(UsdLux.DiskLight) else UsdLux.SphereLight(prim)).GetRadiusAttr()
                    if radius_attr and radius_attr.IsValid():
                        light_data["radius"] = radius_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.RectLight):
                    width_attr = UsdLux.RectLight(prim).GetWidthAttr()
                    height_attr = UsdLux.RectLight(prim).GetHeightAttr()
                    if width_attr and width_attr.IsValid() and height_attr and height_attr.IsValid():
                        light_data["width"] = width_attr.Get(self._scan_time)
                        light_data["height"] = height_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdLux.CylinderLight):
                    length_attr = UsdLux.CylinderLight(prim).GetLengthAttr()
                    radius_attr = UsdLux.CylinderLight(prim).GetRadiusAttr()
                    if length_attr and length_attr.IsValid() and radius_attr and radius_attr.IsValid():
                        light_data["length"] = length_attr.Get(self._scan_time)
                        light_data["radius"] = radius_attr.Get(self._scan_time)
                
                # Add transform
                xformable = UsdGeom.Xformable(prim)
                if xformable:
                    matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                    light_data["position"] = self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation()))
                
                lights.append(light_data)
        
        return {
            "lights": lights,
            "dome_light": self._extract_dome_light()
        }
    
    def _extract_dome_light(self) -> Optional[Dict[str, Any]]:
        """Extract dome light information if present"""
        for prim in self._stage.Traverse():
            if prim.IsA(UsdLux.DomeLight):
                dome_light = UsdLux.DomeLight(prim)
                dome_data = {
                    "path": str(prim.GetPath()),
                    "enabled": dome_light.GetEnableColorTemperatureAttr().Get(self._scan_time) if dome_light.GetEnableColorTemperatureAttr() else True,
                }
                
                texture_attr = dome_light.GetTextureFileAttr()
                if texture_attr and texture_attr.IsValid():
                    dome_data["texture"] = texture_attr.Get(self._scan_time)
                    
                exposure_attr = dome_light.GetExposureAttr()
                if exposure_attr and exposure_attr.IsValid():
                    dome_data["exposure"] = exposure_attr.Get(self._scan_time)
                    
                intensity_attr = dome_light.GetIntensityAttr()
                if intensity_attr and intensity_attr.IsValid():
                    dome_data["intensity"] = intensity_attr.Get(self._scan_time)
                    
                return dome_data
                
        return None
    
    def _extract_cameras(self) -> List[Dict[str, Any]]:
        """Extract camera information"""
        cameras = []
        
        for prim in self._stage.Traverse():
            if prim.IsA(UsdGeom.Camera):
                camera = UsdGeom.Camera(prim)
                
                # Basic camera info
                camera_data = {
                    "path": str(prim.GetPath()),
                    "active": "activeCamera" in [token.GetString() for token in prim.GetPropertyNames()]
                }
                
                # Get projection
                projection_attr = camera.GetProjectionAttr()
                if projection_attr and projection_attr.IsValid():
                    camera_data["projection"] = projection_attr.Get(self._scan_time)
                
                # Get focal length
                focal_attr = camera.GetFocalLengthAttr()
                if focal_attr and focal_attr.IsValid():
                    camera_data["focal_length"] = focal_attr.Get(self._scan_time)
                
                # Get horizontal aperture
                h_aperture_attr = camera.GetHorizontalApertureAttr()
                if h_aperture_attr and h_aperture_attr.IsValid():
                    camera_data["horizontal_aperture"] = h_aperture_attr.Get(self._scan_time)
                
                # Get vertical aperture
                v_aperture_attr = camera.GetVerticalApertureAttr()
                if v_aperture_attr and v_aperture_attr.IsValid():
                    camera_data["vertical_aperture"] = v_aperture_attr.Get(self._scan_time)
                
                # Get clipping range
                clipping_attr = camera.GetClippingRangeAttr()
                if clipping_attr and clipping_attr.IsValid():
                    clip_range = clipping_attr.Get(self._scan_time)
                    camera_data["clipping_range"] = f"{clip_range[0]} to {clip_range[1]}"
                
                # Add transform
                xformable = UsdGeom.Xformable(prim)
                if xformable:
                    matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                    camera_data["position"] = self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation()))
                    
                    # Decompose rotation
                    rotation = matrix.ExtractRotation()
                    camera_data["forward"] = self._format_vec3(rotation.TransformDir(Gf.Vec3d(0, 0, -1)))
                    camera_data["up"] = self._format_vec3(rotation.TransformDir(Gf.Vec3d(0, 1, 0)))
                
                cameras.append(camera_data)
        
        return cameras
    
    def _extract_special_prims(self) -> Dict[str, Any]:
        """Extract information about special prims like references, instances, etc."""
        special_prims = {
            "references": [],
            "instances": [],
            "variants": [],
            "important_objects": [],
        }
        
        # Find large meshes or objects with semantic information
        for prim in self._stage.Traverse():
            # Check for references
            if prim.HasAuthoredReferences():
                refs = prim.GetReferences()
                ref_list = []
                for i in range(refs.GetNumReferences()):
                    ref = refs.GetItemForEdit(i)
                    ref_list.append(str(ref.GetAssetPath()))
                    
                if ref_list:
                    special_prims["references"].append({
                        "path": str(prim.GetPath()),
                        "references": ref_list
                    })
            
            # Check for instances
            if prim.IsInstanceable() and prim.IsInstance():
                special_prims["instances"].append({
                    "path": str(prim.GetPath()),
                    "master": str(prim.GetMaster().GetPath()) if prim.GetMaster() else "unknown"
                })
            
            # Check for variants
            if prim.HasVariantSets():
                variant_sets = prim.GetVariantSets()
                all_sets = variant_sets.GetNames()
                
                var_data = {
                    "path": str(prim.GetPath()),
                    "variant_sets": {}
                }
                
                for set_name in all_sets:
                    var_set = variant_sets.GetVariantSet(set_name)
                    var_data["variant_sets"][set_name] = {
                        "variants": var_set.GetVariantNames(),
                        "selected": var_set.GetVariantSelection()
                    }
                    
                special_prims["variants"].append(var_data)
            
            # Identify important objects
            importance_score = 0
            
            # Score geometric complexity
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)
                point_count_attr = mesh.GetPointsAttr()
                if point_count_attr and point_count_attr.IsValid():
                    points = point_count_attr.Get(self._scan_time)
                    if points is not None:
                        point_count = len(points)
                        importance_score += min(point_count / 1000, 10)  # Cap at 10 points
            
            # Score by transformations
            if prim.IsA(UsdGeom.Xformable):
                xformable = UsdGeom.Xformable(prim)
                if xformable.TransformMightBeTimeVarying():
                    importance_score += 5  # Animated objects are important
            
            # Score by semantic type
            if prim.HasAttribute("semanticType") or prim.HasAttribute("kind"):
                importance_score += 3
                
                semantic_type = None
                if prim.HasAttribute("semanticType"):
                    semantic_attr = prim.GetAttribute("semanticType")
                    if semantic_attr.IsValid():
                        semantic_type = semantic_attr.Get(self._scan_time)
                elif prim.HasAttribute("kind"):
                    kind_attr = prim.GetAttribute("kind")
                    if kind_attr.IsValid():
                        semantic_type = kind_attr.Get(self._scan_time)
                
                if importance_score >= 2:
                    obj_info = {
                        "path": str(prim.GetPath()),
                        "type": str(prim.GetTypeName()),
                        "importance_score": importance_score
                    }
                    
                    if semantic_type:
                        obj_info["semantic_label"] = semantic_type
                        
                    special_prims["important_objects"].append(obj_info)
        
        # Sort important objects by score
        special_prims["important_objects"] = sorted(
            special_prims["important_objects"], 
            key=lambda x: x["importance_score"], 
            reverse=True
        )
        
        return special_prims
    
    def _extract_detailed_prim_info(self) -> Dict[str, Dict[str, Any]]:
        """Extract detailed information for important prims"""
        detailed_prims = {}
        
        # Process a reasonable number of prims to avoid overwhelming the LLM
        count = 0
        MAX_DETAILED_PRIMS = 100
        
        for prim in self._stage.Traverse():
            # Skip prims that aren't interesting
            if not (prim.IsA(UsdGeom.Mesh) or 
                    prim.IsA(UsdGeom.Camera) or 
                    prim.IsA(UsdLux.Light) or 
                    prim.IsA(UsdPhysics.RigidBodyAPI) or
                    prim.HasAttribute("semanticType")):
                continue
                
            if count >= MAX_DETAILED_PRIMS:
                break
                
            prim_path = str(prim.GetPath())
            detailed_prims[prim_path] = self._extract_prim_data(prim, detailed=True)
            count += 1
            
        return detailed_prims
    
    def _extract_prim_data(self, prim: Usd.Prim, detailed: bool = False) -> Dict[str, Any]:
        """Extract comprehensive data for a single prim"""
        prim_path = str(prim.GetPath())
        
        # Return from cache if available
        if prim_path in self._prim_cache:
            if detailed or self._prim_cache[prim_path].get("detailed", False):
                return self._prim_cache[prim_path]
                
        # Basic prim info
        prim_data = {
            "path": prim_path,
            "name": prim.GetName(),
            "type": str(prim.GetTypeName()),
            "active": prim.IsActive(),
            "defined": prim.IsDefined(),
            "abstract": prim.IsAbstract(),
            "has_children": prim.GetFilteredChildren(Usd.PrimIsDefined).size() > 0,
            "detailed": detailed,
        }
        
        # Extract metadata
        prim_data["metadata"] = self._get_important_metadata(prim)
        
        # Handle transformation
        if prim.IsA(UsdGeom.Xformable):
            xformable = UsdGeom.Xformable(prim)
            
            # Get local transform
            local_transform = self._extract_transform(xformable)
            if local_transform:
                prim_data["transform"] = local_transform
            
            # Get world transform for detailed view
            if detailed:
                matrix = xformable.ComputeLocalToWorldTransform(self._scan_time)
                prim_data["world_transform"] = {
                    "position": self._format_vec3(Gf.Vec3d(matrix.ExtractTranslation())),
                    "rotation": self._format_rotation(matrix),
                    "scale": self._format_vec3(matrix.ExtractScale()),
                }
        
        # Handle specific prim types
        if prim.IsA(UsdGeom.Mesh):
            mesh_data = self._extract_mesh_data(prim)
            prim_data.update(mesh_data)
            
            # Add material binding
            binding_api = UsdShade.MaterialBindingAPI(prim)
            if binding_api:
                material = binding_api.GetDirectBinding().GetMaterial()
                if material:
                    prim_data["material_path"] = str(material.GetPath())
                    
                    # For detailed view, include material data
                    if detailed and material:
                        mat_data = self._material_cache.get(str(material.GetPath()))
                        if mat_data:
                            prim_data["material"] = mat_data
                        else:
                            prim_data["material"] = self._extract_material_data(material.GetPrim())
                            
        elif prim.IsA(UsdShade.Material):
            material_data = self._extract_material_data(prim)
            prim_data.update(material_data)
            
        elif prim.IsA(UsdLux.Light):
            light_data = self._extract_light_data(prim)
            prim_data.update(light_data)
            
        elif prim.IsA(UsdGeom.Camera):
            camera_data = self._extract_camera_data(prim)
            prim_data.update(camera_data)
            
        # Handle physics
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            physics_data = self._extract_physics_data(prim)
            prim_data.update(physics_data)
            
        # Add attributes for detailed view
        if detailed:
            prim_data["attributes"] = {}
            for attr in prim.GetAttributes():
                if attr.IsValid() and attr.IsAuthored():
                    try:
                        value = attr.Get(self._scan_time)
                        # Convert complex types to strings
                        if isinstance(value, Gf.Vec3f) or isinstance(value, Gf.Vec3d):
                            value = self._format_vec3(value)
                        elif isinstance(value, Gf.Matrix4d):
                            value = "matrix(4x4)"
                        elif isinstance(value, (list, tuple)) and len(value) > 10:
                            value = f"array[{len(value)}]"
                            
                        prim_data["attributes"][attr.GetName()] = str(value)
                    except Exception:
                        prim_data["attributes"][attr.GetName()] = "error"
        
        # Store in cache
        self._prim_cache[prim_path] = prim_data
        return prim_data
        
    def _extract_mesh_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract mesh-specific data"""
        mesh = UsdGeom.Mesh(prim)
        mesh_data = {"geometry_type": "mesh"}
        
        # Get point count
        points_attr = mesh.GetPointsAttr()
        if points_attr and points_attr.IsValid():
            points = points_attr.Get(self._scan_time)
            if points is not None:
                mesh_data["point_count"] = len(points)
                
        # Get face counts
        face_counts_attr = mesh.GetFaceVertexCountsAttr()
        if face_counts_attr and face_counts_attr.IsValid():
            face_counts = face_counts_attr.Get(self._scan_time)
            if face_counts is not None:
                mesh_data["face_count"] = len(face_counts)
                triangle_count = sum(1 for count in face_counts if count == 3)
                quad_count = sum(1 for count in face_counts if count == 4)
                ngon_count = sum(1 for count in face_counts if count > 4)
                mesh_data["topology"] = {
                    "triangles": triangle_count,
                    "quads": quad_count,
                    "ngons": ngon_count,
                }
        
        # Get extent
        extent_attr = mesh.GetExtentAttr()
        if extent_attr and extent_attr.IsValid():
            extent = extent_attr.Get(self._scan_time)
            if extent is not None and len(extent) == 2:
                mesh_data["local_bounds"] = {
                    "min": self._format_vec3(extent[0]),
                    "max": self._format_vec3(extent[1]),
                    "size": self._format_vec3([extent[1][i] - extent[0][i] for i in range(3)])
                }
        
        # Check for texture coordinates
        st_attr = mesh.GetPrimvar("st")
        if st_attr and st_attr.IsValid():
            mesh_data["has_uvs"] = True
            
        # Check for normals
        normals_attr = mesh.GetNormalsAttr()
        if normals_attr and normals_attr.IsValid():
            mesh_data["has_normals"] = True
            
        # Check for color
        displayColor_attr = mesh.GetDisplayColorAttr()
        if displayColor_attr and displayColor_attr.IsValid():
            color = displayColor_attr.Get(self._scan_time)
            if color is not None and len(color) > 0:
                mesh_data["display_color"] = self._format_vec3(color[0])
                
        return mesh_data
        
    def _extract_material_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract material data from a material prim"""
        material_data = {"material_type": "unknown"}
        
        # Get the material
        material = UsdShade.Material(prim)
        
        # Try to determine material type from outputs
        outputs = material.GetOutputs()
        for output in outputs:
            material_data["material_type"] = output.GetFullName()
            break  # Just use the first output to identify material type
        
        # Extract surface color if available
        surface_shader = material.ComputeSurfaceSource()
        if surface_shader:
            shader_prim = surface_shader.GetPrim()
            
            # Try to find a color input
            color_inputs = ["diffuseColor", "baseColor", "color", "emissiveColor"]
            for color_input in color_inputs:
                if shader_prim.HasAttribute(f"inputs:{color_input}"):
                    attr = shader_prim.GetAttribute(f"inputs:{color_input}")
                    if attr and attr.IsValid():
                        color = attr.Get(self._scan_time)
                        if color is not None:
                            material_data["color"] = self._format_vec3(color)
                            break
            
            # Get inputs that are connectable
            inputs = surface_shader.GetInputs()
            material_data["shader_inputs"] = {}
            for input in inputs:
                if input.HasConnectedSource():
                    source = input.GetConnectedSource()
                    if source:
                        material_data["shader_inputs"][input.GetBaseName()] = str(source[0].GetPrim().GetPath())
                else:
                    try:
                        value = input.Get(self._scan_time)
                        if value is not None:
                            if isinstance(value, Gf.Vec3f) or isinstance(value, Gf.Vec3d):
                                value = self._format_vec3(value)
                            elif isinstance(value, str):
                                # Check if it's a texture path
                                if "." in value and "/" in value:
                                    material_data["shader_inputs"][input.GetBaseName()] = f"texture: {os.path.basename(value)}"
                                    continue
                                    
                            material_data["shader_inputs"][input.GetBaseName()] = str(value)
                    except:
                        pass
                        
        # Check for MDL material specifically (common in Isaac Sim)
        if prim.GetTypeName() == "Material" and prim.HasAttribute("info:mdl:sourceAsset"):
            attr = prim.GetAttribute("info:mdl:sourceAsset")
            if attr and attr.IsValid():
                mdl_path = attr.Get(self._scan_time)
                if mdl_path:
                    material_data["material_type"] = "mdl"
                    material_data["mdl_source"] = os.path.basename(mdl_path)
        
        return material_data
        
    def _extract_light_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract light-specific data"""
        light_data = {"light_type": str(prim.GetTypeName())}
        
        # Get common light attributes
        light = UsdLux.Light(prim)
        
        intensity_attr = light.GetIntensityAttr()
        if intensity_attr and intensity_attr.IsValid():
            light_data["intensity"] = intensity_attr.Get(self._scan_time)
            
        exposure_attr = light.GetExposureAttr()
        if exposure_attr and exposure_attr.IsValid():
            light_data["exposure"] = exposure_attr.Get(self._scan_time)
            
        color_attr = light.GetColorAttr()
        if color_attr and color_attr.IsValid():
            color = color_attr.Get(self._scan_time)
            light_data["color"] = self._format_vec3(color)
            
        return light_data
        
    def _extract_camera_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract camera-specific data"""
        camera_data = {"camera_type": "perspective"}
        
        camera = UsdGeom.Camera(prim)
        
        # Get projection
        projection_attr = camera.GetProjectionAttr()
        if projection_attr and projection_attr.IsValid():
            camera_data["camera_type"] = projection_attr.Get(self._scan_time)
        
        # Get focal length and aperture
        focal_attr = camera.GetFocalLengthAttr()
        if focal_attr and focal_attr.IsValid():
            camera_data["focal_length"] = focal_attr.Get(self._scan_time)
            
        h_aperture = camera.GetHorizontalApertureAttr()
        if h_aperture and h_aperture.IsValid():
            camera_data["horizontal_aperture"] = h_aperture.Get(self._scan_time)
            
        v_aperture = camera.GetVerticalApertureAttr()
        if v_aperture and v_aperture.IsValid():
            camera_data["vertical_aperture"] = v_aperture.Get(self._scan_time)
            
        # Get clipping range
        clipping_attr = camera.GetClippingRangeAttr()
        if clipping_attr and clipping_attr.IsValid():
            clip_range = clipping_attr.Get(self._scan_time)
            camera_data["near_clip"] = clip_range[0]
            camera_data["far_clip"] = clip_range[1]
            
        # Calculate FOV
        try:
            if "horizontal_aperture" in camera_data and "focal_length" in camera_data:
                h_fov = 2 * np.arctan(camera_data["horizontal_aperture"] / (2 * camera_data["focal_length"])) * 180 / np.pi
                camera_data["horizontal_fov"] = h_fov
        except:
            pass
            
        return camera_data
        
    def _extract_physics_data(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract physics data from a prim"""
        physics_data = {}
        
        # Check for rigid body API
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            rigid_body = UsdPhysics.RigidBodyAPI(prim)
            physics_data["physics_type"] = "rigid_body"
            
            # Get mass
            mass_attr = rigid_body.GetMassAttr()
            if mass_attr and mass_attr.IsValid():
                physics_data["mass"] = mass_attr.Get(self._scan_time)
                
            # Get velocity
            vel_attr = rigid_body.GetVelocityAttr()
            if vel_attr and vel_attr.IsValid():
                vel = vel_attr.Get(self._scan_time)
                physics_data["velocity"] = self._format_vec3(vel) if vel is not None else "zero"
                
            # Get angular velocity
            ang_vel_attr = rigid_body.GetAngularVelocityAttr()
            if ang_vel_attr and ang_vel_attr.IsValid():
                ang_vel = ang_vel_attr.Get(self._scan_time)
                physics_data["angular_velocity"] = self._format_vec3(ang_vel) if ang_vel is not None else "zero"
                
            # Check if kinematic
            kinematic_attr = rigid_body.GetKinematicEnabledAttr()
            if kinematic_attr and kinematic_attr.IsValid():
                physics_data["kinematic"] = kinematic_attr.Get(self._scan_time)
                
        # Check for collision API
        if prim.HasAPI(UsdPhysics.CollisionAPI):
            physics_data["has_collisions"] = True
            
            # Try to get collision shape if this is a collider
            if prim.IsA(UsdPhysics.Collider):
                collider = UsdPhysics.Collider(prim)
                approximation_attr = collider.GetApproximationAttr()
                if approximation_attr and approximation_attr.IsValid():
                    physics_data["collision_approximation"] = approximation_attr.Get(self._scan_time)
                    
                # Get specific collider type
                if prim.IsA(UsdPhysics.SphereCollider):
                    physics_data["collider_type"] = "sphere"
                    radius_attr = UsdPhysics.SphereCollider(prim).GetRadiusAttr()
                    if radius_attr and radius_attr.IsValid():
                        physics_data["collider_radius"] = radius_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdPhysics.BoxCollider):
                    physics_data["collider_type"] = "box"
                    size_attr = UsdPhysics.BoxCollider(prim).GetSizeAttr()
                    if size_attr and size_attr.IsValid():
                        size = size_attr.Get(self._scan_time)
                        physics_data["collider_size"] = self._format_vec3(size)
                        
                elif prim.IsA(UsdPhysics.CapsuleCollider):
                    physics_data["collider_type"] = "capsule"
                    radius_attr = UsdPhysics.CapsuleCollider(prim).GetRadiusAttr()
                    height_attr = UsdPhysics.CapsuleCollider(prim).GetHeightAttr()
                    if radius_attr and radius_attr.IsValid() and height_attr and height_attr.IsValid():
                        physics_data["collider_radius"] = radius_attr.Get(self._scan_time)
                        physics_data["collider_height"] = height_attr.Get(self._scan_time)
                        
                elif prim.IsA(UsdPhysics.ConvexHullCollider):
                    physics_data["collider_type"] = "convex_hull"
                    
                elif prim.IsA(UsdPhysics.MeshCollider):
                    physics_data["collider_type"] = "mesh"
                    
        return physics_data
    
    def _extract_transform(self, xformable: UsdGeom.Xformable) -> Optional[Dict[str, Any]]:
        """Extract transform data"""
        # Get transform ops
        transform_ops = xformable.GetOrderedXformOps()
        if not transform_ops:
            return None
            
        # Create transform result with defaults
        transform = {
            "position": "0, 0, 0",
            "rotation": "0, 0, 0",
            "scale": "1, 1, 1",
        }
        
        # Process each transform op
        for op in transform_ops:
            op_type = op.GetOpType()
            value = op.Get(self._scan_time)
            
            if not value:
                continue
                
            if op_type == UsdGeom.XformOp.TypeTranslate:
                transform["position"] = self._format_vec3(value)
                
            elif op_type in (UsdGeom.XformOp.TypeRotateXYZ, UsdGeom.XformOp.TypeRotateXZY,
                         UsdGeom.XformOp.TypeRotateYXZ, UsdGeom.XformOp.TypeRotateYZX,
                         UsdGeom.XformOp.TypeRotateZXY, UsdGeom.XformOp.TypeRotateZYX):
                transform["rotation"] = self._format_vec3(value)
                
            elif op_type == UsdGeom.XformOp.TypeScale:
                transform["scale"] = self._format_vec3(value)
                
            elif op_type == UsdGeom.XformOp.TypeTransform:
                # Matrix transform
                matrix = value
                transform["position"] = self._format_vec3(matrix.ExtractTranslation())
                transform["rotation"] = self._format_rotation(matrix)
                transform["scale"] = self._format_vec3(matrix.ExtractScale())
                
        return transform
    
    def _get_important_metadata(self, prim: Usd.Prim) -> Dict[str, Any]:
        """Extract important metadata from a prim"""
        metadata = {}
        
        # Handle common important metadata
        for key in ["kind", "purpose", "instanceable", "active", "hidden"]:
            if prim.HasMetadata(key):
                metadata[key] = prim.GetMetadata(key)
                
        # Look for USD attributes that might be metadata
        for attr_name in ["semanticLabel", "semanticType", "label", "category", "class"]:
            if prim.HasAttribute(attr_name):
                attr = prim.GetAttribute(attr_name)
                if attr.IsValid():
                    metadata[attr_name] = attr.Get(self._scan_time)
                    
        # Look for Isaac Sim specific semantic data
        if prim.HasAttribute("userProperties:semanticLabel"):
            attr = prim.GetAttribute("userProperties:semanticLabel")
            if attr.IsValid():
                metadata["semantic_label"] = attr.Get(self._scan_time)
                
        return metadata 
    
    def _format_vec3(self, vec) -> str:
        """Format a vector3 as a string"""
        if isinstance(vec, (list, tuple)):
            return f"{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}"
        else:
            return f"{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}"

    def _format_rotation(self, matrix) -> str:
        """Format a rotation from a matrix as a string in Euler angles (degrees)"""
        rotation = matrix.ExtractRotation()
        euler = rotation.DecomposeRotation("XYZ", True)
        return f"{euler[0]:.3f}, {euler[1]:.3f}, {euler[2]:.3f}"

    def _format_scale(self, scale) -> str:
        """Format a scale vector as a string"""
        return f"{scale[0]:.3f}, {scale[1]:.3f}, {scale[2]:.3f}"