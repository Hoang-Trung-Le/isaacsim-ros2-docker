import omni.usd
from pxr import Usd, UsdGeom, Gf
from typing import Dict, List, Any, Optional
from collections import defaultdict
class SceneAnalyzer:
    """Analyzes USD scene structure and content"""
    
    def __init__(self):
        self._context = omni.usd.get_context()
        self._stage = None
        self._prim_type_count = defaultdict(int)
        self._all_prims = []
        
    def analyze_current_scene(self) -> str:
        """Analyze the current USD scene and return summary"""
        self._stage = self._context.get_stage()
        
        if not self._stage:
            return "No USD stage loaded"
            
        # Cache all prims for faster analysis
        self._all_prims = list(self._stage.Traverse())
        self._count_prim_types()
        
        # Get scene metrics
        prim_count = len(self._all_prims)
        meshes = self._get_meshes_list()
        materials = self._get_materials_list()
        lights = self._get_lights_list()
        cameras = self._get_cameras_list()
        xforms = self._get_xforms_list()
        
        # Get world bounds
        bounds = self._get_world_bounds()
        
        # Build summary
        summary = f"""Scene Analysis:
- Total Prims: {prim_count}
- Meshes: {len(meshes)}
- Materials: {len(materials)}
- Lights: {len(lights)}
- Cameras: {len(cameras)}
- Xforms: {len(xforms)}
- Root Prim: {self._stage.GetRootLayer().GetDisplayName()}
- Default Prim: {self._stage.GetDefaultPrim().GetPath() if self._stage.GetDefaultPrim() else 'None'}
- World Bounds: {bounds}
- Time: {self._stage.GetStartTimeCode()} - {self._stage.GetEndTimeCode()}
Prim Type Distribution:
{self._format_prim_types()}
Detailed Object Lists:
{self._format_object_lists()}
"""
        return summary
    
    def _count_prim_types(self):
        """Count all prim types in the scene"""
        self._prim_type_count.clear()
        for prim in self._all_prims:
            prim_type = prim.GetTypeName()
            if prim_type:
                self._prim_type_count[prim_type] += 1
            else:
                # Check if it might be a scope or other type
                if prim.IsA(UsdGeom.Scope):
                    self._prim_type_count["Scope"] += 1
                else:
                    self._prim_type_count["Typeless"] += 1
                    
    def _format_prim_types(self) -> str:
        """Format prim type distribution"""
        lines = []
        for prim_type, count in sorted(self._prim_type_count.items()):
            lines.append(f"  - {prim_type}: {count}")
        return "\n".join(lines) if lines else "  None"
        
    def _format_object_lists(self) -> str:
        """Format detailed object lists"""
        lines = []
        
        # Meshes
        meshes = self._get_meshes_list()
        if meshes:
            lines.append(f"\nMeshes ({len(meshes)}):")
            for mesh in meshes[:10]:
                lines.append(f"  - {mesh['path']} ({mesh['vertex_count']} vertices)")
                
        # Lights
        lights = self._get_lights_list()
        if lights:
            lines.append(f"\nLights ({len(lights)}):")
            for light in lights:
                lines.append(f"  - {light['path']} ({light['type']})")
                
        # Materials
        materials = self._get_materials_list()
        if materials:
            lines.append(f"\nMaterials ({len(materials)}):")
            for material in materials[:10]:
                lines.append(f"  - {material['path']} ({material['type']})")
                
        return "\n".join(lines) if lines else "  No objects found"
    
    def get_objects_list(self) -> Dict[str, Any]:
        """Get categorized list of all objects in the scene"""
        return {
            "meshes": self._get_meshes_list(),
            "lights": self._get_lights_list(),
            "cameras": self._get_cameras_list(),
            "xforms": self._get_xforms_list(),
            "materials": self._get_materials_list(),
            "scopes": self._get_scopes_list(),
            "other": self._get_other_prims()
        }
    
    def get_prim_info(self, prim_path: str) -> Dict[str, Any]:
        """Get detailed information about a specific prim"""
        if not self._stage:
            self._stage = self._context.get_stage()
            if not self._stage:
                return {"error": "No stage loaded"}
        
        prim = self._stage.GetPrimAtPath(prim_path)
        if not prim:
            return {"error": f"Prim not found: {prim_path}"}
        
        info = {
            "path": str(prim.GetPath()),
            "type": prim.GetTypeName(),
            "active": prim.IsActive(),
            "children": [str(child.GetPath()) for child in prim.GetChildren()],
            "attributes": {}
        }
        
        # Get attributes
        for attr in prim.GetAttributes():
            try:
                value = attr.Get()
                # Convert Gf types to lists for JSON serialization
                if hasattr(value, '__len__') and not isinstance(value, str):
                    value = list(value)
                info["attributes"][attr.GetName()] = value
            except:
                info["attributes"][attr.GetName()] = "Unable to read"
        
        # Get transform if applicable
        if prim.IsA(UsdGeom.Xformable):
            xform = UsdGeom.Xformable(prim)
            matrix = xform.GetLocalTransformation()
            info["transform"] = {
                "translation": list(matrix.ExtractTranslation()),
                "rotation": list(matrix.ExtractRotation().GetQuaternion()),
                "scale": list(Gf.Vec3d(matrix.GetRow3(0).GetLength(),
                                      matrix.GetRow3(1).GetLength(),
                                      matrix.GetRow3(2).GetLength()))
            }
        
        # Get material binding if exists
        if prim.HasAPI(UsdGeom.MaterialBindingAPI):
            binding_api = UsdGeom.MaterialBindingAPI(prim)
            material = binding_api.GetDirectBinding().GetMaterial()
            if material:
                info["material"] = str(material.GetPath())
                
        # Get bounds if it's a geometric prim
        if prim.IsA(UsdGeom.Gprim):
            bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default"])
            bbox = bbox_cache.ComputeLocalBound(prim)
            bbox_range = bbox.GetRange()
            if not bbox_range.IsEmpty():
                info["bounds"] = {
                    "min": list(bbox_range.GetMin()),
                    "max": list(bbox_range.GetMax()),
                    "size": list(bbox_range.GetSize())
                }
        
        return info
    
    def search_prims(self, query: str) -> List[str]:
        """Search for prims matching query"""
        if not self._stage:
            self._stage = self._context.get_stage()
            if not self._stage:
                return []
            self._all_prims = list(self._stage.Traverse())
        
        results = []
        query_lower = query.lower()
        
        for prim in self._all_prims:
            path_str = str(prim.GetPath())
            prim_name = prim.GetName().lower()
            prim_type = prim.GetTypeName().lower()
            
            if (query_lower in path_str.lower() or 
                query_lower in prim_name or 
                query_lower in prim_type):
                results.append(path_str)
        
        return results
    
    def get_hierarchy(self, root_path: str = "/") -> Dict[str, Any]:
        """Get scene hierarchy from root path"""
        if not self._stage:
            self._stage = self._context.get_stage()
            if not self._stage:
                return {"error": "No stage loaded"}
        
        root_prim = self._stage.GetPrimAtPath(root_path)
        if not root_prim:
            return {"error": f"Invalid root path: {root_path}"}
        
        def build_hierarchy(prim, max_depth=5, current_depth=0):
            if current_depth >= max_depth:
                return {
                    "name": prim.GetName(),
                    "path": str(prim.GetPath()),
                    "type": prim.GetTypeName(),
                    "children": ["... (max depth reached)"]
                }
                
            return {
                "name": prim.GetName(),
                "path": str(prim.GetPath()),
                "type": prim.GetTypeName(),
                "children": [build_hierarchy(child, max_depth, current_depth + 1) 
                           for child in prim.GetChildren()]
            }
        
        return build_hierarchy(root_prim)
    
    def get_detailed_analysis(self) -> Dict[str, Any]:
        """Get comprehensive scene analysis"""
        if not self._stage:
            self._stage = self._context.get_stage()
            if not self._stage:
                return {"error": "No stage loaded"}
        
        objects = self.get_objects_list()
        
        analysis = {
            "overview": self.analyze_current_scene(),
            "hierarchy": self.get_hierarchy(),
            "objects": objects,
            "statistics": {
                "total_prims": len(self._all_prims),
                "meshes": len(objects["meshes"]),
                "lights": len(objects["lights"]),
                "cameras": len(objects["cameras"]),
                "materials": len(objects["materials"]),
                "xforms": len(objects["xforms"])
            }
        }
        
        return analysis
    
    def _get_world_bounds(self) -> str:
        """Calculate world bounds of the scene"""
        if not self._stage:
            return "Unknown"
        
        try:
            bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default", "render"])
            root_bbox = bbox_cache.ComputeWorldBound(self._stage.GetPseudoRoot())
            
            # Check if bbox is empty by comparing the range
            bbox_range = root_bbox.GetRange()
            if bbox_range.IsEmpty():
                return "Empty"
            
            min_pt = bbox_range.GetMin()
            max_pt = bbox_range.GetMax()
            size = bbox_range.GetSize()
            
            return f"Min: ({min_pt[0]:.2f}, {min_pt[1]:.2f}, {min_pt[2]:.2f}) " \
                   f"Max: ({max_pt[0]:.2f}, {max_pt[1]:.2f}, {max_pt[2]:.2f}) " \
                   f"Size: ({size[0]:.2f}, {size[1]:.2f}, {size[2]:.2f})"
        except Exception as e:
            return f"Error computing bounds: {str(e)}"
    
    def _get_materials_list(self) -> List[Dict[str, str]]:
        """Get list of all materials in the scene"""
        materials = []
        material_types = ["Material", "Shader", "NodeGraph", "MaterialBinding"]
        
        for prim in self._all_prims:
            prim_type = prim.GetTypeName()
            prim_path_str = str(prim.GetPath())
            
            if (prim_type in material_types or 
                "material" in prim_type.lower() or
                "shader" in prim_type.lower() or
                "material" in prim_path_str.lower() or
                "shader" in prim_path_str.lower()):
                materials.append({
                    "path": prim_path_str,
                    "name": prim.GetName(),
                    "type": prim_type
                })
        return materials
    
    def _get_meshes_list(self) -> List[Dict[str, Any]]:
        """Get list of all meshes with basic info"""
        meshes = []
        for prim in self._all_prims:
            if prim.IsA(UsdGeom.Mesh):
                mesh = UsdGeom.Mesh(prim)
                points_attr = mesh.GetPointsAttr()
                vertex_count = 0
                if points_attr and points_attr.Get():
                    vertex_count = len(points_attr.Get())
                
                face_count = 0
                face_vertex_counts = mesh.GetFaceVertexCountsAttr()
                if face_vertex_counts and face_vertex_counts.Get():
                    face_count = len(face_vertex_counts.Get())
                
                meshes.append({
                    "path": str(prim.GetPath()),
                    "name": prim.GetName(),
                    "vertex_count": vertex_count,
                    "face_count": face_count
                })
        return meshes
    
    def _get_lights_list(self) -> List[Dict[str, str]]:
        """Get list of all lights in the scene"""
        lights = []
        light_types = ["Light", "DistantLight", "RectLight", 
                      "SphereLight", "DiskLight", "CylinderLight", 
                      "DomeLight", "PortalLight"]
        
        for prim in self._all_prims:
            prim_type = prim.GetTypeName()
            # Check if prim type is in our list of light types
            if (prim_type in light_types or
                "light" in prim_type.lower()):
                lights.append({
                    "path": str(prim.GetPath()),
                    "name": prim.GetName(),
                    "type": prim_type
                })
        return lights
    
    def _get_cameras_list(self) -> List[Dict[str, str]]:
        """Get list of all cameras in the scene"""
        cameras = []
        for prim in self._all_prims:
            if prim.IsA(UsdGeom.Camera) or prim.GetTypeName() == "Camera":
                cameras.append({
                    "path": str(prim.GetPath()),
                    "name": prim.GetName(),
                    "type": prim.GetTypeName()
                })
        return cameras
    
    def _get_xforms_list(self) -> List[Dict[str, str]]:
        """Get list of all transform nodes"""
        xforms = []
        for prim in self._all_prims:
            if prim.IsA(UsdGeom.Xform) and not prim.IsA(UsdGeom.Camera):
                xforms.append({
                    "path": str(prim.GetPath()),
                    "name": prim.GetName(),
                    "type": prim.GetTypeName()
                })
        return xforms
    
    def _get_scopes_list(self) -> List[Dict[str, str]]:
        """Get list of all scope prims"""
        scopes = []
        for prim in self._all_prims:
            if prim.IsA(UsdGeom.Scope) or prim.GetTypeName() == "Scope":
                scopes.append({
                    "path": str(prim.GetPath()),
                    "name": prim.GetName(),
                    "type": prim.GetTypeName()
                })
        return scopes
    
    def _get_other_prims(self) -> List[Dict[str, str]]:
        """Get prims that don't fit in other categories"""
        categorized_paths = set()
        
        # Collect paths from all categories
        for mesh in self._get_meshes_list():
            categorized_paths.add(mesh["path"])
        for light in self._get_lights_list():
            categorized_paths.add(light["path"])
        for camera in self._get_cameras_list():
            categorized_paths.add(camera["path"])
        for xform in self._get_xforms_list():
            categorized_paths.add(xform["path"])
        for material in self._get_materials_list():
            categorized_paths.add(material["path"])
        for scope in self._get_scopes_list():
            categorized_paths.add(scope["path"])
            
        # Add uncategorized prims
        other = []
        for prim in self._all_prims:
            path = str(prim.GetPath())
            if path not in categorized_paths:
                other.append({
                    "path": path,
                    "name": prim.GetName(),
                    "type": prim.GetTypeName() or "Typeless"
                })
                
        return other
