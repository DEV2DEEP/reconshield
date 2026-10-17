# ReconShield

**ReconShield** is a Python desktop application for network reconnaissance, packet analysis, threat-signature detection, and vulnerability research. It combines a dark-themed Tkinter interface with network scanning utilities, live traffic inspection, alerting, and optional AI-assisted analysis.

> **Project status:** Community / learning project. Validate findings independently before using them for operational decisions.

## Features

### 1. Network Reconnaissance
- Discover hosts using ICMP and TCP fallback techniques.
- Scan selected port ranges or predefined scan profiles.
- Identify common services and inspect available service banners.
- Perform selected UDP probes and collect network identity hints where supported.
- Look up potentially relevant vulnerability references using the NVD and Exploit-DB.

### 2. Packet Analyzer
- Capture and inspect network packets where the operating system and permissions allow it.
- Display packet metadata such as source/destination addresses, ports, protocols, lengths, and TCP flags.
- Inspect supported protocol details, including DNS, HTTP, TLS metadata, and other common traffic.
- Filter packet views by protocol, IP address, and port.
- Track TCP conversations and inspect supported HTTP request/response fields.
- Export packet data for further analysis.

### 3. Alerts and Threat Detection
- Apply built-in detection rules to observed traffic.
- Highlight suspicious patterns such as scan activity, SYN-flood-like behavior, DNS anomalies, ARP-related indicators, and possible command-and-control patterns where supported by the implemented rules.
- Associate selected detections with MITRE ATT&CK techniques.
- Review alert severity and supporting indicators.

### 4. HTTP Security Inspection
- Search observed HTTP fields and payload text for signatures associated with SQL injection, cross-site scripting (XSS), path traversal, command injection, SSRF, file inclusion, and scanner-like user agents.
- Inspect request methods, URIs, headers, cookies, user-agent strings, and available payload previews.
- Treat signature matches as **indicators for investigation**, not proof that an attack succeeded.

### 5. AI Security Analyst (Optional)
- Send selected network context and questions to Anthropic's API for AI-assisted analysis.
- Use prompts for threat summaries, IOC extraction, MITRE ATT&CK mapping, remediation planning, and incident-report drafting.
- Requires an Anthropic API key and network access. API usage may incur charges under the provider's terms.

### 6. Export and Investigation Workflow
- Export supported packet data and reports in formats offered by the application, including JSON, CSV, and text.
- Inspect individual packets and use available filters to support investigation.

## Interface

The application provides four main areas:

- **Network Recon** — target discovery, port scanning, service inspection, and vulnerability-reference lookups.
- **Packet Analyzer** — packet capture, filters, protocol details, and session tracking.
- **Alerts & Threats** — review generated detection alerts.
- **AI Security Analyst** — optional AI-assisted interpretation of selected findings.

## Requirements

