#!/usr/bin/env python3
"""
System Information & Performance Monitor
A comprehensive utility for system diagnostics, performance monitoring, and system management
"""

import os
import sys
import platform
import psutil
import subprocess
import json
import time
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class SystemInfo:
    hostname: str
    os_name: str
    os_version: str
    architecture: str
    processor: str
    python_version: str
    uptime: str
    boot_time: str

@dataclass
class PerformanceMetrics:
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    load_average: Tuple[float, float, float]
    temperature: Optional[float]
    fan_speed: Optional[int]

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.monitoring = False
        self.log_file = "system_monitor.log"
        
    def get_system_info(self) -> SystemInfo:
        """Get comprehensive system information"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return SystemInfo(
                hostname=platform.node(),
                os_name=platform.system(),
                os_version=platform.release(),
                architecture=platform.machine(),
                processor=platform.processor() or "Unknown",
                python_version=platform.python_version(),
                uptime=str(uptime).split('.')[0],  # Remove microseconds
                boot_time=boot_time.strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Error getting system info: {e}")
            return None
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get current system performance metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network_io = psutil.net_io_counters()._asdict()
            
            # Load average (Unix-like systems)
            try:
                load_avg = os.getloadavg()
            except AttributeError:
                load_avg = (0.0, 0.0, 0.0)
            
            # Temperature and fan speed (if available)
            temperature = self.get_cpu_temperature()
            fan_speed = self.get_fan_speed()
            
            return PerformanceMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                load_average=load_avg,
                temperature=temperature,
                fan_speed=fan_speed
            )
        except Exception as e:
            print(f"Error getting performance metrics: {e}")
            return None
    
    def get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature if available"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            return entries[0].current
            return None
        except:
            return None
    
    def get_fan_speed(self) -> Optional[int]:
        """Get fan speed if available"""
        try:
            if hasattr(psutil, "sensors_fans"):
                fans = psutil.sensors_fans()
                if fans:
                    for name, entries in fans.items():
                        if entries:
                            return entries[0].current
            return None
        except:
            return None
    
    def get_process_info(self, limit: int = 10) -> List[Dict]:
        """Get information about running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:limit]
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get detailed memory information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_free': swap.free,
            'swap_percent': swap.percent
        }
    
    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk usage information for all mounted filesystems"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': (usage.used / usage.total) * 100
                })
            except PermissionError:
                continue
        return disks
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network interface information"""
        interfaces = {}
        for interface, addrs in psutil.net_if_addrs().items():
            interfaces[interface] = {
                'addresses': [addr._asdict() for addr in addrs],
                'stats': psutil.net_if_stats()[interface]._asdict() if interface in psutil.net_if_stats() else None
            }
        return interfaces
    
    def get_battery_info(self) -> Optional[Dict[str, Any]]:
        """Get battery information if available"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'secsleft': battery.secsleft,
                    'power_plugged': battery.power_plugged
                }
            return None
        except:
            return None
    
    def monitor_system(self, duration: int = 60, interval: int = 5) -> List[Dict]:
        """Monitor system performance over time"""
        print(f"Starting system monitoring for {duration} seconds...")
        print("Press Ctrl+C to stop monitoring early")
        
        self.monitoring = True
        data_points = []
        start_time = time.time()
        
        try:
            while self.monitoring and (time.time() - start_time) < duration:
                metrics = self.get_performance_metrics()
                if metrics:
                    data_points.append({
                        'timestamp': datetime.now().isoformat(),
                        'cpu_percent': metrics.cpu_percent,
                        'memory_percent': metrics.memory_percent,
                        'disk_percent': metrics.disk_percent,
                        'temperature': metrics.temperature
                    })
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        
        self.monitoring = False
        return data_points
    
    def generate_system_report(self) -> str:
        """Generate a comprehensive system report"""
        report = []
        report.append("=" * 60)
        report.append("SYSTEM INFORMATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # System Information
        sys_info = self.get_system_info()
        if sys_info:
            report.append("SYSTEM INFORMATION:")
            report.append("-" * 20)
            report.append(f"Hostname: {sys_info.hostname}")
            report.append(f"OS: {sys_info.os_name} {sys_info.os_version}")
            report.append(f"Architecture: {sys_info.architecture}")
            report.append(f"Processor: {sys_info.processor}")
            report.append(f"Python Version: {sys_info.python_version}")
            report.append(f"Uptime: {sys_info.uptime}")
            report.append(f"Boot Time: {sys_info.boot_time}")
            report.append("")
        
        # Performance Metrics
        metrics = self.get_performance_metrics()
        if metrics:
            report.append("PERFORMANCE METRICS:")
            report.append("-" * 20)
            report.append(f"CPU Usage: {metrics.cpu_percent:.1f}%")
            report.append(f"Memory Usage: {metrics.memory_percent:.1f}%")
            report.append(f"Disk Usage: {metrics.disk_percent:.1f}%")
            if metrics.temperature:
                report.append(f"CPU Temperature: {metrics.temperature:.1f}°C")
            if metrics.fan_speed:
                report.append(f"Fan Speed: {metrics.fan_speed} RPM")
            report.append("")
        
        # Memory Information
        memory_info = self.get_memory_info()
        report.append("MEMORY INFORMATION:")
        report.append("-" * 20)
        report.append(f"Total Memory: {self.format_bytes(memory_info['total'])}")
        report.append(f"Used Memory: {self.format_bytes(memory_info['used'])}")
        report.append(f"Available Memory: {self.format_bytes(memory_info['available'])}")
        report.append(f"Memory Usage: {memory_info['percent']:.1f}%")
        report.append(f"Swap Usage: {memory_info['swap_percent']:.1f}%")
        report.append("")
        
        # Disk Information
        disks = self.get_disk_info()
        report.append("DISK INFORMATION:")
        report.append("-" * 20)
        for disk in disks:
            report.append(f"Device: {disk['device']}")
            report.append(f"Mountpoint: {disk['mountpoint']}")
            report.append(f"Filesystem: {disk['fstype']}")
            report.append(f"Total: {self.format_bytes(disk['total'])}")
            report.append(f"Used: {self.format_bytes(disk['used'])} ({disk['percent']:.1f}%)")
            report.append(f"Free: {self.format_bytes(disk['free'])}")
            report.append("")
        
        # Top Processes
        processes = self.get_process_info(5)
        report.append("TOP PROCESSES (by CPU usage):")
        report.append("-" * 30)
        for proc in processes:
            report.append(f"{proc['name']:<20} PID: {proc['pid']:<8} CPU: {proc.get('cpu_percent', 0):.1f}%")
        report.append("")
        
        # Battery Information
        battery = self.get_battery_info()
        if battery:
            report.append("BATTERY INFORMATION:")
            report.append("-" * 20)
            report.append(f"Charge: {battery['percent']:.1f}%")
            report.append(f"Plugged: {'Yes' if battery['power_plugged'] else 'No'}")
            if battery['secsleft'] != psutil.POWER_TIME_UNLIMITED:
                report.append(f"Time Left: {battery['secsleft'] // 3600}h {(battery['secsleft'] % 3600) // 60}m")
            report.append("")
        
        return "\n".join(report)
    
    def format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def save_report(self, filename: str = None) -> str:
        """Save system report to file"""
        if filename is None:
            filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report = self.generate_system_report()
        with open(filename, 'w') as f:
            f.write(report)
        
        return filename
    
    def export_json(self, filename: str = None) -> str:
        """Export system data as JSON"""
        if filename is None:
            filename = f"system_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'system_info': asdict(self.get_system_info()) if self.get_system_info() else None,
            'performance_metrics': asdict(self.get_performance_metrics()) if self.get_performance_metrics() else None,
            'memory_info': self.get_memory_info(),
            'disk_info': self.get_disk_info(),
            'process_info': self.get_process_info(20),
            'network_info': self.get_network_info(),
            'battery_info': self.get_battery_info()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filename
    
    def cleanup_temp_files(self, older_than_days: int = 7) -> int:
        """Clean up temporary files older than specified days"""
        temp_dirs = ['/tmp', '/var/tmp', os.path.expanduser('~/tmp')]
        cleaned_count = 0
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                if os.path.getmtime(file_path) < time.time() - (older_than_days * 24 * 3600):
                                    os.remove(file_path)
                                    cleaned_count += 1
                            except (OSError, PermissionError):
                                continue
                except PermissionError:
                    continue
        
        return cleaned_count
    
    def check_disk_space(self, threshold: float = 90.0) -> List[Dict]:
        """Check disk space and return partitions above threshold"""
        warnings = []
        disks = self.get_disk_info()
        
        for disk in disks:
            if disk['percent'] > threshold:
                warnings.append({
                    'device': disk['device'],
                    'mountpoint': disk['mountpoint'],
                    'usage_percent': disk['percent'],
                    'free_space': self.format_bytes(disk['free'])
                })
        
        return warnings
    
    def get_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        metrics = self.get_performance_metrics()
        if not metrics:
            return {'score': 0, 'status': 'Unknown', 'issues': ['Unable to get metrics']}
        
        issues = []
        score = 100
        
        # CPU usage penalty
        if metrics.cpu_percent > 80:
            score -= 20
            issues.append("High CPU usage")
        elif metrics.cpu_percent > 60:
            score -= 10
            issues.append("Moderate CPU usage")
        
        # Memory usage penalty
        if metrics.memory_percent > 90:
            score -= 25
            issues.append("Critical memory usage")
        elif metrics.memory_percent > 80:
            score -= 15
            issues.append("High memory usage")
        
        # Disk usage penalty
        if metrics.disk_percent > 95:
            score -= 30
            issues.append("Critical disk usage")
        elif metrics.disk_percent > 85:
            score -= 15
            issues.append("High disk usage")
        
        # Temperature penalty
        if metrics.temperature and metrics.temperature > 80:
            score -= 20
            issues.append("High CPU temperature")
        
        # Determine status
        if score >= 80:
            status = "Excellent"
        elif score >= 60:
            status = "Good"
        elif score >= 40:
            status = "Fair"
        elif score >= 20:
            status = "Poor"
        else:
            status = "Critical"
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def get_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations based on system issues"""
        recommendations = []
        
        for issue in issues:
            if "CPU" in issue:
                recommendations.append("Consider closing unnecessary applications or upgrading CPU")
            if "memory" in issue:
                recommendations.append("Close unused applications or consider adding more RAM")
            if "disk" in issue:
                recommendations.append("Free up disk space by deleting unnecessary files")
            if "temperature" in issue:
                recommendations.append("Check cooling system and clean dust from fans")
        
        return recommendations

def demo():
    """Demonstrate the System Monitor capabilities"""
    monitor = SystemMonitor()
    
    print("🖥️  SYSTEM MONITOR DEMO 🖥️")
    print("=" * 50)
    
    # System Information
    print("\n📋 SYSTEM INFORMATION:")
    sys_info = monitor.get_system_info()
    if sys_info:
        print(f"Hostname: {sys_info.hostname}")
        print(f"OS: {sys_info.os_name} {sys_info.os_version}")
        print(f"Architecture: {sys_info.architecture}")
        print(f"Processor: {sys_info.processor}")
        print(f"Uptime: {sys_info.uptime}")
    
    # Performance Metrics
    print("\n⚡ PERFORMANCE METRICS:")
    metrics = monitor.get_performance_metrics()
    if metrics:
        print(f"CPU Usage: {metrics.cpu_percent:.1f}%")
        print(f"Memory Usage: {metrics.memory_percent:.1f}%")
        print(f"Disk Usage: {metrics.disk_percent:.1f}%")
        if metrics.temperature:
            print(f"CPU Temperature: {metrics.temperature:.1f}°C")
    
    # Memory Information
    print("\n💾 MEMORY INFORMATION:")
    memory = monitor.get_memory_info()
    print(f"Total: {monitor.format_bytes(memory['total'])}")
    print(f"Used: {monitor.format_bytes(memory['used'])} ({memory['percent']:.1f}%)")
    print(f"Available: {monitor.format_bytes(memory['available'])}")
    
    # Top Processes
    print("\n🔄 TOP PROCESSES:")
    processes = monitor.get_process_info(5)
    for proc in processes:
        print(f"{proc['name']:<20} CPU: {proc.get('cpu_percent', 0):.1f}%")
    
    # System Health
    print("\n🏥 SYSTEM HEALTH:")
    health = monitor.get_system_health_score()
    print(f"Health Score: {health['score']}/100 ({health['status']})")
    if health['issues']:
        print("Issues:")
        for issue in health['issues']:
            print(f"  • {issue}")
    
    # Disk Warnings
    print("\n💿 DISK SPACE CHECK:")
    warnings = monitor.check_disk_space(80)
    if warnings:
        for warning in warnings:
            print(f"⚠️  {warning['device']}: {warning['usage_percent']:.1f}% used")
    else:
        print("✅ All disks have adequate free space")

def interactive_mode():
    """Interactive mode for system monitoring"""
    monitor = SystemMonitor()
    
    print("\n🖥️  INTERACTIVE SYSTEM MONITOR 🖥️")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Show System Information")
        print("2. Show Performance Metrics")
        print("3. Show Memory Information")
        print("4. Show Disk Information")
        print("5. Show Top Processes")
        print("6. Monitor System (Real-time)")
        print("7. Generate System Report")
        print("8. Export Data (JSON)")
        print("9. Check System Health")
        print("10. Cleanup Temp Files")
        print("11. Check Disk Space")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-11): ").strip()
        
        if choice == "0":
            print("Thanks for using System Monitor! 🖥️")
            break
        elif choice == "1":
            sys_info = monitor.get_system_info()
            if sys_info:
                print(f"\n📋 SYSTEM INFORMATION:")
                print(f"Hostname: {sys_info.hostname}")
                print(f"OS: {sys_info.os_name} {sys_info.os_version}")
                print(f"Architecture: {sys_info.architecture}")
                print(f"Processor: {sys_info.processor}")
                print(f"Python Version: {sys_info.python_version}")
                print(f"Uptime: {sys_info.uptime}")
                print(f"Boot Time: {sys_info.boot_time}")
        elif choice == "2":
            metrics = monitor.get_performance_metrics()
            if metrics:
                print(f"\n⚡ PERFORMANCE METRICS:")
                print(f"CPU Usage: {metrics.cpu_percent:.1f}%")
                print(f"Memory Usage: {metrics.memory_percent:.1f}%")
                print(f"Disk Usage: {metrics.disk_percent:.1f}%")
                if metrics.temperature:
                    print(f"CPU Temperature: {metrics.temperature:.1f}°C")
                if metrics.fan_speed:
                    print(f"Fan Speed: {metrics.fan_speed} RPM")
        elif choice == "3":
            memory = monitor.get_memory_info()
            print(f"\n💾 MEMORY INFORMATION:")
            print(f"Total: {monitor.format_bytes(memory['total'])}")
            print(f"Used: {monitor.format_bytes(memory['used'])} ({memory['percent']:.1f}%)")
            print(f"Available: {monitor.format_bytes(memory['available'])}")
            print(f"Free: {monitor.format_bytes(memory['free'])}")
            print(f"Swap Total: {monitor.format_bytes(memory['swap_total'])}")
            print(f"Swap Used: {monitor.format_bytes(memory['swap_used'])} ({memory['swap_percent']:.1f}%)")
        elif choice == "4":
            disks = monitor.get_disk_info()
            print(f"\n💿 DISK INFORMATION:")
            for disk in disks:
                print(f"Device: {disk['device']}")
                print(f"Mountpoint: {disk['mountpoint']}")
                print(f"Filesystem: {disk['fstype']}")
                print(f"Total: {monitor.format_bytes(disk['total'])}")
                print(f"Used: {monitor.format_bytes(disk['used'])} ({disk['percent']:.1f}%)")
                print(f"Free: {monitor.format_bytes(disk['free'])}")
                print("-" * 30)
        elif choice == "5":
            limit = int(input("Number of processes to show (default 10): ") or "10")
            processes = monitor.get_process_info(limit)
            print(f"\n🔄 TOP {limit} PROCESSES:")
            for proc in processes:
                print(f"{proc['name']:<25} PID: {proc['pid']:<8} CPU: {proc.get('cpu_percent', 0):.1f}% Memory: {proc.get('memory_percent', 0):.1f}%")
        elif choice == "6":
            duration = int(input("Monitoring duration in seconds (default 60): ") or "60")
            interval = int(input("Update interval in seconds (default 5): ") or "5")
            data = monitor.monitor_system(duration, interval)
            print(f"\n📊 MONITORING COMPLETE - Collected {len(data)} data points")
        elif choice == "7":
            filename = monitor.save_report()
            print(f"\n📄 System report saved to: {filename}")
        elif choice == "8":
            filename = monitor.export_json()
            print(f"\n📊 System data exported to: {filename}")
        elif choice == "9":
            health = monitor.get_system_health_score()
            print(f"\n🏥 SYSTEM HEALTH:")
            print(f"Health Score: {health['score']}/100 ({health['status']})")
            if health['issues']:
                print("\nIssues:")
                for issue in health['issues']:
                    print(f"  • {issue}")
            if health['recommendations']:
                print("\nRecommendations:")
                for rec in health['recommendations']:
                    print(f"  • {rec}")
        elif choice == "10":
            days = int(input("Delete temp files older than (days, default 7): ") or "7")
            cleaned = monitor.cleanup_temp_files(days)
            print(f"\n🧹 Cleaned up {cleaned} temporary files")
        elif choice == "11":
            threshold = float(input("Disk usage threshold % (default 90): ") or "90")
            warnings = monitor.check_disk_space(threshold)
            if warnings:
                print(f"\n⚠️  DISK SPACE WARNINGS (>{threshold}% used):")
                for warning in warnings:
                    print(f"Device: {warning['device']}")
                    print(f"Mountpoint: {warning['mountpoint']}")
                    print(f"Usage: {warning['usage_percent']:.1f}%")
                    print(f"Free Space: {warning['free_space']}")
                    print("-" * 30)
            else:
                print(f"\n✅ All disks are below {threshold}% usage")
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    demo()
    print("\n" + "="*50)
    interactive_mode()
