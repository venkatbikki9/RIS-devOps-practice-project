# 📘 Project Overview

Build a Bash-based monitoring tool that runs as a systemd service and provides a CLI dashboard for monitoring system metrics, container status, user activity, service logs, and network health. This project simulates real-world monitoring tools used in production environments.


---

## ✅ Prerequisites

### Required Knowledge

- **Linux Command Line**: Comfortable navigating directories, editing files, managing permissions  
- **Basic Bash Scripting**: Understanding variables, functions, conditionals, and loops  
- **Text Editors**: Proficiency with `vim`, `nano`, or VS Code  
- **Process Management**: Understanding of processes, services, and process monitoring  

### System Requirements

- **Operating System**: Ubuntu 20.04+ or Debian 11+ (or similar systemd-based distribution)  
- **User Access**: `sudo` privileges for service installation  
- **Available Resources**: At least 1GB free disk space  

### Recommended Pre-reading

- Bash Scripting Guide  
- Systemd Service Units  
- Linux System Monitoring Basics  

---

## 🎯 Learning Objectives

By completing this project, you will:

- Master Bash scripting for system administration  
- Understand systemd service creation and management  
- Learn system monitoring techniques and tools  
- Practice DevOps automation and deployment  
- Gain experience with log management and rotation  
- Understand CLI tool design principles  

---

## 📂 Project Structure

```
sysmondash/
├── src/
│   ├── sysmondash.sh          # Main CLI monitoring tool
│   ├── sysmondash.service     # systemd service unit file
│   └── logrotate.conf         # Log rotation configuration
├── scripts/
│   ├── install.sh             # Automated installer script
│   ├── uninstall.sh           # Cleanup script
│   └── test.sh                # Basic functionality tests
├── docs/
│   ├── README.md              # Main documentation
│   ├── INSTALL.md             # Installation guide
│   └── TROUBLESHOOTING.md     # Common issues and solutions
├── examples/
│   ├── sample_outputs.txt     # Expected command outputs
│   └── service_logs.txt       # Sample service logs
└── tests/
    ├── unit_tests.bats        # BATS test files (bonus)
    └── integration_tests.sh   # Integration tests
```

---

## ⚙️ Functional Requirements

### 1. Main CLI Tool (`sysmondash.sh`)

- **Location**: `/usr/local/bin/sysmondash`  
- **Permissions**: `755`  
- **Owner**: `root:root`  

#### Command Line Interface

| Flag         | Function              | Example Usage                      | Expected Behavior                              |
|--------------|-----------------------|------------------------------------|------------------------------------------------|
| `-p [port]`  | Show port status      | `sysmondash -p 80`                 | Display processes listening on port 80         |
| `-d [name]`  | Docker container      | `sysmondash -d nginx`              | Show nginx container details                   |
| `-n [domain]`| Nginx configuration   | `sysmondash -n example.com`        | Show server block for domain                   |
| `-u [user]`  | User activity         | `sysmondash -u john`               | Show login history for user                    |
| `-c`         | System resources      | `sysmondash -c`                    | Display CPU and memory usage                   |
| `-r`         | Disk usage            | `sysmondash -r`                    | Show disk space information                    |
| `-t`         | Logs between times    | `sysmondash -t "2024-01-01" "2024-01-02"` | Show logs between timestamps     |
| `-a`         | All metrics           | `sysmondash -a`                    | Display comprehensive system overview          |
| `-h`         | Help                  | `sysmondash -h`                    | Show usage information                         |

#### Error Handling Requirements

- Validate all input parameters  
- Handle missing dependencies gracefully  
- Provide meaningful error messages  
- Exit with appropriate error codes (0 for success, 1–255 for errors)  

---

### 2. Systemd Service (`sysmondash.service`)

- **Service Type**: Simple (long-running process)  
- **Run Frequency**: Continuous monitoring with configurable intervals  
- **Log Location**: `/var/log/sysmondash/sysmondash.log`  
- **Service User**: `sysmondash` (dedicated system user)  
- **Restart Policy**: Always restart on failure with 30-second delay  

