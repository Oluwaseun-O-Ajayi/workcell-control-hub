# Integrated Workcell Control Hub

A PyQt5-based control interface demonstrating multi-instrument orchestration for automated laboratory workcells. Built to showcase system integration capabilities for biopharmaceutical R&D automation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Purpose

This project demonstrates:
- **GUI Development** with PyQt5 for laboratory automation
- **Multi-instrument coordination** and orchestration
- **System integration** concepts for decentralized workcell networks
- **Real-time monitoring** and control interface design
- **Professional software architecture** for industrial automation

**Target Application:** Cell line development, high-throughput screening, and biotherapeutic production workflows

---

## ✨ Key Features

### 📊 Device Monitoring
- Real-time status display for multiple instruments
- Color-coded status indicators (Ready, Active, Stopped)
- Progress tracking for active operations
- Individual device testing capabilities

### 🔄 Protocol Management
- Pre-configured automation workflows
- Sample batch processing (1-96 samples)
- Step-by-step execution with progress tracking
- Pause/resume and emergency stop controls

### 📝 Sample Tracking
- Live sample inventory table
- Location and status tracking
- Timestamp logging for audit trails
- Integration-ready for LIMS systems

### 🔗 System Integration
- Links to related automation projects
- Demonstrates workcell orchestration architecture
- Modular design for easy expansion
- Thread-safe multi-device coordination

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8 or higher
```

### Installation
```bash
# Clone the repository
git clone https://github.com/Oluwaseun-O-Ajayi/workcell-control-hub.git
cd workcell-control-hub

# Install dependencies
pip install -r requirements.txt

# Run the application
python workcell_control_hub.py
```

---

## 🏗️ Architecture

This control hub serves as a **centralized interface** that orchestrates multiple independent automation modules:

```
┌─────────────────────────────────────────┐
│   Workcell Control Hub (PyQt5 GUI)     │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┬──────────────┬──────────────┐
    │           │           │              │              │
┌───▼───┐  ┌───▼───┐  ┌───▼────┐   ┌─────▼────┐  ┌─────▼─────┐
│ Robot │  │Liquid │  │ Plate  │   │Incubator │  │  Storage  │
│Workcell│  │Handler│  │ Reader │   │          │  │   Unit    │
└───────┘  └───────┘  └────────┘   └──────────┘  └───────────┘
```

### Related Projects

This hub integrates concepts from multiple automation repositories:

| Project | Description | Link |
|---------|-------------|------|
| **Robot Workcell Simulator** | 6-axis robot arm control & kinematics | [View Repo](https://github.com/Oluwaseun-O-Ajayi/robot-workcell-simulator) |
| **Cell Line Screening** | CHO cell screening workflows | [View Repo](https://github.com/Oluwaseun-O-Ajayi/cell-line-screening-simulator) |
| **Lab Automation API** | Plate reader API & device communication | [View Repo](https://github.com/Oluwaseun-O-Ajayi/lab-automation-api) |
| **Protocol Manager** | Digital lab notebook & protocol templates | [View Repo](https://github.com/Oluwaseun-O-Ajayi/protocol-manager-lab-notebook) |
| **Sample Tracking Database** | LIMS concepts with audit trails | [View Repo](https://github.com/Oluwaseun-O-Ajayi/sample-tracking-database) |
| **LC-MS Data Processor** | Chromatogram analysis toolkit | [View Repo](https://github.com/Oluwaseun-O-Ajayi/lcms-data-processor) |

---

## 💡 Technical Highlights

### PyQt5 Implementation
- **Multi-threaded operations** using `QThread` for non-blocking device control
- **Signal/slot mechanism** for event-driven communication
- **Tab-based interface** for organized workflow management
- **Custom styling** for professional appearance

### Design Patterns
- **Object-oriented architecture** with modular components
- **Thread-safe operations** for concurrent device management
- **Event-driven programming** for responsive UI
- **Separation of concerns** (GUI, logic, simulation)

### Code Quality
- Clean, documented Python code
- Type hints and docstrings
- Follows PEP 8 style guidelines
- Modular and extensible design

---

## 📖 Use Cases

### Biopharmaceutical R&D
- Cell line development workflows
- Clone screening automation
- Bioreactor sample handling
- Quality control testing

### High-Throughput Screening
- Plate-based assay automation
- Multi-instrument coordination
- Sample preparation workflows
- Data collection integration

### Lab Automation Engineering
- Workcell system design
- GUI prototyping
- Device integration testing
- Protocol development

---

## 🔧 Customization

The modular design allows easy customization:

### Adding New Devices
```python
# In __init__ method, add to devices dictionary:
self.devices['New Device'] = {'status': 'Ready', 'progress': 0}
```

### Creating Custom Protocols
```python
# Add to protocol_combo items:
self.protocol_combo.addItems([
    "Your Custom Protocol Name"
])
```

### Integrating Real APIs
Replace simulation threads with actual device API calls:
```python
# Instead of DeviceSimulationThread, use real device SDK:
from hamilton_api import LiquidHandler
handler = LiquidHandler(port='COM3')
handler.aspirate(volume=100, well='A1')
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Professional GUI development with PyQt5
- ✅ Multi-threaded programming in Python
- ✅ Event-driven architecture design
- ✅ Laboratory automation concepts
- ✅ System integration principles
- ✅ Software engineering best practices

---

## 🛠️ Development Roadmap

### Future Enhancements
- [ ] Integration with actual device APIs (Hamilton, Tecan, etc.)
- [ ] Database backend for persistent sample tracking
- [ ] Network communication between multiple workcells
- [ ] Advanced scheduling and queue management
- [ ] Data visualization and analytics dashboard
- [ ] Configuration file support for different setups
- [ ] User authentication and access control

---

## 🤝 Related Work

This project is part of a broader portfolio of laboratory automation tools:

- **Autonomous Drug Discovery Lab** - Self-driving laboratory framework
- **Drugability Toolkit** - ADMET prediction and lead optimization
- **Assay Design Calculator** - HTS workflow optimization
- **Enzymatic Kinetics Analyzer** - Michaelis-Menten analysis
- **PubMed Research Assistant** - Literature mining automation

[View All Projects](https://github.com/Oluwaseun-O-Ajayi)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👤 Author

**Oluwaseun Ajayi**
- GitHub: [@Oluwaseun-O-Ajayi](https://github.com/Oluwaseun-O-Ajayi)
- Portfolio: Lab automation and computational chemistry tools

---

## 🙏 Acknowledgments

Built as a demonstration of system integration concepts for:
- Multi-instrument laboratory automation
- Decentralized workcell networks
- Biopharmaceutical R&D workflows
- Cell line development automation

---

## 📞 Contact

For questions, collaboration opportunities, or feedback:
- Open an issue on GitHub
- Connect via [GitHub profile](https://github.com/Oluwaseun-O-Ajayi)

---

**Note:** This is a demonstration project showcasing GUI development and system integration concepts for laboratory automation. It simulates device operations for portfolio purposes. In production environments, this would integrate with actual instrument APIs and control systems.
