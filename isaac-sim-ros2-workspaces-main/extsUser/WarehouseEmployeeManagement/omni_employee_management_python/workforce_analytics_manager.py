import carb
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from .global_variables import ANALYTICS_UPDATE_INTERVAL


class WorkforceAnalyticsManager:
    """
    Comprehensive workforce analytics and performance monitoring
    Tracks KPIs, productivity metrics, and generates insights
    """

    def __init__(self):
        self.settings = carb.settings.get_settings()
        self.analytics_active = False
        
        # Data storage
        self.employee_metrics = defaultdict(dict)
        self.workstation_metrics = defaultdict(dict)
        self.historical_data = defaultdict(lambda: deque(maxlen=1000))  # Keep last 1000 data points
        
        # Performance tracking
        self.productivity_data = {}
        self.efficiency_data = {}
        self.quality_data = {}
        self.safety_data = {}
        
        # Time tracking
        self.session_start_time = time.time()
        self.last_update_time = time.time()
        
        # KPI definitions
        self.kpis = {
            "productivity": {
                "name": "Productivity Rate",
                "unit": "tasks/hour",
                "target": 20.0,
                "calculation": "tasks_completed / hours_worked"
            },
            "efficiency": {
                "name": "Efficiency Score",
                "unit": "%",
                "target": 85.0,
                "calculation": "(actual_output / expected_output) * 100"
            },
            "quality": {
                "name": "Quality Score",
                "unit": "%",
                "target": 95.0,
                "calculation": "(successful_tasks / total_tasks) * 100"
            },
            "safety_compliance": {
                "name": "Safety Compliance",
                "unit": "%",
                "target": 100.0,
                "calculation": "(compliant_time / total_time) * 100"
            },
            "utilization": {
                "name": "Utilization Rate",
                "unit": "%",
                "target": 80.0,
                "calculation": "(active_time / available_time) * 100"
            }
        }

    def initialize_analytics(self) -> bool:
        """Initialize the analytics system"""
        try:
            self.analytics_active = True
            self.session_start_time = time.time()
            carb.log_info("Workforce Analytics: System initialized")
            return True
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to initialize: {str(e)}")
            return False

    def update_employee_position_data(self, employee_id: str, position: Tuple[float, float, float], timestamp: float = None):
        """Update employee position for analytics tracking"""
        if timestamp is None:
            timestamp = time.time()
            
        try:
            if employee_id not in self.employee_metrics:
                self.employee_metrics[employee_id] = {
                    "positions": deque(maxlen=100),
                    "movement_distance": 0.0,
                    "zone_time": defaultdict(float),
                    "last_position": None,
                    "start_time": timestamp
                }
            
            employee_data = self.employee_metrics[employee_id]
            
            # Calculate movement if we have a previous position
            if employee_data["last_position"]:
                distance = self._calculate_distance(employee_data["last_position"], position)
                employee_data["movement_distance"] += distance
            
            # Store position with timestamp
            employee_data["positions"].append({
                "position": position,
                "timestamp": timestamp
            })
            employee_data["last_position"] = position
            
            # Update zone time tracking
            zone = self._get_zone_from_position(position)
            if zone:
                time_delta = timestamp - self.last_update_time
                employee_data["zone_time"][zone] += time_delta
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to update position data: {str(e)}")

    def record_task_completion(self, employee_id: str, task_data: Dict[str, Any]):
        """Record task completion for productivity tracking"""
        try:
            timestamp = time.time()
            
            if employee_id not in self.productivity_data:
                self.productivity_data[employee_id] = {
                    "tasks_completed": 0,
                    "tasks_failed": 0,
                    "total_task_time": 0.0,
                    "quality_scores": deque(maxlen=50),
                    "task_history": deque(maxlen=100)
                }
            
            emp_data = self.productivity_data[employee_id]
            
            # Update task counts
            if task_data.get("success", True):
                emp_data["tasks_completed"] += 1
            else:
                emp_data["tasks_failed"] += 1
            
            # Record task time
            task_time = task_data.get("duration", 0)
            emp_data["total_task_time"] += task_time
            
            # Record quality score
            quality_score = task_data.get("quality_score", 100)
            emp_data["quality_scores"].append(quality_score)
            
            # Store task history
            emp_data["task_history"].append({
                "timestamp": timestamp,
                "task_type": task_data.get("task_type", "unknown"),
                "duration": task_time,
                "success": task_data.get("success", True),
                "quality_score": quality_score
            })
            
            carb.log_info(f"Workforce Analytics: Recorded task completion for {employee_id}")
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to record task completion: {str(e)}")

    def calculate_kpis(self, employee_id: str = None) -> Dict[str, Any]:
        """Calculate KPIs for specific employee or all employees"""
        try:
            current_time = time.time()
            session_duration = current_time - self.session_start_time
            
            if employee_id:
                return self._calculate_employee_kpis(employee_id, session_duration)
            else:
                # Calculate aggregate KPIs
                all_kpis = {}
                employee_kpis = {}
                
                for emp_id in self.employee_metrics.keys():
                    employee_kpis[emp_id] = self._calculate_employee_kpis(emp_id, session_duration)
                
                # Calculate overall metrics
                all_kpis["employees"] = employee_kpis
                all_kpis["aggregate"] = self._calculate_aggregate_kpis(employee_kpis)
                all_kpis["session_duration"] = session_duration
                all_kpis["timestamp"] = current_time
                
                return all_kpis
                
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to calculate KPIs: {str(e)}")
            return {}

    def _calculate_employee_kpis(self, employee_id: str, session_duration: float) -> Dict[str, Any]:
        """Calculate KPIs for a specific employee"""
        kpis = {}
        
        try:
            # Get employee data
            emp_metrics = self.employee_metrics.get(employee_id, {})
            emp_productivity = self.productivity_data.get(employee_id, {})
            
            # Calculate productivity rate
            tasks_completed = emp_productivity.get("tasks_completed", 0)
            hours_worked = session_duration / 3600  # Convert to hours
            productivity_rate = tasks_completed / hours_worked if hours_worked > 0 else 0
            kpis["productivity"] = {
                "value": productivity_rate,
                "target": self.kpis["productivity"]["target"],
                "unit": self.kpis["productivity"]["unit"],
                "status": "good" if productivity_rate >= self.kpis["productivity"]["target"] else "warning"
            }
            
            # Calculate efficiency score
            total_tasks = emp_productivity.get("tasks_completed", 0) + emp_productivity.get("tasks_failed", 0)
            efficiency = (tasks_completed / total_tasks * 100) if total_tasks > 0 else 100
            kpis["efficiency"] = {
                "value": efficiency,
                "target": self.kpis["efficiency"]["target"],
                "unit": self.kpis["efficiency"]["unit"],
                "status": "good" if efficiency >= self.kpis["efficiency"]["target"] else "warning"
            }
            
            # Calculate quality score
            quality_scores = emp_productivity.get("quality_scores", [])
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 100
            kpis["quality"] = {
                "value": avg_quality,
                "target": self.kpis["quality"]["target"],
                "unit": self.kpis["quality"]["unit"],
                "status": "good" if avg_quality >= self.kpis["quality"]["target"] else "warning"
            }
            
            # Calculate movement metrics
            movement_distance = emp_metrics.get("movement_distance", 0)
            kpis["movement_distance"] = {
                "value": movement_distance,
                "unit": "meters",
                "description": "Total distance moved during session"
            }
            
            # Calculate zone utilization
            zone_times = emp_metrics.get("zone_time", {})
            kpis["zone_utilization"] = dict(zone_times)
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Error calculating employee KPIs: {str(e)}")
        
        return kpis

    def _calculate_aggregate_kpis(self, employee_kpis: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate aggregate KPIs across all employees"""
        aggregate = {}
        
        try:
            if not employee_kpis:
                return aggregate
            
            # Calculate averages for key metrics
            metrics = ["productivity", "efficiency", "quality"]
            
            for metric in metrics:
                values = []
                for emp_id, emp_kpis in employee_kpis.items():
                    if metric in emp_kpis:
                        values.append(emp_kpis[metric]["value"])
                
                if values:
                    avg_value = sum(values) / len(values)
                    target = self.kpis[metric]["target"]
                    aggregate[metric] = {
                        "value": avg_value,
                        "target": target,
                        "unit": self.kpis[metric]["unit"],
                        "status": "good" if avg_value >= target else "warning",
                        "employee_count": len(values)
                    }
            
            # Calculate total movement
            total_movement = sum(
                emp_kpis.get("movement_distance", {}).get("value", 0)
                for emp_kpis in employee_kpis.values()
            )
            aggregate["total_movement"] = {
                "value": total_movement,
                "unit": "meters",
                "description": "Total movement by all employees"
            }
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Error calculating aggregate KPIs: {str(e)}")
        
        return aggregate

    def generate_heat_map_data(self, zone_resolution: float = 1.0) -> Dict[str, Any]:
        """Generate heat map data for employee movement patterns"""
        try:
            heat_map = defaultdict(int)
            
            for employee_id, emp_data in self.employee_metrics.items():
                positions = emp_data.get("positions", [])
                for pos_data in positions:
                    position = pos_data["position"]
                    # Discretize position for heat map
                    x_grid = int(position[0] / zone_resolution)
                    y_grid = int(position[1] / zone_resolution)
                    heat_map[(x_grid, y_grid)] += 1
            
            return {
                "heat_map": dict(heat_map),
                "resolution": zone_resolution,
                "total_points": sum(heat_map.values())
            }
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to generate heat map: {str(e)}")
            return {}

    def get_performance_trends(self, employee_id: str = None, metric: str = "productivity") -> Dict[str, Any]:
        """Get performance trends over time"""
        try:
            if employee_id:
                return self._get_employee_trends(employee_id, metric)
            else:
                # Get trends for all employees
                trends = {}
                for emp_id in self.employee_metrics.keys():
                    trends[emp_id] = self._get_employee_trends(emp_id, metric)
                return trends
                
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to get performance trends: {str(e)}")
            return {}

    def _get_employee_trends(self, employee_id: str, metric: str) -> List[Dict[str, Any]]:
        """Get trends for a specific employee"""
        trends = []
        
        try:
            emp_productivity = self.productivity_data.get(employee_id, {})
            task_history = emp_productivity.get("task_history", [])
            
            # Group tasks by time windows (e.g., hourly)
            time_windows = defaultdict(list)
            for task in task_history:
                window = int(task["timestamp"] // 3600)  # Hourly windows
                time_windows[window].append(task)
            
            # Calculate metric for each time window
            for window, tasks in time_windows.items():
                if metric == "productivity":
                    value = len([t for t in tasks if t["success"]])
                elif metric == "quality":
                    quality_scores = [t["quality_score"] for t in tasks]
                    value = sum(quality_scores) / len(quality_scores) if quality_scores else 0
                elif metric == "efficiency":
                    successful = len([t for t in tasks if t["success"]])
                    value = (successful / len(tasks) * 100) if tasks else 0
                else:
                    value = 0
                
                trends.append({
                    "timestamp": window * 3600,
                    "value": value,
                    "task_count": len(tasks)
                })
            
            # Sort by timestamp
            trends.sort(key=lambda x: x["timestamp"])
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Error getting employee trends: {str(e)}")
        
        return trends

    def export_analytics_data(self, format: str = "json") -> Optional[str]:
        """Export analytics data in specified format"""
        try:
            data = {
                "session_info": {
                    "start_time": self.session_start_time,
                    "duration": time.time() - self.session_start_time,
                    "export_time": time.time()
                },
                "kpis": self.calculate_kpis(),
                "heat_map": self.generate_heat_map_data(),
                "trends": self.get_performance_trends()
            }
            
            if format == "json":
                import json
                return json.dumps(data, indent=2, default=str)
            else:
                carb.log_error(f"Workforce Analytics: Unsupported export format: {format}")
                return None
                
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to export data: {str(e)}")
            return None

    def reset_analytics(self):
        """Reset all analytics data"""
        try:
            self.employee_metrics.clear()
            self.productivity_data.clear()
            self.efficiency_data.clear()
            self.quality_data.clear()
            self.safety_data.clear()
            self.session_start_time = time.time()
            carb.log_info("Workforce Analytics: Data reset complete")
            
        except Exception as e:
            carb.log_error(f"Workforce Analytics: Failed to reset data: {str(e)}")

    def _calculate_distance(self, pos1: Tuple[float, float, float], pos2: Tuple[float, float, float]) -> float:
        """Calculate Euclidean distance between two positions"""
        return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2 + (pos2[2] - pos1[2]) ** 2) ** 0.5

    def _get_zone_from_position(self, position: Tuple[float, float, float]) -> Optional[str]:
        """Determine zone from position (customize based on your layout)"""
        x, y, z = position
        
        # Example zone mapping - customize for your warehouse layout
        if x < -10:
            return "warehouse_left"
        elif x > 10:
            return "warehouse_right"
        elif y < -10:
            return "warehouse_back"
        elif y > 10:
            return "warehouse_front"
        else:
            return "warehouse_center"

    def get_analytics_status(self) -> Dict[str, Any]:
        """Get current analytics system status"""
        return {
            "active": self.analytics_active,
            "session_duration": time.time() - self.session_start_time,
            "tracked_employees": len(self.employee_metrics),
            "total_tasks_recorded": sum(
                data.get("tasks_completed", 0) + data.get("tasks_failed", 0)
                for data in self.productivity_data.values()
            ),
            "data_points": sum(len(data.get("positions", [])) for data in self.employee_metrics.values())
        }
