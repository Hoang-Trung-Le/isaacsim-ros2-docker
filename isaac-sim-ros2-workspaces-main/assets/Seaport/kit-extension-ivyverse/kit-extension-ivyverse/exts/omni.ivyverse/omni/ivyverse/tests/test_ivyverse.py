import omni.kit.test
import omni.usd
from pxr import Usd, UsdGeom
class TestIvyverse(omni.kit.test.AsyncTestCase):
    """Test cases for Ivyverse extension"""
    
    async def setUp(self):
        """Set up test environment"""
        self._stage = omni.usd.get_context().get_stage()
        
    async def test_extension_load(self):
        """Test if extension loads correctly"""
        import omni.ivyverse
        self.assertIsNotNone(omni.ivyverse)
    
    async def test_scene_analyzer(self):
        """Test scene analyzer functionality"""
        from omni.ivyverse.scene_analyzer import SceneAnalyzer
        
        analyzer = SceneAnalyzer()
        analysis = analyzer.analyze_current_scene()
        self.assertIsInstance(analysis, str)
    
    async def test_llm_manager(self):
        """Test LLM manager initialization"""
        from omni.ivyverse.llm_manager import LLMManager
        
        manager = LLMManager()
        self.assertIn("NVIDIA NIM", manager.providers)
        self.assertIn("OpenAI GPT-4o", manager.providers)
    
    async def test_utils(self):
        """Test utility functions"""
        from omni.ivyverse.utils import format_usd_path, extract_prim_name
        
        # Test path formatting
        self.assertEqual(format_usd_path("test"), "/test")
        self.assertEqual(format_usd_path("/test"), "/test")
        
        # Test name extraction
        self.assertEqual(extract_prim_name("/World/Cube"), "Cube")
        self.assertEqual(extract_prim_name("/"), "")
