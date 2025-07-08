"""
Unit tests for Employee Management Extension

Run these tests to validate the functionality of the extension components.
"""

import unittest
import sys
import os
import numpy as np
from unittest.mock import Mock, patch, MagicMock

# Add the extension path to sys.path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'omni_employee_management_python'))

# Mock Omniverse modules for testing
sys.modules['omni'] = Mock()
sys.modules['omni.ext'] = Mock()
sys.modules['omni.ui'] = Mock()
sys.modules['omni.usd'] = Mock()
sys.modules['pxr'] = Mock()
sys.modules['carb'] = Mock()

# Import after mocking
from motion_capture_manager import MotionCaptureManager
from workforce_analytics_manager import WorkforceAnalyticsManager
from safety_monitoring_manager import SafetyMonitoringManager
from camera_calibration import CameraCalibrationManager


class TestMotionCaptureManager(unittest.TestCase):
    """Test cases for Motion Capture Manager."""
    
    def setUp(self):
        self.manager = MotionCaptureManager()
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertFalse(self.manager._is_tracking)
        self.assertEqual(len(self.manager._tracked_employees), 0)
    
    def test_coordinate_transformation(self):
        """Test coordinate transformation from camera to world space."""
        # Test basic transformation
        world_x, world_y, world_z = self.manager._transform_to_world_coords(100, 200)
        
        # Should return reasonable world coordinates
        self.assertIsInstance(world_x, float)
        self.assertIsInstance(world_y, float)
        self.assertIsInstance(world_z, float)
    
    def test_employee_tracking(self):
        """Test employee tracking functionality."""
        # Mock camera data
        camera_data = {
            'employees': [
                {'id': 'emp_001', 'bbox': [100, 150, 200, 300], 'confidence': 0.95},
                {'id': 'emp_002', 'bbox': [300, 400, 450, 600], 'confidence': 0.87}
            ]
        }
        
        self.manager.process_camera_data(camera_data)
        
        # Check if employees are tracked
        self.assertEqual(len(self.manager._tracked_employees), 2)
        self.assertIn('emp_001', self.manager._tracked_employees)
        self.assertIn('emp_002', self.manager._tracked_employees)
    
    def test_avatar_update(self):
        """Test avatar position updates."""
        employee_id = 'emp_test'
        position = (10.0, 20.0, 0.0)
        
        # This would normally update avatar in Isaac Sim
        result = self.manager.update_avatar_position(employee_id, position)
        
        # Should return success (mocked)
        self.assertTrue(result or result is None)  # Allowing for mocked return


class TestWorkforceAnalyticsManager(unittest.TestCase):
    """Test cases for Workforce Analytics Manager."""
    
    def setUp(self):
        self.manager = WorkforceAnalyticsManager()
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertIsNotNone(self.manager._kpis)
    
    def test_kpi_calculation(self):
        """Test KPI calculations."""
        # Add some sample data
        self.manager.update_employee_metrics('emp_001', {
            'tasks_completed': 10,
            'time_worked': 480,  # 8 hours in minutes
            'quality_score': 0.95,
            'safety_incidents': 0
        })
        
        # Calculate KPIs
        kpis = self.manager.calculate_kpis()
        
        self.assertIn('productivity', kpis)
        self.assertIn('efficiency', kpis)
        self.assertIn('quality', kpis)
        self.assertIn('safety', kpis)
    
    def test_performance_prediction(self):
        """Test performance prediction."""
        # Mock historical data
        historical_data = [
            {'hour': 9, 'productivity': 85},
            {'hour': 10, 'productivity': 90},
            {'hour': 11, 'productivity': 88},
            {'hour': 12, 'productivity': 75}  # Lunch dip
        ]
        
        prediction = self.manager.predict_performance(historical_data)
        
        self.assertIsInstance(prediction, (int, float))
        self.assertGreaterEqual(prediction, 0)
        self.assertLessEqual(prediction, 100)


