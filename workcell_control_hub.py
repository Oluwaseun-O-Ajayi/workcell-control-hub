"""
Integrated Workcell Control Hub
================================
Multi-instrument orchestration system for automated laboratory workcells.
Demonstrates PyQt5 GUI development and system integration for biopharmaceutical R&D.

Author: Oluwaseun Ajayi
GitHub: https://github.com/Oluwaseun-O-Ajayi
Purpose: Portfolio demonstration for lab automation engineering position

This GUI integrates concepts from multiple automation projects:
- Robot workcell control
- Cell line screening workflows
- Protocol management
- Real-time device monitoring
- Multi-instrument coordination
"""

import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QGroupBox, QGridLayout, QComboBox,
    QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QStatusBar, QCheckBox, QSpinBox
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor
import random


class DeviceSimulationThread(QThread):
    """Background thread for simulating device operations"""
    status_update = pyqtSignal(str, str, int)  # device_name, status, progress
    log_message = pyqtSignal(str, str)  # message, level
    
    def __init__(self, device_name, operation):
        super().__init__()
        self.device_name = device_name
        self.operation = operation
        self.is_running = True
        
    def run(self):
        """Simulate device operation with progress updates"""
        steps = 10
        for i in range(steps + 1):
            if not self.is_running:
                self.status_update.emit(self.device_name, "Stopped", 0)
                return
                
            progress = int((i / steps) * 100)
            self.status_update.emit(self.device_name, "Active", progress)
            
            if i == steps // 2:
                self.log_message.emit(
                    f"{self.device_name}: {self.operation} 50% complete",
                    "INFO"
                )
            
            self.msleep(500)  # 0.5 second per step
        
        self.status_update.emit(self.device_name, "Ready", 100)
        self.log_message.emit(
            f"{self.device_name}: {self.operation} completed successfully",
            "SUCCESS"
        )
    
    def stop(self):
        self.is_running = False