- Python 3.10 or newer is recommended.
- Tkinter (usually included with standard Python installations; Linux users may need to install their distribution's Tk package).
- Internet access for live NVD / Exploit-DB lookups and optional AI analysis.
- Administrative/root privileges may be required for some scans and packet-capture operations.

Optional packages used when available:

- `matplotlib` — charts and visualizations.
- `networkx` — network graph functionality.
- `psutil` — system and network-interface information.
- `scapy` — packet capture and protocol support, depending on the platform.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ReconShield.git
cd ReconShield
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL you create on GitHub.

### 2. Create a virtual environment (recommended)

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3. Install optional dependencies

```bash
python -m pip install matplotlib networkx psutil scapy
```

The application includes fallbacks for some optional libraries, but features that depend on an absent package may be unavailable. Packet capture can also require platform-specific setup.

**Windows:** Install [Npcap](https://npcap.com/#download) if required for packet capture, and run the application with appropriate permissions.

**Linux:** Install the Tkinter package for your distribution if it is missing. Packet capture may require suitable capabilities or elevated privileges.

### 4. Run ReconShield

Use the actual Python filename in your downloaded repository. For the uploaded version named `ReconShield_v1(1).py`:

```bash
python "ReconShield_v1(1).py"
```

You may rename the file to `ReconShield.py` for a cleaner command:

```bash
python ReconShield.py
```

## Quick Start

1. Launch ReconShield.
2. Open **Network Recon** and enter an IP address, hostname, or CIDR range you are authorized to assess.
3. Choose an appropriate scan profile and start the scan.
4. Open **Packet Analyzer**, select an available interface, and start capture if your platform supports it.
5. Review packets and alerts; inspect individual packets for more context.
6. Use the export options to save supported results.
7. If you configure the optional AI analyst, avoid sending secrets or sensitive traffic data to an external service.

## Live Vulnerability Lookups: Important Limitations

ReconShield queries external sources such as:

- [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
- [Exploit Database](https://www.exploit-db.com/)

These lookups use service names, port-related keywords, and any available version hints. A result associated with a port or service is **not confirmation that the target is vulnerable**. Validate the product, exact version, configuration, affected conditions, and vendor advisories before assigning a finding.

Severity labels inferred from titles or service/port heuristics may be approximate. Prefer authoritative CVE records and validated CVSS data for risk decisions.

## Safety and Responsible Use

ReconShield is intended for authorized network administration, defensive security, education, and testing in environments where you have explicit permission.

- Only scan systems and networks you own or are explicitly authorized to assess.
- Obtain approval before packet capture; captured traffic may contain personal data, credentials, tokens, or confidential information.
- Use the minimum scan scope and intensity necessary.
- Protect exported reports and packet captures as sensitive data.
- AI-assisted output and signature-based detections can be incomplete or incorrect; verify findings before taking action.
- Do not treat this tool as a replacement for a dedicated vulnerability scanner, packet-analysis suite, or professional security assessment.

## Privacy

Packet captures and exports may include sensitive information. Store them securely and share them only with authorized people. If you use the AI analyst, the context you submit is sent to Anthropic's API and is subject to the provider's terms and privacy practices. Do not submit confidential data unless your organization has approved that use.

## Troubleshooting

### The application opens, but packet capture fails
- Check that the correct network interface is selected.
- Confirm that the required capture library is installed.
- On Windows, check Npcap installation and permissions.
- On Linux, check packet-capture permissions and Tkinter availability.
- Review the error message shown by the application.

### Some features or charts are missing
Install the optional packages listed above, then restart the application.

### CVE lookups return no results
Check your internet connection and try again later. External services may throttle requests, change their APIs, or be temporarily unavailable. A lack of results does not mean the target is secure.

### The AI analyst does not respond
Confirm that an appropriate Anthropic API key has been entered, that network access is available, and that the account has API access. Keep API keys private and never commit them to GitHub.

## Technology Stack

- **Language:** Python
- **Desktop GUI:** Tkinter / ttk
- **Network and protocol utilities:** Python standard library and optional packet/network packages
- **Vulnerability references:** NVD API and Exploit-DB search
- **Visualization:** Matplotlib (optional)
- **Graph support:** NetworkX (optional)
- **System information:** psutil (optional)
- **AI-assisted analysis:** Anthropic API (optional)

## Roadmap

Potential improvements for future versions:

- Add automated unit and integration tests.
- Add structured logging and clearer capture diagnostics.
- Add configurable scan timeouts, concurrency limits, and rate controls.
- Improve version-aware CVE matching and clearly display source confidence.
- Add report templates and reproducible evidence summaries.
- Add configuration files and dependency pinning.
- Add a documented plugin or rule format for custom detections.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes and test them in an authorized lab.
4. Open a pull request describing the change and validation performed.

Please do not submit API keys, private packet captures, credentials, or other sensitive data in issues or pull requests.

## License

No license has been specified yet. Until a license is added to the repository, do not assume that the code is available for unrestricted reuse, redistribution, or modification. Consider adding a license file before publishing the project publicly.

## Author

**Deependra**

GitHub: `https://github.com/YOUR-USERNAME`

---

If you use or learn from ReconShield, consider starring the repository and sharing constructive feedback.
