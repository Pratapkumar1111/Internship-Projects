# Internship-Projects
# PCAP File Slicer

## Overview
The **PCAP File Slicer** is a user-friendly web-based tool designed to slice and analyze PCAP files. It allows users to upload and segment large PCAP files, providing insights into network traffic. The project is built with **Flask (Python backend)** for handling the PCAP files and uses **HTML, CSS**, and **JavaScript** for the frontend to ensure a seamless and intuitive UI/UX experience.

## Features
- **Upload PCAP Files**: Users can upload PCAP files for slicing and analysis.
- **Segment PCAP Files**: The tool allows users to slice the files based on time or packet count.
- **Visualize Network Traffic**: Graphical representations of network traffic over time.
- **Download Segments**: Users can download the sliced PCAP segments for further analysis.
- **Responsive Design**: The interface is optimized for both desktop and mobile users.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Libraries**:
  - **scapy** for PCAP file handling
  - **Flask** for backend and API
  - **Bootstrap** for responsive design
  - **Plotly.js** for visualizing traffic

## Installation

### Prerequisites
- **Python 3.x** installed on your system
- **Flask** and **scapy** Python libraries
- **Git** (optional)

### Clone the Repository
```bash
git clone https://github.com/yourusername/pcap-file-slicer.git
cd pcap-file-slicer