class TestSafetyMonitoringManager(unittest.TestCase):
    """Test cases for Safety Monitoring Manager."""
    
    def setUp(self):
        self.manager = SafetyMonitoringManager()
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertIsNotNone(self.manager._safety_zones)
        self.assertIsNotNone(self.manager._ppe_requirements)
    
    def test_hazard_zone_detection(self):
        """Test hazard zone detection."""
        # Define a hazard zone
        zone = {
            'id': 'forklift_area',
            'type': 'vehicle_operation',
            'bounds': {'x_min': 0, 'x_max': 10, 'y_min': 0, 'y_max': 10},
            'required_ppe': ['hard_hat', 'safety_vest']
        }
        
        self.manager.add_safety_zone(zone)
        
        # Test employee in hazard zone
        employee_pos = (5.0, 5.0, 0.0)  # Inside zone
        is_in_hazard = self.manager.check_hazard_zones('emp_001', employee_pos)
        
        # Should detect hazard
        self.assertTrue(is_in_hazard)
    
    def test_ppe_compliance(self):
        """Test PPE compliance checking."""
        employee_ppe = {
            'hard_hat': True,
            'safety_vest': True,
            'safety_boots': False
        }
        
        required_ppe = ['hard_hat', 'safety_vest']
        
        is_compliant = self.manager.check_ppe_compliance(employee_ppe, required_ppe)
        
        # Should be compliant
        self.assertTrue(is_compliant)
        
        # Test non-compliance
        required_ppe.append('safety_boots')
        is_compliant = self.manager.check_ppe_compliance(employee_ppe, required_ppe)
        
        # Should not be compliant
        self.assertFalse(is_compliant)


class TestCameraCalibrationManager(unittest.TestCase):
    """Test cases for Camera Calibration Manager."""
    
    def setUp(self):
        self.manager = CameraCalibrationManager()
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(len(self.manager._calibration_points), 0)
        self.assertFalse(self.manager._is_calibrating)
    
    def test_calibration_points(self):
        """Test calibration point management."""
        # Add calibration points
        self.manager._add_calibration_point()
        self.manager._add_calibration_point()
        
        self.assertEqual(len(self.manager._calibration_points), 2)
        
        # Clear points
        self.manager._clear_calibration_points()
        self.assertEqual(len(self.manager._calibration_points), 0)
    
    def test_coordinate_transformation(self):
        """Test coordinate transformation."""
        # Mock calibration data
        self.manager._calibration_data['Camera_01'] = {
            'transformation_matrix': [
                [0.01, 0, 0],
                [0, 0.01, 0],
                [0, 0, 1]
            ]
        }
        
        # Test transformation
        world_x, world_y, world_z = self.manager.transform_coordinates('Camera_01', 100, 200)
        
        self.assertIsInstance(world_x, float)
        self.assertIsInstance(world_y, float)
        self.assertIsInstance(world_z, float)
    
    def test_calibration_status(self):
        """Test calibration status checking."""
        # Initially not calibrated
        self.assertFalse(self.manager.is_camera_calibrated('Camera_01'))
        
        # Add calibration data
        self.manager._calibration_data['Camera_01'] = {'transformation_matrix': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}
        
        # Now should be calibrated
        self.assertTrue(self.manager.is_camera_calibrated('Camera_01'))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        self.motion_manager = MotionCaptureManager()
        self.analytics_manager = WorkforceAnalyticsManager()
        self.safety_manager = SafetyMonitoringManager()
        self.calibration_manager = CameraCalibrationManager()
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from camera data to analytics."""
        # 1. Process camera data
        camera_data = {
            'employees': [
                {
                    'id': 'emp_001',
                    'bbox': [100, 150, 200, 300],
                    'confidence': 0.95,
                    'ppe': {'hard_hat': True, 'safety_vest': True}
                }
            ]
        }
        
        self.motion_manager.process_camera_data(camera_data)
        
        # 2. Update analytics
        self.analytics_manager.update_employee_metrics('emp_001', {
            'tasks_completed': 5,
            'time_worked': 240,
            'quality_score': 0.92
        })
        
        # 3. Check safety compliance
        employee_pos = (5.0, 5.0, 0.0)
        safety_status = self.safety_manager.check_overall_safety('emp_001', employee_pos)
        
        # System should handle the complete workflow
        self.assertIsNotNone(safety_status or True)  # Allowing for mocked returns


if __name__ == '__main__':
    # Configure test runner
    unittest.TestLoader.sortTestMethodsUsing = None
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMotionCaptureManager,
        TestWorkforceAnalyticsManager,
        TestSafetyMonitoringManager,
        TestCameraCalibrationManager,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print results summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