class WorkcellControlHub(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Device states
        self.devices = {
            'Transport Robot': {'status': 'Idle', 'progress': 0},
            'Liquid Handler': {'status': 'Ready', 'progress': 0},
            'Plate Reader': {'status': 'Ready', 'progress': 0},
            'Centrifuge': {'status': 'Ready', 'progress': 0},
            'Incubator': {'status': 'Maintaining 37°C', 'progress': 0},
            'Storage Unit': {'status': 'Ready', 'progress': 0}
        }
        
        # Active device threads
        self.device_threads = {}
        
        # Protocol execution state
        self.protocol_running = False
        self.current_step = 0
        
        # Sample tracking
        self.samples = []
        
        self.init_ui()
        
        # Status bar updates
        self.statusBar().showMessage('System Ready')
        
        # Periodic updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_update)
        self.timer.start(5000)  # Every 5 seconds
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Integrated Workcell Control Hub - Lab Automation')
        self.setGeometry(100, 50, 1200, 800)
        
        # Central widget with tab interface
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for different sections
        self.tabs = QTabWidget()
        
        # Tab 1: Device Monitoring
        self.tabs.addTab(self.create_device_monitor_tab(), "Device Monitor")
        
        # Tab 2: Protocol Execution
        self.tabs.addTab(self.create_protocol_tab(), "Protocol Manager")
        
        # Tab 3: Sample Tracking
        self.tabs.addTab(self.create_sample_tracking_tab(), "Sample Tracking")
        
        # Tab 4: System Integration
        self.tabs.addTab(self.create_integration_tab(), "System Integration")
        
        main_layout.addWidget(self.tabs)
        
        # Activity log at bottom (visible across all tabs)
        log_group = self.create_log_section()
        main_layout.addWidget(log_group)
        
        # Status bar
        self.setStatusBar(QStatusBar())
        
        self.log_message("Workcell Control Hub initialized", "SUCCESS")
        self.log_message("All devices connected and ready", "INFO")
        
    def create_header(self):
        """Create header section"""
        header_widget = QWidget()
        layout = QVBoxLayout(header_widget)
        
        title = QLabel('Integrated Workcell Control Hub')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Multi-Instrument Orchestration for Automated Laboratory Workflows')
        subtitle.setFont(QFont('Arial', 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #555;")
        layout.addWidget(subtitle)
        
        # GitHub link
        github_label = QLabel(
            '<a href="https://github.com/Oluwaseun-O-Ajayi">View Related Projects on GitHub</a>'
        )
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setStyleSheet("margin: 5px;")
        layout.addWidget(github_label)
        
        return header_widget
        
    def create_device_monitor_tab(self):
        """Create device monitoring tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Device status grid
        device_group = QGroupBox("Device Status Monitor")
        device_layout = QGridLayout()
        
        self.status_labels = {}
        self.progress_bars = {}
        
        row = 0
        for device_name in self.devices.keys():
            # Device name
            name_label = QLabel(device_name + ":")
            name_label.setFont(QFont('Arial', 11, QFont.Bold))
            device_layout.addWidget(name_label, row, 0)
            
            # Status label
            status_label = QLabel(self.devices[device_name]['status'])
            status_label.setStyleSheet(
                "background-color: #90EE90; padding: 8px; "
                "border-radius: 4px; min-width: 150px;"
            )
            device_layout.addWidget(status_label, row, 1)
            self.status_labels[device_name] = status_label
            
            # Progress bar
            progress = QProgressBar()
            progress.setVisible(False)
            device_layout.addWidget(progress, row, 2)
            self.progress_bars[device_name] = progress
            
            # Manual control button
            control_btn = QPushButton('Test Device')
            control_btn.clicked.connect(
                lambda checked, d=device_name: self.test_device(d)
            )
            device_layout.addWidget(control_btn, row, 3)
            
            row += 1
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Quick stats
        stats_group = QGroupBox("System Statistics")
        stats_layout = QGridLayout()
        
        stats_layout.addWidget(QLabel("Total Devices:"), 0, 0)
        stats_layout.addWidget(QLabel(str(len(self.devices))), 0, 1)
        
        stats_layout.addWidget(QLabel("Active Operations:"), 1, 0)
        self.active_ops_label = QLabel("0")
        stats_layout.addWidget(self.active_ops_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Uptime:"), 2, 0)
        self.uptime_label = QLabel("0:00:00")
        stats_layout.addWidget(self.uptime_label, 2, 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
        return tab
        
    def create_protocol_tab(self):
        """Create protocol execution tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Protocol selection
        protocol_group = QGroupBox("Protocol Configuration")
        protocol_layout = QVBoxLayout()
        
        # Protocol dropdown
        proto_select_layout = QHBoxLayout()
        proto_select_layout.addWidget(QLabel("Select Protocol:"))
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems([
            "Cell Culture - Automated Passage",
            "High-Throughput Clone Screening",
            "Sample Prep for LC-MS Analysis",
            "Plate-Based Assay Workflow",
            "Bioreactor Sample Collection",
            "Inter-Lab Sample Transfer"
        ])
        proto_select_layout.addWidget(self.protocol_combo)
        proto_select_layout.addStretch()
        protocol_layout.addLayout(proto_select_layout)
        
        # Sample count
        sample_layout = QHBoxLayout()
        sample_layout.addWidget(QLabel("Number of Samples:"))
        self.sample_count = QSpinBox()
        self.sample_count.setMinimum(1)
        self.sample_count.setMaximum(96)
        self.sample_count.setValue(24)
        sample_layout.addWidget(self.sample_count)
        sample_layout.addStretch()
        protocol_layout.addLayout(sample_layout)
        
        protocol_group.setLayout(protocol_layout)
        layout.addWidget(protocol_group)
        
        # Protocol execution controls
        control_group = QGroupBox("Execution Controls")
        control_layout = QHBoxLayout()
        
        self.start_protocol_btn = QPushButton('Start Protocol')
        self.start_protocol_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; "
            "padding: 12px; font-weight: bold; font-size: 12pt;"
        )
        self.start_protocol_btn.clicked.connect(self.start_protocol)
        control_layout.addWidget(self.start_protocol_btn)
        
        self.pause_protocol_btn = QPushButton('Pause')
        self.pause_protocol_btn.setStyleSheet(
            "background-color: #FFA500; color: white; padding: 12px;"
        )
        self.pause_protocol_btn.setEnabled(False)
        self.pause_protocol_btn.clicked.connect(self.pause_protocol)
        control_layout.addWidget(self.pause_protocol_btn)
        
        self.stop_protocol_btn = QPushButton('Emergency Stop')
        self.stop_protocol_btn.setStyleSheet(
            "background-color: #f44336; color: white; "
            "padding: 12px; font-weight: bold;"
        )
        self.stop_protocol_btn.clicked.connect(self.emergency_stop)
        control_layout.addWidget(self.stop_protocol_btn)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Protocol progress
        progress_group = QGroupBox("Protocol Progress")
        progress_layout = QVBoxLayout()
        
        self.protocol_progress = QProgressBar()
        self.protocol_progress.setTextVisible(True)
        progress_layout.addWidget(self.protocol_progress)
        
        self.current_step_label = QLabel("Ready to start protocol")
        self.current_step_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.current_step_label)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        layout.addStretch()
        return tab
        
    def create_sample_tracking_tab(self):
        """Create sample tracking tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Sample table
        table_group = QGroupBox("Active Samples")
        table_layout = QVBoxLayout()
        
        self.sample_table = QTableWidget()
        self.sample_table.setColumnCount(5)
        self.sample_table.setHorizontalHeaderLabels([
            'Sample ID', 'Type', 'Location', 'Status', 'Last Updated'
        ])
        self.sample_table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.sample_table)
        
        # Add sample button
        add_sample_btn = QPushButton('Add Test Sample')
        add_sample_btn.clicked.connect(self.add_test_sample)
        table_layout.addWidget(add_sample_btn)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        return tab
        
    def create_integration_tab(self):
        """Create system integration info tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_group = QGroupBox("Related Automation Projects")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "<b>This control hub demonstrates integration with multiple automation systems:</b><br><br>"
            
            "🤖 <b>Robot Workcell Simulator</b><br>"
            "└─ 6-axis robot arm control for sample transport and manipulation<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/robot-workcell-simulator'>"
            "github.com/Oluwaseun-O-Ajayi/robot-workcell-simulator</a><br><br>"
            
            "🧬 <b>Cell Line Screening Simulator</b><br>"
            "└─ CHO cell screening workflows for biotherapeutic development<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/cell-line-screening-simulator'>"
            "github.com/Oluwaseun-O-Ajayi/cell-line-screening-simulator</a><br><br>"
            
            "🔬 <b>Lab Automation API</b><br>"
            "└─ Mock plate reader API with multi-wavelength support<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/lab-automation-api'>"
            "github.com/Oluwaseun-O-Ajayi/lab-automation-api</a><br><br>"
            
            "📋 <b>Protocol Manager & Lab Notebook</b><br>"
            "└─ Digital lab notebook with protocol templates and sample tracking<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook'>"
            "github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook</a><br><br>"
            
            "💾 <b>Sample Tracking Database</b><br>"
            "└─ SQLite-based LIMS demonstrating GMP compliance concepts<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/sample-tracking-database'>"
            "github.com/Oluwaseun-O-Ajayi/sample-tracking-database</a><br><br>"
            
            "🧪 <b>LC-MS Data Processor</b><br>"
            "└─ Chromatogram analysis and quantification toolkit<br>"
            "└─ <a href='https://github.com/Oluwaseun-O-Ajayi/lcms-data-processor'>"
            "github.com/Oluwaseun-O-Ajayi/lcms-data-processor</a><br><br>"
            
            "<b>Integration Approach:</b><br>"
            "This GUI serves as a centralized control hub that would orchestrate "
            "these independent modules in a real workcell system. Each backend module "
            "represents a different instrument or subsystem that communicates via APIs, "
            "demonstrating the decentralized workcell architecture described in the "
            "CEAS automation roadmap."
        )
        info_text.setWordWrap(True)
        info_text.setOpenExternalLinks(True)
        info_text.setTextFormat(Qt.RichText)
        
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        return tab
        
    def create_log_section(self):
        """Create activity log section"""
        group = QGroupBox("Activity Log")
        layout = QVBoxLayout()
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        layout.addWidget(self.log_display)
        
        # Log controls
        btn_layout = QHBoxLayout()
        clear_log_btn = QPushButton('Clear Log')
        clear_log_btn.clicked.connect(lambda: self.log_display.clear())
        btn_layout.addWidget(clear_log_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
        
    def log_message(self, message, level="INFO"):
        """Add timestamped message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        color_map = {
            "INFO": "black",
            "WARNING": "orange",
            "ERROR": "red",
            "SUCCESS": "green",
            "DEVICE": "blue"
        }
        
        color = color_map.get(level, "black")
        formatted_msg = f'<span style="color: {color};">[{timestamp}] {level}: {message}</span>'
        
        self.log_display.append(formatted_msg)
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )
        
    def test_device(self, device_name):
        """Test individual device"""
        if device_name in self.device_threads and self.device_threads[device_name].isRunning():
            self.log_message(f"{device_name} is already active", "WARNING")
            return
            
        operations = {
            'Transport Robot': 'Moving to position A3',
            'Liquid Handler': 'Aspirating samples',
            'Plate Reader': 'Reading absorbance at 450nm',
            'Centrifuge': 'Spinning at 2000 RPM',
            'Incubator': 'Temperature verification',
            'Storage Unit': 'Retrieving plate from position B2'
        }
        
        operation = operations.get(device_name, 'Running test')
        self.log_message(f"Starting {device_name}: {operation}", "DEVICE")
        
        # Create and start thread
        thread = DeviceSimulationThread(device_name, operation)
        thread.status_update.connect(self.update_device_status)
        thread.log_message.connect(self.log_message)
        thread.finished.connect(lambda: self.cleanup_thread(device_name))
        
        self.device_threads[device_name] = thread
        thread.start()
        
    def update_device_status(self, device_name, status, progress):
        """Update device status display"""
        if device_name not in self.devices:
            return
            
        self.devices[device_name]['status'] = status
        self.devices[device_name]['progress'] = progress
        
        # Update label
        label = self.status_labels[device_name]
        label.setText(status)
        
        # Color coding
        if status in ['Ready', 'Idle']:
            label.setStyleSheet(
                "background-color: #90EE90; padding: 8px; "
                "border-radius: 4px; min-width: 150px;"
            )
        elif status == 'Active':
            label.setStyleSheet(
                "background-color: #87CEEB; padding: 8px; "
                "border-radius: 4px; min-width: 150px;"
            )
        elif status == 'Stopped':
            label.setStyleSheet(
                "background-color: #FFB6C6; padding: 8px; "
                "border-radius: 4px; min-width: 150px;"
            )
        else:
            label.setStyleSheet(
                "background-color: #FFFFE0; padding: 8px; "
                "border-radius: 4px; min-width: 150px;"
            )
        
        # Update progress bar
        progress_bar = self.progress_bars[device_name]
        if status == 'Active':
            progress_bar.setVisible(True)
            progress_bar.setValue(progress)
        else:
            progress_bar.setVisible(False)
            
    def cleanup_thread(self, device_name):
        """Clean up finished thread"""
        if device_name in self.device_threads:
            del self.device_threads[device_name]
        self.update_active_operations_count()
        
    def start_protocol(self):
        """Start protocol execution"""
        protocol = self.protocol_combo.currentText()
        num_samples = self.sample_count.value()
        
        self.log_message(f"Starting protocol: {protocol}", "SUCCESS")
        self.log_message(f"Processing {num_samples} samples", "INFO")
        
        self.protocol_running = True
        self.start_protocol_btn.setEnabled(False)
        self.pause_protocol_btn.setEnabled(True)
        
        self.current_step = 0
        self.protocol_progress.setValue(0)
        
        # Simulate protocol steps
        self.execute_protocol_step()
        
    def execute_protocol_step(self):
        """Execute next protocol step"""
        if not self.protocol_running:
            return
            
        steps = [
            ('Transport Robot', 'Retrieving samples from storage'),
            ('Liquid Handler', 'Dispensing reagents'),
            ('Incubator', 'Incubating samples'),
            ('Centrifuge', 'Centrifuging samples'),
            ('Plate Reader', 'Reading plate'),
            ('Transport Robot', 'Returning samples to storage')
        ]
        
        if self.current_step < len(steps):
            device, operation = steps[self.current_step]
            self.current_step_label.setText(f"Step {self.current_step + 1}/{len(steps)}: {operation}")
            
            progress = int((self.current_step / len(steps)) * 100)
            self.protocol_progress.setValue(progress)
            
            # Start device operation
            if device not in self.device_threads or not self.device_threads[device].isRunning():
                thread = DeviceSimulationThread(device, operation)
                thread.status_update.connect(self.update_device_status)
                thread.log_message.connect(self.log_message)
                thread.finished.connect(lambda: self.protocol_step_complete())
                
                self.device_threads[device] = thread
                thread.start()
            
            self.current_step += 1
        else:
            self.protocol_complete()
            
    def protocol_step_complete(self):
        """Handle completion of protocol step"""
        if self.protocol_running and self.current_step < 6:
            QTimer.singleShot(1000, self.execute_protocol_step)
            
    def protocol_complete(self):
        """Handle protocol completion"""
        self.protocol_running = False
        self.protocol_progress.setValue(100)
        self.current_step_label.setText("Protocol completed successfully!")
        self.log_message("Protocol execution completed", "SUCCESS")
        
        self.start_protocol_btn.setEnabled(True)
        self.pause_protocol_btn.setEnabled(False)
        
        # Add samples to tracking table
        num_samples = self.sample_count.value()
        for i in range(num_samples):
            self.add_test_sample()
        
    def pause_protocol(self):
        """Pause protocol execution"""
        self.protocol_running = False
        self.log_message("Protocol paused by user", "WARNING")
        self.start_protocol_btn.setEnabled(True)
        self.pause_protocol_btn.setEnabled(False)
        
    def emergency_stop(self):
        """Emergency stop all operations"""
        reply = QMessageBox.question(
            self,
            'Emergency Stop',
            'Are you sure you want to stop all operations?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.log_message("EMERGENCY STOP ACTIVATED", "ERROR")
            self.protocol_running = False
            
            # Stop all device threads
            for device_name, thread in self.device_threads.items():
                thread.stop()
                
            # Update all device statuses
            for device in self.devices:
                self.devices[device]['status'] = 'Stopped'
                self.update_device_status(device, 'Stopped', 0)
                
            self.start_protocol_btn.setEnabled(True)
            self.pause_protocol_btn.setEnabled(False)
            
            self.statusBar().showMessage('EMERGENCY STOP - All operations halted', 5000)
            
    def add_test_sample(self):
        """Add a test sample to tracking table"""
        sample_id = f"S{len(self.samples) + 1:04d}"
        sample_types = ['CHO Clone', 'Media Sample', 'Assay Plate', 'QC Sample']
        locations = ['Incubator A', 'Storage -80C', 'Workcell 1', 'Reader Station']
        
        sample_data = {
            'id': sample_id,
            'type': random.choice(sample_types),
            'location': random.choice(locations),
            'status': 'Active',
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        self.samples.append(sample_data)
        
        # Add to table
        row = self.sample_table.rowCount()
        self.sample_table.insertRow(row)
        
        self.sample_table.setItem(row, 0, QTableWidgetItem(sample_data['id']))
        self.sample_table.setItem(row, 1, QTableWidgetItem(sample_data['type']))
        self.sample_table.setItem(row, 2, QTableWidgetItem(sample_data['location']))
        self.sample_table.setItem(row, 3, QTableWidgetItem(sample_data['status']))
        self.sample_table.setItem(row, 4, QTableWidgetItem(sample_data['timestamp']))
        
    def periodic_update(self):
        """Periodic system updates"""
        self.update_active_operations_count()
        
    def update_active_operations_count(self):
        """Update count of active operations"""
        active = sum(1 for t in self.device_threads.values() if t.isRunning())
        self.active_ops_label.setText(str(active))


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the control hub
    hub = WorkcellControlHub()
    hub.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
