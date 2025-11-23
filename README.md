# DockerView

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple terminal-based Docker performance monitor that displays real-time container statistics in a beautiful table format.

## Features
- Real-time monitoring of Docker containers
- Displays container ID, name, status, CPU usage, and memory usage
- Auto-refreshing display (1 second interval)
- Clean terminal UI using Rich library
- Simple keyboard control (Ctrl+C to exit)

## Installation
```bash
pip install dockerview
```

## Usage
```bash
dockerview
```

Example output:
```
DockerView Monitor (Press Ctrl+C to exit)
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ ID         ┃ Name             ┃ Status   ┃ CPU %  ┃ Memory Usage ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ a1b2c3d4e5 │ web-server       │ running  │ 2.5%   │ 120MB/2GB    │
│ f6g7h8i9j0 │ database         │ running  │ 15.2%  │ 890MB/4GB    │
│ k1l2m3n4o5 │ redis-cache      │ running  │ 0.8%   │ 45MB/1GB     │
└────────────┴──────────────────┴──────────┴────────┴──────────────┘
```

## Requirements
- Docker Engine
- Python 3.8+
- Rich library (>=13.0.0)
- Docker SDK for Python (>=6.0.0)

## Project Structure
```
dockerview/
├── cli.py          # Command line interface
├── monitor.py      # Docker monitoring logic
├── __init__.py     # Package initialization
├── CHANGELOG.md    # Project change history
└── ...
```

## Changelog
For details of each release, see the [CHANGELOG](CHANGELOG.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.