#### Service Behavior

- Runs continuously, collecting metrics every 60 seconds  
- Writes timestamped entries to log file  
- Automatically restarts if process fails  
- Can be controlled with standard `systemctl` commands  

---

### 3. Installation Script (`install.sh`)

- **Requirements**: Must be idempotent (safe to run multiple times)  

#### Installation Steps

1. **Dependency Check**: Verify and install required packages  
2. **User Creation**: Create dedicated `sysmondash` system user  
3. **File Deployment**: Copy scripts to appropriate system locations  
4. **Permission Setup**: Set correct file permissions and ownership  
5. **Log Configuration**: Create log directory and setup rotation  
6. **Service Registration**: Install and enable systemd service  
7. **Validation**: Test that service starts correctly  

#### Dependencies to Install

```bash
apt-get install -y \
    jq \
    curl \
    net-tools \
    docker.io \
    nginx \
    logrotate \
    bash \
    coreutils \
    util-linux \
    procps
```

---

### 4. Log Management

- **Log Directory**: `/var/log/sysmondash/`  
- **Main Log File**: `sysmondash.log`  

#### Rotation Policy

- Rotate daily  
- Keep 7 days of logs  
- Compress rotated logs  
- Maximum log size: 100MB  

---

## 🚀 Getting Started (Manual Setup)

### Step 1: Create the Basic Script

```bash
# Create project directory
mkdir -p ~/sysmondash/src
cd ~/sysmondash/src

# Create main script
cat > sysmondash.sh << 'EOF'
#!/bin/bash
# SysMonDash - System Monitoring Tool
# Version: 1.0

show_help() {
    echo "Usage: sysmondash [OPTIONS]"
    echo "Options:"
    echo "  -c          Show CPU and memory usage"
    echo "  -r          Show disk usage"
    echo "  -h          Show this help message"
}

show_cpu_memory() {
    echo "=== System Resources ==="
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
    echo "Memory Usage: $(free -h | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')"
    echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
}

show_disk_usage() {
    echo "=== Disk Usage ==="
    df -h | grep -vE '^Filesystem|tmpfs|cdrom'
}

# Parse command line arguments
case "$1" in
    -c) show_cpu_memory ;;
    -r) show_disk_usage ;;
    -h) show_help ;;
    *) show_help ;;
esac
EOF

# Make executable
chmod +x sysmondash.sh
```

---

### Step 2: Test Basic Functionality

```bash
./sysmondash.sh -h
./sysmondash.sh -c
./sysmondash.sh -r
```

---

### Step 3: Create Basic Service File

```bash
cat > sysmondash.service << 'EOF'
[Unit]
Description=SysMonDash System Monitoring Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/home/$USER/sysmondash/src/sysmondash.sh -c
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF
```

---

### Step 4: Test Service Installation

```bash
# Copy service file (requires sudo)
sudo cp sysmondash.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable sysmondash
sudo systemctl start sysmondash

# Check status
sudo systemctl status sysmondash
```

---

## 📊 Expected Outputs

### CPU and Memory Usage (`-c` flag)

```
=== System Resources ===
CPU Usage: 15.3%
Memory Usage: 26.4% (2.1GB / 8.0GB)
Load Average: 0.50, 0.45, 0.42
Uptime: 2 days, 14:32
```

### Disk Usage (`-r` flag)

```
=== Disk Usage ===
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G  8.5G   11G  45% /
/dev/sda2       100G   45G   50G  48% /home
```

### Port Status (`-p 80` flag)

```
=== Port 80 Status ===
Status: LISTENING
Process: nginx (PID: 1234)
User: www-data
Command: nginx: master process /usr/sbin/nginx
```

### Service Logs (from systemd)

```
Jan 15 10:30:01 server sysmondash[1234]: [INFO] Starting system monitoring
Jan 15 10:30:01 server sysmondash[1234]: [INFO] CPU: 12.3%, Memory: 24.1%
Jan 15 10:31:01 server sysmondash[1234]: [INFO] CPU: 15.7%, Memory: 24.3%
```
