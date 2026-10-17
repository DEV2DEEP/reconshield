#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║  ReconShield  v1.0  —   Network Security Platform                      ║
║  Developer : Deependra          ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading, socket, struct, time, os, sys, json, queue
import ipaddress, subprocess, hashlib, math, re, collections
import concurrent.futures, urllib.request, urllib.error, random
import platform, ctypes

try:
    import matplotlib; matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.patches as mpatches
    import matplotlib.patheffects as pe
    MPLOT = True
except ImportError: MPLOT = False

try: import networkx as nx; NX = True
except ImportError: NX = False

try: import psutil; PSUTIL = True
except ImportError: PSUTIL = False

_OS = sys.platform

def _is_admin():
    try:
        if _OS == "win32": return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.geteuid() == 0
    except: return False

ROOT = _is_admin()

# ═══════════════════════════════════════════════════════════════════
#  COLOUR PALETTE  —  Professional Dark Cyber Theme
# ═══════════════════════════════════════════════════════════════════
C = {
    "bg":       "#050810", "bg2":     "#080C18", "panel":   "#0C1220",
    "panel2":   "#0E1628", "card":    "#101828", "card2":   "#131E32",
    "card3":    "#0A1220", "border":  "#1C3050", "sep":     "#0C1828",
    "glow":     "#003060",
    "text":     "#B8CCE8", "text_hi": "#E8F0FF", "text_dim": "#4A6080",
    "text_muted":"#283848",
    "cyan":     "#00D8FF", "green":   "#00F080", "yellow":  "#FFD800",
    "red":      "#FF1845", "orange":  "#FF6A00", "blue":    "#2E80FF",
    "purple":   "#B060F8", "teal":    "#00B898", "pink":    "#FF60B8",
    "indigo":   "#5060C8", "lime":    "#A0FF40", "gold":    "#FFB800",
    "btn":      "#0E1E3C", "btn_h":   "#162844",
    "btn_g":    "#003020", "btn_gh":  "#004830",
    "btn_r":    "#280010", "btn_rh":  "#400018",
    "btn_b":    "#0A1E40", "btn_bh":  "#122848",
    "tsel":     "#0A2040",
    "sev_c":    "#FF1845", "sev_h":   "#FF6A00",
    "sev_m":    "#FFD800", "sev_l":   "#00F080", "sev_i":   "#2E80FF",
}

# ═══════════════════════════════════════════════════════════════════
#  WIDGET FACTORY  —  Professional styled components
# ═══════════════════════════════════════════════════════════════════
def _style_app(root):
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", background=C["bg2"], foreground=C["text"],
                 fieldbackground=C["card"], troughcolor=C["bg"],
                 selectbackground=C["tsel"], selectforeground=C["text_hi"],
                 font=("Segoe UI", 9))
    s.configure("Treeview", background=C["card"], foreground=C["text"],
                 rowheight=26, fieldbackground=C["card"],
                 borderwidth=0, relief="flat")
    s.configure("Treeview.Heading", background=C["panel2"],
                 foreground=C["cyan"], font=("Segoe UI Semibold", 9),
                 relief="flat", borderwidth=0)
    s.map("Treeview",
          background=[("selected", C["tsel"])],
          foreground=[("selected", C["text_hi"])])
    s.configure("TNotebook", background=C["bg"], borderwidth=0, tabmargins=0)
    s.configure("TNotebook.Tab", background=C["panel"],
                 foreground=C["text_dim"], padding=[20, 9],
                 font=("Segoe UI Semibold", 10), borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", C["bg2"]), ("active", C["card"])],
          foreground=[("selected", C["cyan"]), ("active", C["text"])])
    s.configure("TScrollbar", background=C["panel"],
                 troughcolor=C["bg"], arrowcolor=C["text_dim"],
                 relief="flat", borderwidth=0, width=8)
    s.configure("Horizontal.TProgressbar", background=C["cyan"],
                 troughcolor=C["panel"], borderwidth=0, thickness=4)
    s.configure("TCombobox", fieldbackground=C["card"],
                 background=C["card"], foreground=C["text"],
                 arrowcolor=C["cyan"], relief="flat")
    s.map("TCombobox", fieldbackground=[("readonly", C["card"])])
    s.configure("TSeparator", background=C["border"])


def Lbl(p, text="", **kw):
    return tk.Label(p, text=text,
                    bg=kw.pop("bg", C["bg2"]),
                    fg=kw.pop("fg", C["text"]),
                    font=kw.pop("font", ("Segoe UI", 9)), **kw)


def Btn(p, text, cmd, bg=None, fg=None, **kw):
    abg  = kw.pop("activebackground", C["btn_h"])
    afg  = kw.pop("activeforeground", C["cyan"])
    font = kw.pop("font", ("Segoe UI Semibold", 9))
    padx = kw.pop("padx", 14)
    pady = kw.pop("pady", 6)
    bd   = kw.pop("bd", 0)
    cur  = kw.pop("cursor", "hand2")
    rel  = kw.pop("relief", "flat")
    hlth = kw.pop("highlightthickness", 1)
    hlbg = kw.pop("highlightbackground", C["border"])
    b = tk.Button(p, text=text, command=cmd,
                  bg=bg or C["btn"], fg=fg or C["text_hi"],
                  font=font, relief=rel,
                  activebackground=abg, activeforeground=afg,
                  cursor=cur, padx=padx, pady=pady, bd=bd,
                  highlightthickness=hlth, highlightbackground=hlbg, **kw)
    return b


def GBtn(p, text, cmd, **kw):
    kw.setdefault("activebackground", C["btn_gh"])
    return Btn(p, text, cmd, bg=C["btn_g"], fg=C["green"], **kw)


def RBtn(p, text, cmd, **kw):
    kw.setdefault("activebackground", C["btn_rh"])
    return Btn(p, text, cmd, bg=C["btn_r"], fg=C["red"], **kw)


def BBtn(p, text, cmd, **kw):
    kw.setdefault("activebackground", C["btn_bh"])
    return Btn(p, text, cmd, bg=C["btn_b"], fg=C["blue"], **kw)


def Card(p, col=None, pad=1, **kw):
    col = col or C["border"]
    return tk.Frame(p, bg=C["card"],
                    highlightbackground=col,
                    highlightthickness=pad, **kw)


def GlowFrame(p, col=None, **kw):
    col = col or C["cyan"]
    outer = tk.Frame(p, bg=col, **kw)
    inner = tk.Frame(outer, bg=C["card"])
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    return outer, inner


def SecHdr(p, text, color=None, sub=None):
    color = color or C["cyan"]
    f = tk.Frame(p, bg=C["panel"]); f.pack(fill="x")
    tk.Frame(f, bg=color, height=2).pack(fill="x")
    inner = tk.Frame(f, bg=C["panel"], pady=9); inner.pack(fill="x")
    indicator = tk.Frame(inner, bg=color, width=4, height=22)
    indicator.pack(side="left", padx=(14, 10))
    tf = tk.Frame(inner, bg=C["panel"]); tf.pack(side="left")
    tk.Label(tf, text=text, bg=C["panel"], fg=C["text_hi"],
             font=("Segoe UI Semibold", 12)).pack(anchor="w")
    if sub:
        tk.Label(tf, text=sub, bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI", 8)).pack(anchor="w")
    return inner


def make_tree(parent, cols, widths, height=16, stretch_last=True):
    f = tk.Frame(parent, bg=C["bg"])
    tree = ttk.Treeview(f, columns=cols, show="headings", height=height)
    for i, (col, w) in enumerate(zip(cols, widths)):
        anchor = "center" if col in ("#","#","Len","TTL","Risk","Spt","Dpt") else "w"
        stretch = (i == len(cols)-1 and stretch_last)
        tree.heading(col, text=col)
        tree.column(col, width=w, minwidth=20, anchor=anchor, stretch=stretch)
    vsb = ttk.Scrollbar(f, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(f, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)
    f.pack(fill="both", expand=True)
    return tree


def StatusDot(p, color=C["green"]):
    c = tk.Canvas(p, width=10, height=10, bg=C["panel"],
                  highlightthickness=0)
    c.create_oval(1, 1, 9, 9, fill=color, outline="")
    return c

# ═══════════════════════════════════════════════════════════════════
#  NETWORK CONSTANTS & UTILITIES
# ═══════════════════════════════════════════════════════════════════
SERVICE_DB = {
    7:"Echo",19:"Chargen",20:"FTP-Data",21:"FTP",22:"SSH",23:"Telnet",
    25:"SMTP",42:"WINS",43:"WHOIS",49:"TACACS",53:"DNS",
    67:"DHCP-Server",68:"DHCP-Client",69:"TFTP",70:"Gopher",
    79:"Finger",80:"HTTP",88:"Kerberos",102:"ISO-TSAP",
    110:"POP3",111:"RPCBind",113:"Ident",119:"NNTP",
    123:"NTP",135:"MSRPC",137:"NetBIOS-NS",138:"NetBIOS-DGM",
    139:"NetBIOS-SSN",143:"IMAP",161:"SNMP",162:"SNMP-Trap",
    177:"XDMCP",179:"BGP",194:"IRC",389:"LDAP",
    443:"HTTPS",445:"SMB",464:"Kerberos-pw",465:"SMTPS",
    500:"ISAKMP",502:"Modbus",512:"rexec",513:"rlogin",
    514:"Syslog",515:"LPD",520:"RIP",521:"RIPng",
    540:"UUCP",554:"RTSP",587:"SMTP-Sub",623:"IPMI",
    631:"IPP",636:"LDAPS",647:"DHCP-Failover",873:"Rsync",
    902:"VMware-ESXi",903:"VMware-UI",993:"IMAPS",995:"POP3S",
    1080:"SOCKS5",1099:"RMI",1194:"OpenVPN",1433:"MSSQL",
    1434:"MSSQL-UDP",1521:"Oracle-DB",1723:"PPTP",
    1883:"MQTT",1900:"UPnP",2049:"NFS",2121:"FTP-Alt",
    2181:"ZooKeeper",2375:"Docker-HTTP",2376:"Docker-TLS",
    2379:"etcd",2483:"Oracle-SSL",3000:"Dev-HTTP",
    3128:"Squid-Proxy",3268:"LDAP-GC",3269:"LDAPS-GC",
    3306:"MySQL",3389:"RDP",3690:"SVN",4000:"ICQ",
    4369:"EPMD",4444:"Metasploit",4500:"IKEv2-NAT",
    4505:"SaltStack-Pub",4506:"SaltStack-Ret",
    5000:"UPnP-Alt",5432:"PostgreSQL",5555:"ADB-Android",
    5601:"Kibana",5672:"AMQP",5900:"VNC",5985:"WinRM",
    5986:"WinRM-HTTPS",6379:"Redis",6443:"K8s-API",
    6667:"IRC",7001:"WebLogic",7077:"Spark",7474:"Neo4j",
    7547:"CWMP",8009:"AJP",8080:"HTTP-Alt",8443:"HTTPS-Alt",
    8554:"RTSP-Alt",8888:"Jupyter",9000:"PHP-FPM/SonarQube",
    9001:"Tor-ORPort",9042:"Cassandra",9092:"Kafka",
    9200:"Elasticsearch",9300:"ES-Transport",9418:"Git",
    10000:"Webmin",10250:"K8s-Kubelet",11211:"Memcached",
    15672:"RabbitMQ-UI",27017:"MongoDB",27018:"MongoDB-Shard",
    28017:"MongoDB-Web",50000:"SAP-ABAP",50070:"Hadoop-NameNode",
    50075:"Hadoop-DataNode",61616:"ActiveMQ",
}

RISK_PORTS = {
    21:"High",22:"Medium",23:"Critical",25:"Medium",
    53:"Low",67:"Low",68:"Low",69:"Medium",79:"Medium",
    80:"Low",88:"Medium",110:"Medium",111:"High",
    119:"Low",123:"Low",135:"Critical",137:"Critical",
    138:"Critical",139:"Critical",143:"Medium",161:"High",
    162:"Medium",179:"Medium",389:"Medium",443:"Low",
    445:"Critical",465:"Low",500:"Medium",502:"High",
    512:"High",513:"High",514:"High",515:"Medium",
    520:"Medium",554:"Low",587:"Low",623:"Critical",
    631:"Low",636:"Low",873:"Medium",902:"High",
    993:"Low",995:"Low",1080:"High",1099:"High",
    1433:"Critical",1521:"Critical",1723:"Medium",
    1883:"Medium",1900:"Medium",2049:"High",2181:"High",
    2375:"Critical",2376:"High",2379:"Critical",
    3000:"Low",3128:"Medium",3306:"High",3389:"Critical",
    3690:"Medium",4369:"Medium",4444:"Critical",
    4505:"High",4506:"High",5432:"High",5555:"Critical",
    5601:"High",5672:"Medium",5900:"Critical",5985:"High",
    5986:"High",6379:"Critical",6443:"High",6667:"Medium",
    7001:"Critical",7474:"High",7547:"High",
    8009:"High",8080:"Low",8443:"Low",8888:"High",
    9001:"High",9042:"High",9092:"High",9200:"Critical",
    9300:"High",10000:"High",10250:"Critical",
    11211:"Critical",27017:"Critical",27018:"High",
    50070:"High",61616:"High",
}

# ═══════════════════════════════════════════════════════════════════
#  LIVE CVE ENGINE  —  Exploit-DB + NVD real-time lookup
#  All vulnerability data is fetched LIVE from:
#    • https://www.exploit-db.com   (exploit search API)
#    • https://services.nvd.nist.gov (NVD CVE API 2.0)
#  Results are cached per session to avoid duplicate requests.
#  No static CVE data is bundled — always fresh from the source.
# ═══════════════════════════════════════════════════════════════════
import html

_CVE_CACHE     = {}          # key → [cve_dict, …]
_CVE_LOCK      = threading.Lock()
_CVE_FETCHING  = set()       # keys currently being fetched (avoid dup threads)

# Service keyword map: port → search terms for Exploit-DB & NVD queries.
# This is the SOLE source for vulnerability lookups — no static CVE data.
_PORT_KEYWORDS = {
    # Remote access / shell
    21:  "vsftpd proftpd ftp",
    22:  "openssh ssh",
    23:  "telnet",
    513: "rsh rlogin",
    514: "rsh rexec",
    # Mail
    25:  "postfix sendmail smtp",
    110: "dovecot pop3",
    143: "dovecot imap",
    465: "smtps openssl",
    587: "smtp submission",
    993: "imaps openssl",
    995: "pop3s openssl",
    # DNS / NTP / SNMP
    53:  "bind named dns",
    123: "ntpd ntp",
    161: "snmp net-snmp",
    162: "snmp trap",
    # Web / HTTP
    80:  "apache nginx http",
    81:  "apache http",
    443: "openssl https apache nginx",
    631: "cups ipp",
    8000:"python flask http server",
    8008:"apache http",
    8080:"apache tomcat jboss jetty",
    8081:"apache tomcat",
    8443:"https tomcat openssl",
    8888:"jupyter notebook",
    9090:"prometheus cockpit",
    # Windows / Active Directory
    88:  "kerberos windows",
    111: "rpcbind portmap",
    135: "msrpc dcom windows",
    137: "netbios nbns windows",
    138: "netbios nbdgm",
    139: "samba smb netbios",
    389: "openldap ldap active directory",
    445: "samba smb eternalblue",
    464: "kerberos password change",
    593: "http rpc windows",
    636: "ldaps active directory",
    3268:"active directory global catalog",
    5985:"winrm powershell remoting",
    5986:"winrm https",
    # ICS / SCADA / industrial
    502: "modbus scada ics",
    102: "s7 siemens plc",
    20000: "dnp3 scada",
    44818: "ethernet ip scada rockwell",
    # Database
    1433:"mssql sql server",
    1434:"mssql browser sql server",
    1521:"oracle tns database",
    2483:"oracle jdbc",
    3306:"mysql mariadb",
    5432:"postgresql",
    5433:"postgresql",
    6379:"redis",
    7474:"neo4j graph database",
    9200:"elasticsearch",
    9300:"elasticsearch cluster",
    11211:"memcached",
    27017:"mongodb",
    27018:"mongodb",
    28017:"mongodb http",
    50000:"ibm db2",
    # Virtualization / Cloud / Container
    623: "ipmi bmc",
    2375:"docker daemon unauthenticated",
    2376:"docker tls",
    2379:"etcd kubernetes",
    2380:"etcd kubernetes",
    5000:"docker registry",
    6443:"kubernetes api server",
    8001:"kubernetes dashboard",
    10250:"kubernetes kubelet",
    10255:"kubernetes kubelet readonly",
    10256:"kubernetes kube-proxy",
    # Remote desktop / VNC
    3389:"rdp bluekeep windows",
    5900:"vnc realvnc",
    5901:"vnc",
    6000:"x11 xserver",
    # Web services / DevOps
    3000:"grafana nodejs",
    7001:"weblogic oracle",
    7002:"weblogic ssl",
    7070:"realserver rtsp",
    8161:"activemq",
    8500:"consul hashicorp",
    9000:"sonarqube php-fpm",
    9418:"git protocol",
    15672:"rabbitmq management",
    61616:"activemq",
    # File sharing
    20:  "ftp data",
    69:  "tftp",
    873: "rsync",
    2049:"nfs network file system",
    # Backdoor / C2
    4444:"metasploit meterpreter reverse shell",
    5555:"android adb",
    31337:"backdoor elite",
    # Misc
    8888:"jupyter notebook",
    50070:"hadoop namenode",
    50075:"hadoop datanode",
}

def _exploitdb_search(query, max_results=8):
    """
    Search exploit-db.com for exploits/CVEs matching query.
    Returns list of dicts: {source, edb_id, cve_id, title, date, type, platform, url, severity}
    Uses the Exploit-DB DataTables JSON API — no API key required.
    """
    results = []
    if not query or not query.strip():
        return results
    try:
        encoded = urllib.request.quote(query.strip()[:100])
        url = (f"https://www.exploit-db.com/search"
               f"?q={encoded}&draw=1&start=0&length={max_results}"
               f"&columns[0][data]=id&columns[1][data]=date_published"
               f"&columns[2][data]=title&columns[3][data]=type"
               f"&columns[4][data]=platform&columns[5][data]=author")
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":      ("Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
                                   "Gecko/20100101 Firefox/115.0"),
                "Accept":          "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "X-Requested-With":"XMLHttpRequest",
                "Referer":         "https://www.exploit-db.com/",
                "Connection":      "keep-alive",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", "replace")
        data = json.loads(raw)
        rows = data.get("data", [])

        for row in rows[:max_results]:
            try:
                # Row can be a dict (newer API) or list (legacy)
                if isinstance(row, dict):
                    eid   = str(row.get("id", ""))
                    date  = str(row.get("date_published", ""))[:10]
                    title = str(row.get("description") or row.get("title", ""))
                    etype_raw = row.get("type", {})
                    plat_raw  = row.get("platform", {})
                    etype = etype_raw.get("label","") if isinstance(etype_raw, dict) else str(etype_raw)
                    plat  = plat_raw.get("label","")  if isinstance(plat_raw,  dict) else str(plat_raw)
                    # CVE extraction from codes field if present
                    codes = row.get("codes", "") or ""
                    cve_match = re.search(r"CVE-\d{4}-\d+", str(codes) + " " + title)
                    cve_id = cve_match.group(0) if cve_match else ""
                elif isinstance(row, list) and len(row) >= 7:
                    eid   = str(row[0])
                    date  = str(row[1])[:10]
                    title = str(row[6])
                    etype = ""
                    plat  = ""
                    cve_match = re.search(r"CVE-\d{4}-\d+", title)
                    cve_id = cve_match.group(0) if cve_match else ""
                else:
                    continue

                # Clean HTML entities / tags
                title = re.sub(r"<[^>]+>", "", html.unescape(title)).strip()
                eid   = re.sub(r"<[^>]+>", "", eid).strip()
                if not eid or not title:
                    continue

                results.append({
                    "source":   "Exploit-DB",
                    "edb_id":   eid,
                    "cve_id":   cve_id,
                    "title":    title[:120],
                    "date":     date,
                    "type":     etype,
                    "platform": plat,
                    "url":      f"https://www.exploit-db.com/exploits/{eid}",
                    "severity": _infer_severity(title),
                })
            except Exception:
                continue

    except urllib.error.HTTPError as e:
        results.append({"source":"Exploit-DB", "error": f"HTTP {e.code}: {e.reason}",
                        "title": f"Exploit-DB HTTP error {e.code}", "url": "", "severity":"?"})
    except urllib.error.URLError as e:
        results.append({"source":"Exploit-DB", "error": str(e.reason)[:80],
                        "title": "Exploit-DB unreachable — check internet connection",
                        "url": "", "severity":"?"})
    except json.JSONDecodeError:
        results.append({"source":"Exploit-DB", "error": "JSON parse error",
                        "title": "Exploit-DB returned unexpected response",
                        "url": "", "severity":"?"})
    except Exception as e:
        results.append({"source":"Exploit-DB", "error": str(e)[:80],
                        "title": f"Exploit-DB error: {type(e).__name__}",
                        "url": "", "severity":"?"})
    return results


def _nvd_search(service_keyword, version_hint="", max_results=6):
    """
    Query NIST NVD CVE API 2.0 for recent CVEs matching keyword + version.
    Returns list of dicts: {cve_id, title, cvss, severity, published, url}
    """
    results = []
    try:
        kw = service_keyword.split()[0]    # use first word for NVD keyword search
        if version_hint:
            kw = f"{kw} {version_hint}"
        encoded = urllib.request.quote(kw.strip()[:80])
        url = (f"https://services.nvd.nist.gov/rest/json/cves/2.0"
               f"?keywordSearch={encoded}&resultsPerPage={max_results}"
               f"&sortBy=lastModified")
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ReconShield/1.0 (security research)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", "replace")
        data  = json.loads(raw)
        items = data.get("vulnerabilities", [])
        for item in items[:max_results]:
            try:
                cve  = item.get("cve", {})
                cid  = cve.get("id", "")
                desc = ""
                for d in cve.get("descriptions", []):
                    if d.get("lang") == "en":
                        desc = d.get("value", "")[:120]; break
                metrics = cve.get("metrics", {})
                cvss_score = None; cvss_sev = "MEDIUM"
                for key in ("cvssMetricV31","cvssMetricV30","cvssMetricV2"):
                    ms = metrics.get(key, [])
                    if ms:
                        cvss_score = ms[0].get("cvssData",{}).get("baseScore")
                        cvss_sev   = ms[0].get("cvssData",{}).get("baseSeverity",
                                      "MEDIUM").upper()
                        break
                pub = cve.get("published","")[:10]
                results.append({
                    "source":   "NVD",
                    "cve_id":   cid,
                    "title":    desc,
                    "cvss":     cvss_score,
                    "severity": cvss_sev,
                    "published":pub,
                    "url":      f"https://nvd.nist.gov/vuln/detail/{cid}",
                })
            except Exception:
                continue
    except Exception as e:
        results.append({"source":"NVD","error": str(e)[:80],
                        "title":"(NVD offline)","url":"","severity":"?"})
    return results


def _infer_severity(title):
    t = title.lower()
    if any(x in t for x in ("rce","remote code","command execution","arbitrary code",
                              "unauthenticated","authentication bypass","root","kernel",
                              "exploit","backdoor","critical")):
        return "CRITICAL"
    if any(x in t for x in ("privilege","escalation","injection","overflow","heap",
                              "stack","use-after","type confusion","high")):
        return "HIGH"
    if any(x in t for x in ("xss","csrf","disclosure","traversal","redirect",
                              "medium","denial of service","dos")):
        return "MEDIUM"
    return "LOW"


def fetch_cves_for_port(port, service="", banner="", version=""):
    """
    Main entry point: returns enriched CVE list for a given port/service/version.
    Combines Exploit-DB live search + NVD API.
    Results cached in _CVE_CACHE. Non-blocking (call from a thread).
    """
    cache_key = f"{port}:{service}:{version[:20]}"
    with _CVE_LOCK:
        if cache_key in _CVE_CACHE:
            return _CVE_CACHE[cache_key]

    results = []

    # Build search query: use version from banner if available, else service keyword
    kw = _PORT_KEYWORDS.get(port, service or f"port {port}")
    if version:
        search_q = f"{kw.split()[0]} {version}"
    else:
        search_q = kw.split()[0] if kw else service

    # 1. Exploit-DB live search
    edb = _exploitdb_search(search_q, max_results=6)
    results.extend(edb)

    # 2. NVD live search (separate keyword so we get broad CVE coverage)
    nvd = _nvd_search(kw, version_hint=version, max_results=5)
    results.extend(nvd)

    # 3. Second Exploit-DB pass — port-number search to catch anything missed
    #    e.g. "port 22 exploit" or "port 445 vulnerability"
    if not version and port:
        port_q = f"port {port} exploit"
        edb2 = _exploitdb_search(port_q, max_results=4)
        # Only add entries not already in results (deduplicate by edb_id)
        existing_ids = {r.get("edb_id","") for r in results}
        for entry in edb2:
            eid = entry.get("edb_id","")
            if eid and eid not in existing_ids:
                results.append(entry)
                existing_ids.add(eid)

    with _CVE_LOCK:
        _CVE_CACHE[cache_key] = results
    return results


def fetch_cves_async(port, service="", banner="", version="", callback=None):
    """
    Non-blocking CVE fetch. Runs in background thread.
    Calls callback(port, results) when done (on background thread — caller must
    schedule GUI update via .after() if needed).
    """
    cache_key = f"{port}:{service}:{version[:20]}"
    with _CVE_LOCK:
        if cache_key in _CVE_CACHE:
            if callback: callback(port, _CVE_CACHE[cache_key])
            return
        if cache_key in _CVE_FETCHING:
            return
        _CVE_FETCHING.add(cache_key)

    def _run():
        try:
            res = fetch_cves_for_port(port, service, banner, version)
        finally:
            with _CVE_LOCK:
                _CVE_FETCHING.discard(cache_key)
        if callback: callback(port, res)

    threading.Thread(target=_run, daemon=True, name=f"CVE-{port}").start()


def format_cve_summary(cve_list, max_items=6):
    """
    Format CVE list into a compact string for tree display.
    Shows CVE IDs + EDB IDs + severity + source. Live data only.
    """
    if not cve_list:
        return "⏳ fetching from exploit-db.com…"
    parts = []
    seen  = set()
    errors = [c for c in cve_list if c.get("error")]
    valid  = [c for c in cve_list if not c.get("error")]
    for c in valid[:max_items]:
        cve_id = c.get("cve_id","")
        edb_id = c.get("edb_id","")
        label  = cve_id or (f"EDB-{edb_id}" if edb_id else "")
        sev    = c.get("severity","?")
        src    = c.get("source","?")
        title  = c.get("title","")[:55]
        if label and label not in seen:
            seen.add(label)
            date = c.get("date","") or c.get("published","")
            date_str = f" [{date}]" if date else ""
            parts.append(f"[{sev}] {label}{date_str}  {src}  —  {title}")
    if not parts and errors:
        return f"⚠ Exploit-DB offline: {errors[0].get('error','unknown error')}"
    return "  |  ".join(parts) if parts else "⏳ fetching…"


def format_cve_detail(cve_list):
    """
    Format full CVE detail block for the CVE popup window.
    Groups by source: Exploit-DB first, then NVD.
    """
    lines = []
    if not cve_list:
        return ["⏳ Fetching live data from exploit-db.com and NVD…\n\n"]
    edb = [c for c in cve_list if c.get("source")=="Exploit-DB" and not c.get("error")]
    nvd = [c for c in cve_list if c.get("source")=="NVD"        and not c.get("error")]
    err = [c for c in cve_list if c.get("error")]

    if edb:
        lines.append(f"{'═'*68}\n")
        lines.append(f"  🔴  EXPLOIT-DB  ({len(edb)} results)   https://www.exploit-db.com\n")
        lines.append(f"{'─'*68}\n")
        for c in edb:
            eid  = c.get("edb_id","")
            cid  = c.get("cve_id","")
            sev  = c.get("severity","?")
            date = c.get("date","")
            etype= c.get("type","")
            plat = c.get("platform","")
            lines.append(f"  EDB-{eid:<8}  [{sev}]   {date}\n")
            lines.append(f"  Title    : {c.get('title','')}\n")
            if cid:   lines.append(f"  CVE ID   : {cid}\n")
            if etype: lines.append(f"  Type     : {etype}\n")
            if plat:  lines.append(f"  Platform : {plat}\n")
            if c.get("url"):
                lines.append(f"  URL      : {c['url']}\n")
            lines.append("\n")

    if nvd:
        lines.append(f"{'═'*68}\n")
        lines.append(f"  🔵  NVD (NIST)  ({len(nvd)} results)   https://nvd.nist.gov\n")
        lines.append(f"{'─'*68}\n")
        for c in nvd:
            cid   = c.get("cve_id","")
            sev   = c.get("severity","?")
            score = c.get("cvss","")
            pub   = c.get("published","")
            score_str = f"  CVSS: {score}" if score else ""
            lines.append(f"  {cid}   [{sev}]{score_str}   Published: {pub}\n")
            lines.append(f"  Desc     : {c.get('title','')}\n")
            if c.get("url"):
                lines.append(f"  URL      : {c['url']}\n")
            lines.append("\n")

    if err:
        lines.append(f"{'─'*68}\n")
        for e in err:
            lines.append(f"  ⚠  {e.get('source','?')} error: {e.get('error','')}\n")
        lines.append("\n")

    if not edb and not nvd:
        lines.append("  No results found on Exploit-DB or NVD for this service.\n")
        lines.append("  Try a manual search: https://www.exploit-db.com/search\n")

    return lines




# ═══════════════════════════════════════════════════════════════════
#  HTTP SECURITY ANALYZER  —  Real-world web attack detection
# ═══════════════════════════════════════════════════════════════════
HTTP_ATTACK_SIGS = {
    "SQL Injection": [
        (r"(?i)(union\s+select|select\s+\*\s+from|drop\s+table|insert\s+into|delete\s+from|update\s+\w+\s+set)", "CRITICAL"),
        (r"(?i)('|\%27|%27)\s*(or|and)\s*('|\%27|%27|\d)", "HIGH"),
        (r"(?i)(or\s+1=1|and\s+1=1|'='|''='|or\s+'1'='1)", "HIGH"),
        (r"(?i)(information_schema|sysobjects|xp_cmdshell|exec\s*\(|eval\s*\()", "CRITICAL"),
        (r"(?i)(sleep\s*\(\d|benchmark\s*\(|waitfor\s+delay)", "HIGH"),
    ],
    "XSS": [
        (r"(?i)(<script[\s>]|javascript:|vbscript:|on\w+=)", "HIGH"),
        (r"(?i)(alert\s*\(|confirm\s*\(|prompt\s*\(|document\.cookie|document\.write)", "HIGH"),
        (r"(?i)(<img\s[^>]*onerror|<svg\s[^>]*onload|<body\s[^>]*onload)", "HIGH"),
        (r"(?i)(%3cscript|%3e|&#x3c;script|&lt;script)", "MEDIUM"),
    ],
    "Path Traversal": [
        (r"(\.\.\/|\.\.\\|%2e%2e%2f|%2e%2e/|\.\.%2f)", "HIGH"),
        (r"(?i)(/etc/passwd|/etc/shadow|/proc/self|/windows/system32|boot\.ini)", "CRITICAL"),
        (r"(?i)(file:///|php://|expect://|zip://|data://)", "HIGH"),
    ],
    "Command Injection": [
        (r"(?i)(;\s*ls\s|;\s*cat\s|;\s*wget\s|;\s*curl\s|\|\s*nc\s|\&\&\s*id\b)", "CRITICAL"),
        (r"(?i)(`[^`]+`|\$\([^)]+\)|;\s*ping\s|;\s*whoami)", "CRITICAL"),
        (r"(?i)(%60|%7c|%26%26|%3b\s*(id|ls|cat|wget|curl)\b)", "HIGH"),
    ],
    "SSRF": [
        (r"(?i)(url=https?://(?:169\.254\.169\.254|metadata\.google|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)|url=file://)", "CRITICAL"),
        (r"(?i)(http://localhost|url=http://0\.0\.0\.0|url=http://\[::1\])", "HIGH"),
    ],
    "LFI/RFI": [
        (r"(?i)(include|require|require_once|include_once)\s*[\('\"]\s*(https?://|//|\.\.)", "HIGH"),
        (r"(?i)\?(?:file|page|path|template|include|module)=(?:https?://|//|\.\./)", "HIGH"),
    ],
    "Credential Brute-force": [
        (r"(?i)(password=|passwd=|pwd=|pass=)([^&\s]{1,6})(&|$|\s)", "MEDIUM"),
        (r"(?i)(admin|root|user|login|username)=([^&\s]+)", "LOW"),
    ],
    "Scanner/Bot UA": [
        (r"(?i)(nmap|nikto|sqlmap|dirbuster|gobuster|burp\s*suite|metasploit|nessus|openvas|masscan|zap|acunetix|w3af)", "HIGH"),
        (r"(?i)(python-requests|go-http-client/|java/|libwww-perl|lwp-useragent|curl/[0-9])", "LOW"),
    ],
}

def analyze_http_security(pkt):
    """Returns list of (category, severity, detail) tuples for detected threats."""
    threats = []
    targets = [
        pkt.http_uri or "",
        pkt.http_cookie or "",
        pkt.http_user_agent or "",
        pkt.payload_ascii or "",
    ]
    combined = " ".join(targets)
    for category, sigs in HTTP_ATTACK_SIGS.items():
        for pattern, severity in sigs:
            m = re.search(pattern, combined)
            if m:
                threats.append((category, severity, m.group(0)[:80]))
                break  # one per category
    return threats


def build_http_detail_text(pkt):
    """
    Build a rich multi-section HTTP inspector text suitable for ScrolledText display.
    Returns list of (text, tag) tuples.
    """
    d = []
    is_request = bool(pkt.http_method)
    is_response = bool(pkt.http_status) and not pkt.http_method

    # ── Header banner ──────────────────────────────────────────────
    d += [("\n","")]
    if is_request:
        method_color_map = {
            "GET": "ok", "POST": "warn", "PUT": "warn",
            "DELETE": "crit", "PATCH": "warn", "HEAD": "val",
            "OPTIONS": "val", "TRACE": "crit", "CONNECT": "crit",
        }
        mtag = method_color_map.get(pkt.http_method, "val")
        d += [("  ┌─ HTTP REQUEST ────────────────────────────────────────────────┐\n","sep")]
        d += [(f"  │  {pkt.http_method}  ", mtag)]
        d += [(f"{pkt.http_uri or '/'}  ", "info")]
        d += [(f"{pkt.http_ver or 'HTTP/1.1'}\n","dim")]
        if pkt.http_host:
            d += [(f"  │  Host: {pkt.http_host}\n","addr")]
        d += [("  └──────────────────────────────────────────────────────────────┘\n","sep")]
    elif is_response:
        status = int(pkt.http_status) if pkt.http_status and pkt.http_status.isdigit() else 0
        stag = "ok" if status < 300 else "warn" if status < 400 else "crit"
        status_msgs = {
            200:"OK",201:"Created",204:"No Content",206:"Partial Content",
            301:"Moved Permanently",302:"Found",304:"Not Modified",
            400:"Bad Request",401:"Unauthorized",403:"Forbidden",
            404:"Not Found",405:"Method Not Allowed",429:"Too Many Requests",
            500:"Internal Server Error",502:"Bad Gateway",503:"Service Unavailable",
        }
        smsg = status_msgs.get(status, "")
        d += [("  ┌─ HTTP RESPONSE ───────────────────────────────────────────────┐\n","sep")]
        d += [(f"  │  {pkt.http_ver or 'HTTP/1.1'}  {pkt.http_status}  {smsg}\n", stag)]
        if pkt.http_server:
            d += [(f"  │  Server: {pkt.http_server}\n","addr")]
        d += [("  └──────────────────────────────────────────────────────────────┘\n","sep")]
    else:
        d += [("  ┌─ HTTP DATA ───────────────────────────────────────────────────┐\n","sep")]
        d += [("  │  (HTTP payload fragment — headers incomplete)\n","dim")]
        d += [("  └──────────────────────────────────────────────────────────────┘\n","sep")]

    # ── Security Analysis ──────────────────────────────────────────
    threats = analyze_http_security(pkt)
    if threats:
        d += [("\n  ⚠ SECURITY THREATS DETECTED\n","crit")]
        d += [("  " + "═"*62 + "\n","sep")]
        for cat, sev, detail in threats:
            stag = "crit" if sev=="CRITICAL" else "warn" if sev=="HIGH" else "info"
            d += [(f"  [{sev}] {cat}\n", stag)]
            d += [(f"  Match: {detail}\n","dim")]
        d += [("\n","")]
    else:
        d += [("\n  ✅ No obvious web attack signatures detected\n","ok")]
        d += [("\n","")]

    # ── Request/Response Line ──────────────────────────────────────
    d += [("  REQUEST LINE\n","hdr")]
    d += [("  " + "─"*62 + "\n","sep")]
    if pkt.http_method:
        method = pkt.http_method
        uri    = pkt.http_uri or "/"
        ver    = pkt.http_ver or "HTTP/1.1"
        # Color the method
        mctag = {"GET":"ok","POST":"warn","PUT":"warn","DELETE":"crit",
                 "PATCH":"warn","HEAD":"val","OPTIONS":"val",
                 "TRACE":"crit","CONNECT":"crit"}.get(method,"val")
        d += [(f"  Method:   ", "dim"), (f"{method}\n", mctag)]
        d += [(f"  URI:      ", "dim"), (f"{uri}\n", "info")]
        d += [(f"  Version:  ", "dim"), (f"{ver}\n", "val")]
        # Parse query params
        if "?" in uri:
            path, qs = uri.split("?",1)
            d += [(f"  Path:     ", "dim"), (f"{path}\n", "addr")]
            d += [("\n  QUERY PARAMETERS\n","hdr")]
            d += [("  " + "─"*62 + "\n","sep")]
            params = qs.split("&")
            for p in params:
                if "=" in p:
                    pk, _, pv = p.partition("=")
                    # Highlight suspicious values
                    suspicious = bool(re.search(r"(?i)(union|select|drop|script|alert|etc/passwd|\.\.\/)", pv))
                    vtag = "crit" if suspicious else "val"
                    d += [(f"  {pk:<20} = ", "dim"), (f"{pv}\n", vtag)]
                else:
                    d += [(f"  {p}\n","dim")]
    elif pkt.http_status:
        d += [(f"  Status: ", "dim"), (f"{pkt.http_status}\n","ok" if int(pkt.http_status or 0) < 400 else "crit")]
        d += [(f"  Version: ", "dim"), (f"{pkt.http_ver}\n","val")]
    d += [("\n","")]

    # ── Host & Connection ──────────────────────────────────────────
    if pkt.http_host:
        d += [("  NETWORK IDENTITY\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        d += [(f"  Host:       ", "dim"), (f"{pkt.http_host}\n","addr")]
        d += [(f"  Src IP:     ", "dim"), (f"{pkt.src_ip or '?'}\n","addr")]
        d += [(f"  Dst IP:     ", "dim"), (f"{pkt.dst_ip or '?'}:{pkt.dport or 80}\n","addr")]
        d += [("\n","")]

    # ── All Headers ────────────────────────────────────────────────
    if pkt.http_headers:
        d += [("  REQUEST HEADERS\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        SECURITY_HDRS = {
            "authorization","cookie","x-forwarded-for","x-real-ip",
            "x-api-key","x-auth-token","bearer","proxy-authorization",
        }
        RESPONSE_SECURITY = {
            "set-cookie","content-security-policy","x-frame-options",
            "x-xss-protection","strict-transport-security",
        }
        for hk, hv in pkt.http_headers.items():
            hkl = hk.lower()
            if hkl in SECURITY_HDRS:
                htag = "warn"
                hk_disp = f"⚠ {hk}"
            elif hkl in RESPONSE_SECURITY:
                htag = "ok"
                hk_disp = f"✅ {hk}"
            else:
                htag = "dim"
                hk_disp = hk
            trunc = hv[:120] + ("…" if len(hv)>120 else "")
            d += [(f"  {hk_disp:<38} ", htag), (f"{trunc}\n","val")]
        d += [("\n","")]

    # ── Cookie Analysis ────────────────────────────────────────────
    if pkt.http_cookie:
        d += [("  🍪 COOKIE ANALYSIS\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        cookies = pkt.http_cookie.split(";")
        for ck in cookies:
            ck = ck.strip()
            if "=" in ck:
                ck_name, _, ck_val = ck.partition("=")
                is_session = any(x in ck_name.lower() for x in
                                 ("session","sessid","token","jwt","auth","sid"))
                ctag = "warn" if is_session else "val"
                d += [(f"  {ck_name.strip():<24} = ", "dim"),
                      (f"{ck_val.strip()[:60]}\n", ctag)]
        d += [("\n","")]

    # ── User-Agent Profiling ───────────────────────────────────────
    if pkt.http_user_agent:
        d += [("  USER-AGENT PROFILE\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        ua = pkt.http_user_agent
        d += [(f"  Raw:   {ua[:100]}\n","dim")]
        # Classify UA
        if re.search(r"(?i)(nmap|nikto|sqlmap|burp|metasploit|masscan|zap|acunetix|w3af|dirbuster|gobuster)", ua):
            d += [("  Class: ⚠ SECURITY SCANNER\n","crit")]
        elif re.search(r"(?i)(python-requests|curl/|wget/|go-http-client|java/|libwww)", ua):
            d += [("  Class: SCRIPT/BOT (non-browser)\n","warn")]
        elif re.search(r"(?i)(mozilla|chrome|safari|firefox|edge|opera)", ua):
            browser = ("Chrome" if "Chrome" in ua and "Edge" not in ua else
                       "Edge"   if "Edge" in ua or "Edg/" in ua else
                       "Firefox" if "Firefox" in ua else
                       "Safari"  if "Safari" in ua and "Chrome" not in ua else
                       "Browser")
            os_hint = ("Windows" if "Windows" in ua else
                       "macOS"   if "Mac OS" in ua else
                       "Linux"   if "Linux" in ua else
                       "Android" if "Android" in ua else
                       "iOS"     if "iPhone" in ua else "Unknown OS")
            d += [(f"  Class: {browser} on {os_hint}\n","ok")]
        else:
            d += [("  Class: Unknown/Custom\n","val")]
        d += [("\n","")]

    # ── Response-specific fields ───────────────────────────────────
    if pkt.http_content_type:
        d += [("  CONTENT\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        d += [(f"  Content-Type:   ", "dim"), (f"{pkt.http_content_type}\n","val")]
        if pkt.http_content_len:
            d += [(f"  Content-Length: ", "dim"), (f"{pkt.http_content_len} bytes\n","val")]
        if pkt.http_server:
            d += [(f"  Server:         ", "dim"), (f"{pkt.http_server}\n","addr")]
        d += [("\n","")]

    # ── Payload Preview ────────────────────────────────────────────
    if pkt.payload_ascii:
        d += [("  PAYLOAD PREVIEW (first 256 bytes)\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        # Try to show as text
        ascii_data = pkt.payload_ascii[:256]
        # Find the body (after headers)
        body_match = re.search(r'\r\n\r\n(.+)', ascii_data, re.DOTALL)
        if body_match:
            d += [("  Headers parsed — body follows:\n","dim")]
            body = body_match.group(1)[:200]
            d += [(f"  {body}\n","val")]
        else:
            d += [(f"  {ascii_data}\n","dim")]
        d += [("\n","")]

    # ── MITRE Mapping ──────────────────────────────────────────────
    mitre_map = {
        "SQL Injection": "T1190 Exploit Public-Facing Application",
        "XSS": "T1059.007 JavaScript",
        "Path Traversal": "T1083 File and Directory Discovery / T1005 Data from Local System",
        "Command Injection": "T1059 Command and Scripting Interpreter",
        "SSRF": "T1090.002 External Proxy / T1071 Application Layer Protocol",
        "LFI/RFI": "T1190 Exploit Public-Facing Application",
        "Scanner/Bot UA": "T1595 Active Scanning / T1046 Network Service Discovery",
    }
    if threats:
        d += [("  MITRE ATT&CK MAPPING\n","hdr")]
        d += [("  " + "─"*62 + "\n","sep")]
        seen_cats = set()
        for cat, sev, _ in threats:
            if cat not in seen_cats and cat in mitre_map:
                seen_cats.add(cat)
                d += [(f"  ⚡ {cat:<22} → {mitre_map[cat]}\n","info")]
        d += [("\n","")]

    return d


# ═══════════════════════════════════════════════════════════════════
#  TCP SESSION TRACKER  —  Groups packets into conversations
# ═══════════════════════════════════════════════════════════════════
class SessionTracker:
    """Tracks TCP sessions and reconstructs HTTP flows."""
    MAX_SESSIONS = 500

    def __init__(self):
        self._sessions = collections.OrderedDict()  # flow_key → session dict
        self._lock = threading.Lock()

    def feed(self, pkt):
        if not pkt.flow_key or not pkt.src_ip: return
        # Normalize flow key (bidirectional)
        parts = pkt.flow_key.split("-")
        if len(parts) == 2:
            a, b = parts
            fk = "-".join(sorted([a, b]))
        else:
            fk = pkt.flow_key

        with self._lock:
            if fk not in self._sessions:
                if len(self._sessions) >= self.MAX_SESSIONS:
                    self._sessions.popitem(last=False)
                self._sessions[fk] = {
                    "flow_key": fk,
                    "start_ts": pkt.ts,
                    "last_ts":  pkt.ts,
                    "src_ip":   pkt.src_ip,
                    "dst_ip":   pkt.dst_ip,
                    "sport":    pkt.sport,
                    "dport":    pkt.dport,
                    "proto":    pkt.app_proto or pkt.proto or "?",
                    "packets":  0,
                    "bytes":    0,
                    "http_reqs": [],
                    "flags_seen": set(),
                    "state":    "NEW",
                    "risk_max": 0,
                    "alerts":   [],
                }
            s = self._sessions[fk]
            s["packets"] += 1
            s["bytes"]   += pkt.length or 0
            s["last_ts"]  = pkt.ts
            s["risk_max"] = max(s["risk_max"], pkt.risk_score or 0)

            if pkt.tcp_flags_str:
                flags = set(pkt.tcp_flags_str.split())
                s["flags_seen"].update(flags)
                # State machine
                if "SYN" in flags and "ACK" not in flags:
                    s["state"] = "SYN-SENT"
                elif "SYN" in flags and "ACK" in flags:
                    s["state"] = "ESTABLISHED"
                elif "FIN" in flags:
                    s["state"] = "CLOSING"
                elif "RST" in flags:
                    s["state"] = "RESET"
                elif "ACK" in flags and s["state"] == "ESTABLISHED":
                    s["state"] = "DATA"

            # Record HTTP requests
            if pkt.app_proto == "HTTP" and pkt.http_method:
                req = {
                    "ts":     pkt.ts_str,
                    "method": pkt.http_method,
                    "uri":    pkt.http_uri or "/",
                    "host":   pkt.http_host or "",
                    "ua":     pkt.http_user_agent or "",
                    "threats": analyze_http_security(pkt),
                }
                s["http_reqs"].append(req)
                if len(s["http_reqs"]) > 20:
                    s["http_reqs"].pop(0)

    def get_sessions(self, limit=200):
        with self._lock:
            items = list(self._sessions.values())
        items.sort(key=lambda x: x["last_ts"], reverse=True)
        return items[:limit]

    def get_session(self, flow_key):
        with self._lock:
            return self._sessions.get(flow_key)

    def clear(self):
        with self._lock:
            self._sessions.clear()


BANNER_PROBES = {
    21:  b"",
    22:  b"",
    23:  b"",
    25:  b"EHLO reconshield.local\r\n",
    80:  b"HEAD / HTTP/1.1\r\nHost: target\r\nUser-Agent: ReconShield/3.0\r\nConnection: close\r\n\r\n",
    110: b"",
    143: b"",
    443: b"",
    3306:b"",
    5432:b"",
    6379:b"PING\r\n",
    9200:b"GET / HTTP/1.1\r\nHost: target\r\nConnection: close\r\n\r\n",
    8080:b"HEAD / HTTP/1.1\r\nHost: target\r\nUser-Agent: ReconShield/3.0\r\nConnection: close\r\n\r\n",
    8443:b"HEAD / HTTP/1.1\r\nHost: target\r\nConnection: close\r\n\r\n",
    27017:b"",
    11211:b"stats\r\n",
    6667: b"NICK reconshield\r\nUSER rs 0 * :rs\r\n",
    5900: b"\x00",
    2375: b"GET /info HTTP/1.0\r\n\r\n",
}

# Detailed OS fingerprinting from TTL
def ttl_os(ttl):
    if ttl is None: return "Unknown"
    if ttl <= 64:   return "Linux / macOS / iOS / Android"
    if ttl <= 128:  return "Windows"
    if ttl <= 255:  return "Cisco IOS / Network Device"
    return "Unknown"

# Expanded TTL → OS + initial TTL guess
def ttl_os_detail(ttl):
    if ttl is None: return "Unknown", None
    if ttl <= 64:
        init = 64
        if ttl >= 60:   os_ = "Linux 4.x/5.x (Ubuntu/Debian/CentOS)"
        elif ttl >= 55: os_ = "macOS / iOS"
        else:           os_ = "Linux (older kernel or routed)"
    elif ttl <= 128:
        init = 128
        if ttl >= 120:  os_ = "Windows 10/11/Server 2019"
        elif ttl >= 110:os_ = "Windows 7/8/Server 2012"
        else:           os_ = "Windows (older / routed)"
    else:
        init = 255
        os_ = "Cisco IOS / JunOS / Network Device"
    hops = init - ttl
    return os_, hops


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close()
        return ip
    except: return "127.0.0.1"


def get_all_iface_ips():
    result = collections.OrderedDict()
    if PSUTIL:
        stats = psutil.net_if_stats() if hasattr(psutil,"net_if_stats") else {}
        for name, addrs in sorted(psutil.net_if_addrs().items()):
            for a in addrs:
                if a.family == socket.AF_INET:
                    up = stats.get(name) and stats[name].isup if stats else True
                    result[name] = {"ip": a.address, "mask": a.netmask or "",
                                    "up": up}
    if not result:
        try:
            out = subprocess.check_output(["ip","addr"],
                  stderr=subprocess.DEVNULL, text=True)
            cur = None
            for line in out.splitlines():
                m = re.match(r"\d+: (\S+):", line)
                if m: cur = m.group(1).rstrip(":")
                m2 = re.search(r"inet (\d+\.\d+\.\d+\.\d+)/(\d+)", line)
                if m2 and cur:
                    result[cur] = {"ip": m2.group(1),
                                   "mask": str(ipaddress.ip_network(
                                       f"{m2.group(1)}/{m2.group(2)}",
                                       strict=False).netmask),
                                   "up": True}
        except: pass
    if not result:
        result["default"] = {"ip": get_local_ip(), "mask": "", "up": True}
    return result


def get_arp_table():
    arp = {}
    try:
        with open("/proc/net/arp") as f:
            for line in f.readlines()[1:]:
                p = line.split()
                if len(p) >= 4 and p[3] != "00:00:00:00:00:00":
                    arp[p[0]] = p[3].upper()
    except:
        try:
            if _OS == "win32":
                out = subprocess.check_output(["arp","-a"],
                      stderr=subprocess.DEVNULL, text=True)
                for line in out.splitlines():
                    m = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([\w-]{17})", line)
                    if m:
                        mac = m.group(2).replace("-",":").upper()
                        arp[m.group(1)] = mac
            else:
                out = subprocess.check_output(["arp","-a"],
                      stderr=subprocess.DEVNULL, text=True)
                for line in out.splitlines():
                    m = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9A-Fa-f:]+)", line)
                    if m: arp[m.group(1)] = m.group(2).upper()
        except: pass
    return arp


def _icmp_checksum(data):
    s = 0
    for i in range(0, len(data)-1, 2):
        s += (data[i] << 8) + data[i+1]
    if len(data) % 2: s += data[-1] << 8
    s = (s >> 16) + (s & 0xFFFF); s += s >> 16
    return ~s & 0xFFFF



def icmp_ping(host, timeout=0.8):
    """Fast ICMP ping — 0.8s max wait."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)
        pid  = os.getpid() & 0xFFFF
        hdr  = struct.pack("!BBHHH", 8, 0, 0, pid, 1)
        pay  = b"RS3PROBE" * 2
        chk  = _icmp_checksum(hdr + pay)
        pkt  = struct.pack("!BBHHH", 8, 0, chk, pid, 1) + pay
        t0   = time.time()
        sock.sendto(pkt, (host, 0))
        deadline = t0 + timeout
        while True:
            rem = deadline - time.time()
            if rem <= 0: break
            sock.settimeout(rem)
            try:   data, addr = sock.recvfrom(1024)
            except socket.timeout: break
            if addr[0] == host and len(data) >= 28 and data[20] == 0:
                rtt = (time.time() - t0) * 1000
                ttl = data[8]
                sock.close()
                return True, round(rtt, 2), ttl
        sock.close()
        return False, None, None
    except PermissionError:
        return _tcp_probe(host), None, None
    except:
        return False, None, None


def _tcp_probe(host, ports=(80, 443, 22, 135, 445, 8080, 3389, 8443, 3306, 53)):
    """Parallel TCP probe — all ports at once, return on first hit."""
    result = [False]
    ev = threading.Event()
    def _try(p):
        if ev.is_set(): return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((host, p)) == 0:
                result[0] = True; ev.set()
            s.close()
        except: pass
    threads = [threading.Thread(target=_try, args=(p,), daemon=True) for p in ports]
    for t in threads: t.start()
    ev.wait(timeout=0.7)
    return result[0]


def grab_banner(ip, port, timeout=0.8):
    """Fast banner grab."""
    probe = BANNER_PROBES.get(port)
    if probe is None: probe = b"\r\n"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        if probe: s.sendall(probe)
        data = b""
        s.settimeout(0.45)
        try:
            while len(data) < 2048:
                chunk = s.recv(512)
                if not chunk: break
                data += chunk
        except: pass
        s.close()
        txt = data.decode("utf-8", "replace").strip()
        txt = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", txt)
        return txt[:512]
    except:
        return ""


def scan_ports(host, port_range=None, timeout=0.35, workers=768, stop_ev=None,
               progress_cb=None, udp_scan=False):
    """
    Ultra-fast parallel TCP connect scanner + optional UDP probe.
    service  = ~220 known ports   (~1-2s/host at 768 workers)
    top1000  = 1024 ports         (~3-5s/host)
    full     = 1-65535            (~20-40s/host at 2048 workers)

    Speed tricks:
    - Pre-allocate sockets per thread using socket pool
    - Chunked batches with adaptive sizing
    - Non-blocking connect + select() for batch confirmation
    - Banner grab only on open ports, fully parallel
    """
    if port_range == "full":
        ports   = list(range(1, 65536))
        timeout = 0.22
        workers = 2048
    elif port_range == "top1000":
        ports   = sorted(set(list(SERVICE_DB.keys()) + list(range(1, 1025))))
        timeout = 0.28
        workers = 1024
    else:
        ports   = sorted(SERVICE_DB.keys())
        timeout = 0.35
        workers = 512

    open_ports_tcp = []
    total          = len(ports)

    # -- Phase A: Batch non-blocking connect scan ----------------------
    # Group ports into large chunks, use select() to wait on many at once
    BATCH = 512
    done_n = [0]

    def _batch_scan(batch):
        """Try a batch of ports using non-blocking sockets + select."""
        if stop_ev and stop_ev.is_set(): return []
        socks  = {}
        hits   = []
        import select as _select
        for p in batch:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setblocking(False)
                err = s.connect_ex((host, p))
                # EINPROGRESS (115 Linux / 10035 Win) = connecting
                if err in (0, 115, 10035, 36):
                    socks[s.fileno()] = (s, p)
                else:
                    s.close()
            except: pass

        if not socks:
            return []

        deadline = time.time() + timeout
        fd_map   = dict(socks)
        while fd_map and time.time() < deadline:
            rem = deadline - time.time()
            if rem <= 0: break
            try:
                r_list, w_list, _ = _select.select(
                    [], list(fd_map.keys()), [], min(rem, 0.1))
            except: break
            for fd in w_list:
                info = fd_map.pop(fd, None)
                if not info: continue
                s, p = info
                try:
                    err = s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if err == 0:
                        hits.append(p)
                except: pass
                finally:
                    try: s.close()
                    except: pass

        # Close remaining
        for fd, (s, p) in list(fd_map.items()):
            try: s.close()
            except: pass

        return hits

    # Fall back to simple connect if select-based fails (Windows quirk)
    def _simple_probe(p):
        if stop_ev and stop_ev.is_set(): return p, False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            r = s.connect_ex((host, p))
            s.close()
            return p, r == 0
        except: return p, False

    # Try select-based batch first, fall back to thread-pool
    try:
        for i in range(0, len(ports), BATCH):
            if stop_ev and stop_ev.is_set(): break
            chunk   = ports[i:i+BATCH]
            results = _batch_scan(chunk)
            open_ports_tcp.extend(results)
            done_n[0] += len(chunk)
            if progress_cb:
                progress_cb(done_n[0], total, len(open_ports_tcp))
    except Exception:
        # Full fallback: thread pool connect
        open_ports_tcp = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            for p, open_ in ex.map(_simple_probe, ports):
                if open_: open_ports_tcp.append(p)
            done_n[0] = len(ports)
            if progress_cb: progress_cb(done_n[0], total, len(open_ports_tcp))

    # -- Phase B: UDP probe for known UDP services ---------------------
    UDP_PORTS = {53,67,68,69,123,137,138,161,162,500,514,1900,4500,5353}
    open_ports_udp = []
    if udp_scan and ROOT:
        def _udp_probe(p):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(0.5)
                probe_map = {
                    53: b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                        b"\x07version\x04bind\x00\x00\x10\x00\x03",
                    123: b"\x1b" + b"\x00"*47,
                    161: b"\x30\x26\x02\x01\x00\x04\x06public\xa0\x19"
                         b"\x02\x04\x00\x00\x00\x01\x02\x01\x00\x02\x01\x00"
                         b"\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00",
                }
                s.sendto(probe_map.get(p, b"\x00"), (host, p))
                data, _ = s.recvfrom(512)
                s.close()
                return p, True
            except: return p, False

        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
            for p, ok in ex.map(_udp_probe, UDP_PORTS):
                if ok: open_ports_udp.append(p)

    if not open_ports_tcp and not open_ports_udp:
        return {}

    # -- Phase C: Parallel banner grab + enrichment -------------------
    results = {}
    all_open = [(p,"tcp") for p in open_ports_tcp] + \
               [(p,"udp") for p in open_ports_udp]

    def _enrich(args):
        p, proto = args
        banner = grab_banner(host, p) if proto == "tcp" else ""
        svc    = SERVICE_DB.get(p, f"unknown-{p}")
        # Extract version info from banner
        ver = _parse_version(banner)
        # Dynamic CVE lookup: live Exploit-DB + NVD + static fallback
        cve_list    = fetch_cves_for_port(p, service=svc, banner=banner, version=ver)
        cve_summary = format_cve_summary(cve_list, max_items=5)
        return p, {
            "service":   svc,
            "version":   ver,
            "risk":      RISK_PORTS.get(p, "Low"),
            "banner":    banner,
            "cve":       cve_summary,
            "cve_list":  cve_list,          # full structured list for popup
            "state":     "open",
            "protocol":  proto,
        }

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(128, len(all_open)+1)) as ex:
        for p, info in ex.map(_enrich, all_open):
            results[p] = info

    return results


def _parse_version(banner):
    """Extract version string from service banner."""
    if not banner: return ""
    patterns = [
        r"OpenSSH[_\s]([\d.]+\w*)",
        r"Apache[/\s]([\d.]+)",
        r"nginx[/\s]([\d.]+)",
        r"Microsoft-IIS[/\s]([\d.]+)",
        r"vsftpd\s([\d.]+)",
        r"ProFTPD\s([\d.]+)",
        r"Postfix\s([\d.]+)",
        r"Exim\s([\d.]+)",
        r"MySQL\s([\d.]+)",
        r"MariaDB\s([\d.]+)",
        r"PostgreSQL\s([\d.]+)",
        r"Redis\s([\d.]+)",
        r"SSH-([\d.]+)-([\w\d.]+)",
        r"([\d]+\.[\d]+\.[\d]+\.[\d]+)",  # fallback: any x.y.z.w
    ]
    for pat in patterns:
        m = re.search(pat, banner, re.IGNORECASE)
        if m: return m.group(0)[:40]
    return ""


def classify_risk(ports_dict):
    if not ports_dict: return "Unknown"
    risks = [d.get("risk","Low") for d in ports_dict.values()]
    for r in ("Critical","High","Medium"):
        if r in risks: return r
    return "Low"


def subnet_scan(target, timeout=0.7, workers=512, stop_ev=None, cb=None):
    """
    Phase 1: Mass parallel host discovery (ICMP flood + TCP fallback)
    Returns live hosts dict. Port scanning is done separately via parallel_port_scan().
    """
    hosts_to_probe = []
    for t in [x.strip() for x in target.replace(";",",").split(",")]:
        if not t: continue
        try:
            net = ipaddress.ip_network(t, strict=False)
            hosts_to_probe.extend(net.hosts())
        except ValueError:
            try:
                ip = socket.gethostbyname(t)
                hosts_to_probe.append(ipaddress.ip_address(ip))
            except: pass

    if not hosts_to_probe: return {}

    # ── Filter to real-world routable addresses only ──────────────────
    def _is_routable(ip_obj):
        s = str(ip_obj)
        a = ip_obj
        if a.is_loopback: return False
        if a.is_link_local: return False   # 169.254.x.x
        if a.is_multicast: return False
        if s == "0.0.0.0" or s == "255.255.255.255": return False
        return True

    hosts_to_probe = [h for h in hosts_to_probe if _is_routable(h)]
    if not hosts_to_probe: return {}

    arp_table  = get_arp_table()
    live_hosts = {}
    total      = len(hosts_to_probe)
    done_n     = [0]

    def _discover(ip):
        ip_s = str(ip)
        if stop_ev and stop_ev.is_set(): return ip_s, None
        alive, rtt, ttl = icmp_ping(ip_s, timeout)
        if not alive:
            alive = _tcp_probe(ip_s)
            ttl = None; rtt = None
        if not alive:
            return ip_s, None
        try:    hn = socket.gethostbyaddr(ip_s)[0]
        except: hn = ""
        mac = arp_table.get(ip_s, "")
        os_guess, hops = ttl_os_detail(ttl)
        return ip_s, {
            "ip": ip_s, "hostname": hn, "os": os_guess,
            "ttl": ttl, "hops": hops, "rtt": rtt,
            "mac": mac, "vendor": _mac_vendor(mac),
            "ports": {}, "risk": "Unknown", "alive": True,
            "scan_ts": time.strftime("%H:%M:%S"),
        }

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(workers, len(hosts_to_probe))) as ex:
        futs = {ex.submit(_discover, ip): ip for ip in hosts_to_probe}
        for f in concurrent.futures.as_completed(futs):
            done_n[0] += 1
            ip_s, data = f.result()
            if data: live_hosts[ip_s] = data
            if cb: cb(done_n[0], total, len(live_hosts))
            if stop_ev and stop_ev.is_set(): break

    return live_hosts


def parallel_port_scan(host_db, port_range, stop_ev, progress_cb, result_cb):
    """
    Scan ALL hosts simultaneously in parallel — much faster than sequential.
    progress_cb(done, total, ip) — called as each host finishes
    result_cb(ip, ports_dict)    — called to update UI per host
    """
    hosts      = list(host_db.keys())
    if not hosts: return
    total      = len(hosts)
    done_n     = [0]
    per_host   = max(32, min(256, 2048 // max(len(hosts), 1)))

    def _scan_one(ip):
        if stop_ev and stop_ev.is_set(): return ip, {}
        ports = scan_ports(ip, port_range=port_range,
                           workers=per_host, stop_ev=stop_ev)
        done_n[0] += 1
        if progress_cb: progress_cb(done_n[0], total, ip)
        return ip, ports

    host_workers = min(len(hosts), 24)
    with concurrent.futures.ThreadPoolExecutor(max_workers=host_workers) as ex:
        futs = {ex.submit(_scan_one, ip): ip for ip in hosts}
        for f in concurrent.futures.as_completed(futs):
            ip, ports = f.result()
            if result_cb: result_cb(ip, ports)
            if stop_ev and stop_ev.is_set(): break


_VENDOR_CACHE = {}
def _mac_vendor(mac):
    if not mac or len(mac) < 8: return ""
    prefix = mac[:8].upper()
    if prefix in _VENDOR_CACHE: return _VENDOR_CACHE[prefix]
    OUI = {
        "00:50:56":"VMware","00:0C:29":"VMware","00:1A:11":"Google",
        "B8:27:EB":"Raspberry Pi","DC:A6:32":"Raspberry Pi",
        "00:1B:21":"Intel","8C:8D:28":"Intel","F8:34:41":"Apple",
        "A4:C3:F0":"Apple","00:50:F2":"Microsoft","28:D2:44":"Microsoft",
        "00:26:B9":"Dell","14:18:77":"Dell","B8:AC:6F":"Cisco",
        "00:1E:BE":"Cisco","00:16:3E":"Xen/AWS","06:00:00":"Loopback",
        "00:00:00":"Generic","FC:EC:DA":"Ubiquiti",
    }
    v = OUI.get(prefix, "")
    _VENDOR_CACHE[prefix] = v
    return v

# ═══════════════════════════════════════════════════════════════════
#  PACKET DECODER  —  15-Layer deep inspection
# ═══════════════════════════════════════════════════════════════════
class PacketInfo:
    __slots__ = [
        "seq","ts","ts_str","length","iface",
        "eth_src","eth_dst","eth_type","eth_type_name","vlan_id",
        "ip_ver","ip_ihl","ip_dscp","ip_ecn","ip_total_len","ip_id",
        "ip_flags","ip_frag","ip_ttl","ip_proto","ip_proto_name",
        "ip_checksum","src_ip","dst_ip",
        "tcp_sport","tcp_dport","tcp_seq","tcp_ack_num","tcp_data_off",
        "tcp_flags_raw","tcp_flags_str","tcp_win","tcp_checksum","tcp_urg",
        "tcp_opts",
        "udp_sport","udp_dport","udp_len","udp_checksum",
        "icmp_type","icmp_code","icmp_type_name","icmp_id","icmp_seq",
        "app_proto","sport","dport",
        "http_method","http_uri","http_host","http_status","http_ver",
        "http_user_agent","http_content_type","http_server","http_cookie",
        "http_content_len","http_headers",
        "tls_ver","tls_sni","tls_record_type","tls_cipher_suite",
        "dns_txid","dns_qr","dns_opcode","dns_query","dns_qtype",
        "dns_answers","dns_flags","dns_rcode","dns_aa","dns_tc",
        "ftp_cmd","ftp_resp","smtp_cmd","smtp_resp",
        "ssh_banner","ssh_ver",
        "arp_op","arp_smac","arp_sip","arp_tmac","arp_dip",
        "dhcp_op","dhcp_xid","dhcp_client_ip","dhcp_msg_type",
        "ntp_mode","ntp_stratum","ntp_ref_id",
        "snmp_ver","snmp_community","snmp_pdu_type",
        "payload_len","payload_entropy","payload_hex","payload_ascii","payload_raw",
        "risk_score","alert","direction","proto","info","flow_key","conn_state",
    ]

    def __init__(self):
        for s in self.__slots__: setattr(self, s, None)
        self.ts        = time.time()
        self.ts_str    = time.strftime("%H:%M:%S.") + f"{int((self.ts%1)*1000):03d}"
        self.alert     = False
        self.tcp_flags_str = ""
        self.dns_answers   = []
        self.app_proto = ""
        self.risk_score = 0
        self.proto = ""
        self.info  = ""
        self.http_headers = {}


def _entropy(data):
    if not data: return 0.0
    freq = collections.Counter(data); n = len(data)
    return -sum((c/n)*math.log2(c/n) for c in freq.values() if c > 0)


def _dns_labels(data, off, depth=0):
    if depth > 12: return [], off
    labels = []
    while off < len(data):
        ln = data[off]
        if ln == 0: off += 1; break
        if (ln & 0xC0) == 0xC0:
            if off+1 >= len(data): break
            ptr = ((ln & 0x3F) << 8) | data[off+1]
            lbl, _ = _dns_labels(data, ptr, depth+1)
            labels += lbl; off += 2; break
        off += 1
        if off+ln > len(data): break
        try: labels.append(data[off:off+ln].decode("ascii","replace"))
        except: labels.append("?")
        off += ln
    return labels, off


ETH_TYPES  = {0x0800:"IPv4",0x0806:"ARP",0x86DD:"IPv6",0x8100:"VLAN",
               0x8847:"MPLS",0x8863:"PPPoE-D",0x8864:"PPPoE-S",0x88CC:"LLDP"}
IP_PROTOS  = {1:"ICMP",6:"TCP",17:"UDP",47:"GRE",50:"ESP",51:"AH",
               58:"ICMPv6",89:"OSPF",132:"SCTP"}
TLS_VERS   = {0x0301:"TLS 1.0",0x0302:"TLS 1.1",0x0303:"TLS 1.2",0x0304:"TLS 1.3",
               0x0300:"SSL 3.0",0x0002:"SSL 2.0"}
ICMP_TYPES = {0:"Echo Reply",3:"Dest Unreachable",4:"Source Quench",
               5:"Redirect",8:"Echo Request",9:"Router Advert",
               10:"Router Solicitation",11:"TTL Exceeded",
               12:"Parameter Problem",13:"Timestamp Req",14:"Timestamp Reply",
               17:"Address Mask Req",18:"Address Mask Reply",30:"Traceroute"}
DNS_QTYPES = {1:"A",2:"NS",5:"CNAME",6:"SOA",10:"NULL",12:"PTR",
               13:"HINFO",15:"MX",16:"TXT",17:"RP",18:"AFSDB",
               24:"SIG",25:"KEY",28:"AAAA",29:"LOC",33:"SRV",
               35:"NAPTR",36:"KX",43:"DS",46:"RRSIG",47:"NSEC",
               48:"DNSKEY",52:"TLSA",255:"ANY",256:"URI"}
FLAG_BITS  = [(0x001,"FIN"),(0x002,"SYN"),(0x004,"RST"),(0x008,"PSH"),
               (0x010,"ACK"),(0x020,"URG"),(0x040,"ECE"),(0x080,"CWR"),
               (0x100,"NS")]


def decode_packet(raw: bytes, seq: int) -> PacketInfo:
    p = PacketInfo()
    p.seq    = seq
    p.length = len(raw)
    if len(raw) < 14: return p

    # ── L2 Ethernet ──────────────────────────────────────────────────
    p.eth_dst = ":".join(f"{b:02X}" for b in raw[0:6])
    p.eth_src = ":".join(f"{b:02X}" for b in raw[6:12])
    etype = struct.unpack("!H", raw[12:14])[0]
    off   = 14

    # 802.1Q VLAN
    if etype == 0x8100 and len(raw) >= off+4:
        p.vlan_id = struct.unpack("!H", raw[off:off+2])[0] & 0x0FFF
        etype     = struct.unpack("!H", raw[off+2:off+4])[0]
        off      += 4

    p.eth_type      = f"0x{etype:04X}"
    p.eth_type_name = ETH_TYPES.get(etype, f"0x{etype:04X}")

    # ── ARP ──────────────────────────────────────────────────────────
    if etype == 0x0806 and len(raw) >= off+28:
        d  = raw[off:]
        op = struct.unpack("!H", d[6:8])[0]
        p.arp_op   = "Request" if op==1 else "Reply" if op==2 else f"Op-{op}"
        p.arp_smac = ":".join(f"{b:02X}" for b in d[8:14])
        p.arp_sip  = socket.inet_ntoa(d[14:18])
        p.arp_tmac = ":".join(f"{b:02X}" for b in d[18:24])
        p.arp_dip  = socket.inet_ntoa(d[24:28])
        p.src_ip   = p.arp_sip; p.dst_ip = p.arp_dip
        p.proto = "ARP"; p.app_proto = "ARP"
        p.info  = f"ARP {p.arp_op}: {p.arp_sip} ({p.arp_smac}) → {p.arp_dip}"
        return p

    if etype != 0x0800: return p

    # ── IPv4 ─────────────────────────────────────────────────────────
    if len(raw) < off+20: return p
    iph = raw[off:off+20]
    p.ip_ver        = iph[0] >> 4
    p.ip_ihl        = (iph[0] & 0x0F) * 4
    p.ip_dscp       = iph[1] >> 2
    p.ip_ecn        = iph[1] & 0x03
    p.ip_total_len  = struct.unpack("!H", iph[2:4])[0]
    p.ip_id         = struct.unpack("!H", iph[4:6])[0]
    ff              = struct.unpack("!H", iph[6:8])[0]
    p.ip_flags      = (ff >> 13) & 0x7
    p.ip_frag       = ff & 0x1FFF
    p.ip_ttl        = iph[8]
    p.ip_proto      = iph[9]
    p.ip_checksum   = f"0x{struct.unpack('!H', iph[10:12])[0]:04X}"
    p.src_ip        = socket.inet_ntoa(iph[12:16])
    p.dst_ip        = socket.inet_ntoa(iph[16:20])
    p.ip_proto_name = IP_PROTOS.get(p.ip_proto, f"Proto-{p.ip_proto}")
    p.proto         = p.ip_proto_name
    t_off           = off + p.ip_ihl
    p.flow_key      = f"{p.src_ip}:{p.ip_proto}:{p.dst_ip}"

    # ── ICMP ─────────────────────────────────────────────────────────
    if p.ip_proto == 1 and len(raw) >= t_off+8:
        ih = raw[t_off:t_off+8]
        p.icmp_type      = ih[0]; p.icmp_code = ih[1]
        p.icmp_type_name = ICMP_TYPES.get(p.icmp_type, f"Type-{p.icmp_type}")
        if p.icmp_type in (0,8) and len(ih) >= 8:
            p.icmp_id  = struct.unpack("!H", ih[4:6])[0]
            p.icmp_seq = struct.unpack("!H", ih[6:8])[0]
        p.app_proto = "ICMP"
        p.info = (f"ICMP {p.icmp_type_name} "
                  f"{p.src_ip} → {p.dst_ip} "
                  f"code={p.icmp_code}"
                  + (f" id={p.icmp_id} seq={p.icmp_seq}" if p.icmp_id else ""))
        p.risk_score = 20 if p.icmp_type in (3,5,11) else 5
        return p

    # ── TCP ──────────────────────────────────────────────────────────
    if p.ip_proto == 6 and len(raw) >= t_off+20:
        th = raw[t_off:t_off+20]
        p.tcp_sport    = struct.unpack("!H", th[0:2])[0]
        p.tcp_dport    = struct.unpack("!H", th[2:4])[0]
        p.sport        = p.tcp_sport; p.dport = p.tcp_dport
        p.tcp_seq      = struct.unpack("!I", th[4:8])[0]
        p.tcp_ack_num  = struct.unpack("!I", th[8:12])[0]
        p.tcp_data_off = (th[12] >> 4) * 4
        raw_f          = struct.unpack("!H", th[12:14])[0] & 0x1FF
        p.tcp_flags_raw= f"0x{raw_f:03X}"
        p.tcp_flags_str= " ".join(n for b,n in FLAG_BITS if raw_f & b) or "NONE"
        p.tcp_win      = struct.unpack("!H", th[14:16])[0]
        p.tcp_checksum = f"0x{struct.unpack('!H', th[16:18])[0]:04X}"
        p.tcp_urg      = struct.unpack("!H", th[18:20])[0]
        p.flow_key     = f"{p.src_ip}:{p.tcp_sport}-{p.dst_ip}:{p.tcp_dport}"
        payload        = raw[t_off + p.tcp_data_off:]

        # TCP Options parsing
        if p.tcp_data_off > 20:
            opts_raw = th[20:p.tcp_data_off] if p.tcp_data_off <= len(th) else b""
            opts = []
            i = 0
            while i < len(opts_raw):
                k = opts_raw[i]
                if k == 0: break
                if k == 1: i+=1; continue
                if i+1 >= len(opts_raw): break
                l = opts_raw[i+1]
                if l < 2: break
                OPT_NAMES = {2:"MSS",3:"WScale",4:"SACK-OK",
                              5:"SACK",8:"Timestamp",34:"TFO"}
                opts.append(OPT_NAMES.get(k,f"Opt-{k}"))
                i += l
            p.tcp_opts = ",".join(opts) if opts else ""

        # ── TLS ──────────────────────────────────────────────────────
        if p.tcp_dport in (443,8443,465,993,995,636,6443,8883) or \
           p.tcp_sport in (443,8443,465,993,995,636,6443,8883):
            p.app_proto = "TLS"
            if len(payload) >= 6 and payload[0] in (0x14,0x15,0x16,0x17):
                RT = {0x14:"ChangeCipherSpec",0x15:"Alert",
                      0x16:"Handshake",0x17:"AppData"}
                p.tls_record_type = RT.get(payload[0],"?")
                ver = struct.unpack("!H", payload[1:3])[0]
                p.tls_ver = TLS_VERS.get(ver, f"0x{ver:04X}")
                # Extract SNI from ClientHello
                if payload[0] == 0x16 and len(payload) > 43 and payload[5] == 0x01:
                    try:
                        i = 5+4+2+32
                        sl = payload[i] if i < len(payload) else 0
                        i += 1+sl
                        if i+2 < len(payload):
                            cl = struct.unpack("!H", payload[i:i+2])[0]
                            i += 2+cl+1
                            if i+2 < len(payload):
                                ext_l = struct.unpack("!H", payload[i:i+2])[0]
                                i += 2; end = i+ext_l
                                while i+4 <= end and i < len(payload):
                                    et = struct.unpack("!H", payload[i:i+2])[0]
                                    el = struct.unpack("!H", payload[i+2:i+4])[0]
                                    if et == 0 and i+4+el <= len(payload):
                                        sd = payload[i+4:i+4+el]
                                        if len(sd) > 5:
                                            sl2 = struct.unpack("!H", sd[3:5])[0]
                                            p.tls_sni = sd[5:5+sl2].decode("ascii","replace")
                                    i += 4+el
                    except: pass

        # ── HTTP ─────────────────────────────────────────────────────
        elif p.tcp_dport in (80,8080,8000,3000,8008,8888) or \
             p.tcp_sport in (80,8080,8000,3000,8008,8888):
            p.app_proto = "HTTP"
            try:
                text = payload.decode("utf-8","replace")
                lines = text.split("\r\n")
                if lines:
                    fl = lines[0]
                    m = re.match(r"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH|TRACE|CONNECT) (\S+) (HTTP/[\d.]+)", fl)
                    if m:
                        p.http_method = m.group(1); p.http_uri = m.group(2)
                        p.http_ver    = m.group(3)
                    elif re.match(r"HTTP/", fl):
                        m2 = re.match(r"(HTTP/[\d.]+) (\d+)", fl)
                        if m2: p.http_ver = m2.group(1); p.http_status = m2.group(2)
                    hdrs = {}
                    for ln in lines[1:]:
                        if ":" not in ln: continue
                        k, _, v = ln.partition(":")
                        hdrs[k.lower().strip()] = v.strip()
                    p.http_headers      = hdrs
                    p.http_host         = hdrs.get("host","")
                    p.http_user_agent   = hdrs.get("user-agent","")[:100]
                    p.http_content_type = hdrs.get("content-type","")
                    p.http_server       = hdrs.get("server","")
                    p.http_cookie       = hdrs.get("cookie","")[:80]
                    p.http_content_len  = hdrs.get("content-length","")
            except: pass

        # ── SSH ──────────────────────────────────────────────────────
        elif p.tcp_dport == 22 or p.tcp_sport == 22:
            p.app_proto = "SSH"
            try:
                t = payload.decode("utf-8","replace")
                if t.startswith("SSH-"):
                    p.ssh_banner = t.strip()[:120]
                    parts = t.split("-",2)
                    if len(parts) >= 2: p.ssh_ver = parts[1]
            except: pass

        # ── FTP ──────────────────────────────────────────────────────
        elif p.tcp_dport in (20,21) or p.tcp_sport in (20,21):
            p.app_proto = "FTP"
            try:
                t = payload.decode("utf-8","replace").strip()
                if re.match(r"^\d{3} ", t): p.ftp_resp = t[:120]
                else: p.ftp_cmd = t[:120]
            except: pass

        # ── SMTP ─────────────────────────────────────────────────────
        elif p.tcp_dport in (25,465,587) or p.tcp_sport in (25,465,587):
            p.app_proto = "SMTP"
            try:
                t = payload.decode("utf-8","replace").strip()
                if re.match(r"^\d{3}[ -]", t): p.smtp_resp = t[:120]
                else: p.smtp_cmd = t[:120]
            except: pass

        else:
            p.app_proto = SERVICE_DB.get(p.tcp_dport,
                          SERVICE_DB.get(p.tcp_sport, "TCP"))

        p.payload_raw     = payload[:128]
        p.payload_len     = len(payload)
        p.payload_entropy = round(_entropy(payload), 4) if payload else 0.0
        if payload:
            p.payload_hex   = payload[:64].hex()
            p.payload_ascii = re.sub(r"[^\x20-\x7E]",".",
                              payload[:64].decode("latin-1","replace"))
        p.info = (f"TCP [{p.tcp_flags_str}] "
                  f"{p.src_ip}:{p.tcp_sport} → {p.dst_ip}:{p.tcp_dport} "
                  f"[{p.app_proto}] len={p.payload_len} win={p.tcp_win}")

    # ── UDP ──────────────────────────────────────────────────────────
    elif p.ip_proto == 17 and len(raw) >= t_off+8:
        uh = raw[t_off:t_off+8]
        p.udp_sport    = struct.unpack("!H", uh[0:2])[0]
        p.udp_dport    = struct.unpack("!H", uh[2:4])[0]
        p.sport        = p.udp_sport; p.dport = p.udp_dport
        p.udp_len      = struct.unpack("!H", uh[4:6])[0]
        p.udp_checksum = f"0x{struct.unpack('!H', uh[6:8])[0]:04X}"
        p.flow_key     = f"{p.src_ip}:{p.udp_sport}-{p.dst_ip}:{p.udp_dport}"
        payload        = raw[t_off+8:]
        p.payload_len  = len(payload)
        p.payload_entropy = round(_entropy(payload), 4) if payload else 0.0
        if payload:
            p.payload_hex   = payload[:64].hex()
            p.payload_ascii = re.sub(r"[^\x20-\x7E]",".",
                              payload[:64].decode("latin-1","replace"))

        # DNS
        if (p.udp_dport == 53 or p.udp_sport == 53) and len(payload) >= 12:
            p.app_proto = "DNS"
            try:
                p.dns_txid = struct.unpack("!H", payload[0:2])[0]
                fw = struct.unpack("!H", payload[2:4])[0]
                p.dns_flags  = f"0x{fw:04X}"
                p.dns_qr     = "Response" if (fw&0x8000) else "Query"
                p.dns_opcode = (fw>>11)&0xF
                p.dns_aa     = bool(fw&0x400)
                p.dns_tc     = bool(fw&0x200)
                p.dns_rcode  = fw&0xF
                qd = struct.unpack("!H", payload[4:6])[0]
                an = struct.unpack("!H", payload[6:8])[0]
                doff = 12
                for _ in range(qd):
                    lbls, doff = _dns_labels(payload, doff)
                    if lbls: p.dns_query = ".".join(lbls)
                    if doff+4 <= len(payload):
                        qt = struct.unpack("!H", payload[doff:doff+2])[0]
                        p.dns_qtype = DNS_QTYPES.get(qt, str(qt))
                        doff += 4
                answers = []
                for _ in range(min(an, 8)):
                    lbls, doff = _dns_labels(payload, doff)
                    if doff+10 > len(payload): break
                    at  = struct.unpack("!H", payload[doff:doff+2])[0]
                    doff += 4
                    rdl = struct.unpack("!H", payload[doff+2:doff+4])[0]
                    rd  = payload[doff+4:doff+4+rdl]
                    if at==1 and rdl==4: answers.append(socket.inet_ntoa(rd))
                    elif at==28 and rdl==16:
                        try: answers.append(socket.inet6_ntoa(rd))
                        except: pass
                    elif at in (2,5,12):
                        lbs2, _ = _dns_labels(payload, doff+4)
                        if lbs2: answers.append(".".join(lbs2))
                    doff += 4+rdl
                p.dns_answers = answers
            except: pass
            p.info = (f"DNS {p.dns_qr or ''} id=0x{p.dns_txid or 0:04X} "
                      f"q={p.dns_query} ({p.dns_qtype}) "
                      f"ans={','.join(p.dns_answers[:3])}")
        elif p.udp_dport in (67,68):
            p.app_proto = "DHCP"
            p.info = f"DHCP {p.src_ip}:{p.udp_sport} → {p.dst_ip}:{p.udp_dport}"
        elif p.udp_dport in (123,) or p.udp_sport == 123:
            p.app_proto = "NTP"
            if len(payload) >= 4:
                p.ntp_mode    = payload[0] & 0x07
                p.ntp_stratum = payload[1]
        elif p.udp_dport in (161,162) or p.udp_sport in (161,162):
            p.app_proto = "SNMP"
        elif p.udp_dport == 500 or p.udp_sport == 500:
            p.app_proto = "IKE/IPSec"
        elif p.udp_dport == 1900 or p.udp_sport == 1900:
            p.app_proto = "UPnP"
        elif p.udp_dport == 5353 or p.udp_sport == 5353:
            p.app_proto = "mDNS"
        else:
            p.app_proto = SERVICE_DB.get(p.udp_dport,
                          SERVICE_DB.get(p.udp_sport, "UDP"))
        if not p.info:
            p.info = (f"UDP {p.src_ip}:{p.udp_sport} → "
                      f"{p.dst_ip}:{p.udp_dport} [{p.app_proto}] "
                      f"len={p.udp_len}")

    # ── Risk scoring ──────────────────────────────────────────────────
    rs = 0
    if p.ip_ttl and p.ip_ttl < 5: rs += 35
    if p.payload_entropy and p.payload_entropy > 7.4: rs += 30
    if p.payload_entropy and p.payload_entropy > 7.8: rs += 20
    if p.tcp_flags_str and "SYN" in p.tcp_flags_str and "ACK" not in p.tcp_flags_str: rs += 8
    if p.dport in (4444,31337,1337,12345,6666,6667,5554): rs += 45
    if p.app_proto == "DNS" and p.dns_query and len(p.dns_query) > 60: rs += 25
    if p.dport in (23,135,139,445,3389,5900,6379,9200,27017): rs += 20
    if p.tcp_flags_str and all(f in p.tcp_flags_str for f in ("FIN","URG","PSH")): rs += 30
    if p.tcp_flags_str == "NONE": rs += 25
    if p.ip_frag and p.ip_frag > 0: rs += 15
    p.risk_score = min(rs, 100)

    if not p.info:
        p.info = f"{p.proto or '?'} {p.src_ip or '?'} → {p.dst_ip or '?'} len={p.length}"
    return p

# ═══════════════════════════════════════════════════════════════════
#  CAPTURE ENGINE
# ═══════════════════════════════════════════════════════════════════
def _enable_promisc_linux(iface):
    try:
        import fcntl, struct as _s
        SIOCGIFFLAGS=0x8913; SIOCSIFFLAGS=0x8914; IFF_PROMISC=0x100
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ifreq = _s.pack("16sh", iface.encode()[:15], 0)
        flags = _s.unpack("16sh", fcntl.ioctl(s, SIOCGIFFLAGS, ifreq))[1]
        fcntl.ioctl(s, SIOCSIFFLAGS,
                    _s.pack("16sh", iface.encode()[:15], flags|IFF_PROMISC))
        s.close()
    except: pass

def _disable_promisc_linux(iface):
    try:
        import fcntl, struct as _s
        SIOCGIFFLAGS=0x8913; SIOCSIFFLAGS=0x8914; IFF_PROMISC=0x100
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ifreq = _s.pack("16sh", iface.encode()[:15], 0)
        flags = _s.unpack("16sh", fcntl.ioctl(s, SIOCGIFFLAGS, ifreq))[1]
        fcntl.ioctl(s, SIOCSIFFLAGS,
                    _s.pack("16sh", iface.encode()[:15], flags & ~IFF_PROMISC))
        s.close()
    except: pass

# ── Npcap / WinPcap Windows helper ──────────────────────────────────────────
def _npcap_available():
    """Check if Npcap or WinPcap DLL is installed (Windows only)."""
    if _OS != "win32": return False
    try:
        import ctypes
        ctypes.WinDLL("wpcap.dll"); return True
    except Exception: return False

def _scapy_available():
    try: import scapy.all; return True  # noqa
    except Exception: return False

def _npcap_open_live(iface_name):
    """
    Open a live capture handle via ctypes wpcap.dll.
    Returns (handle, errbuf) or (None, error_str).
    Strategy:
      - Try the adapter by GUID name from WinAPI
      - Fall back to \\Device\\NPF_{...} prefix
    """
    try:
        import ctypes, ctypes.wintypes as wt
        wpcap = ctypes.WinDLL("wpcap.dll")

        PCAP_ERRBUF = ctypes.create_string_buffer(256)
        SNAPLEN     = 65535
        PROMISC     = 1
        TIMEOUT_MS  = 1000

        # Build device name — Npcap uses \\Device\\NPF_{GUID}
        if not iface_name.startswith("\\"):
            iface_name = f"\\Device\\NPF_{{{iface_name}}}" if len(iface_name) == 36 else iface_name

        handle = wpcap.pcap_open_live(
            iface_name.encode(), SNAPLEN, PROMISC,
            TIMEOUT_MS, PCAP_ERRBUF)
        if not handle:
            return None, PCAP_ERRBUF.value.decode(errors="replace")
        return handle, ""
    except Exception as e:
        return None, str(e)


# ── Linux: enable promiscuous via ioctl ─────────────────────────────────────
def _set_promisc_linux(iface, enable=True):
    try:
        import fcntl, struct as _s
        SIOCGIFFLAGS = 0x8913; SIOCSIFFLAGS = 0x8914; IFF_PROMISC = 0x100
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ifreq = _s.pack("16sh", iface.encode("utf-8")[:15], 0)
        flags = _s.unpack("16sh", fcntl.ioctl(s, SIOCGIFFLAGS, ifreq))[1]
        flags = (flags | IFF_PROMISC) if enable else (flags & ~IFF_PROMISC)
        fcntl.ioctl(s, SIOCSIFFLAGS, _s.pack("16sh", iface.encode("utf-8")[:15], flags))
        s.close()
    except Exception: pass


# ── Legacy aliases (used elsewhere) ─────────────────────────────────────────
def _enable_promisc_linux(iface):  _set_promisc_linux(iface, True)
def _disable_promisc_linux(iface): _set_promisc_linux(iface, False)


# ════════════════════════════════════════════════════════════════════════════
#  CAPTURE ENGINE  —  Real-world multi-device network capture
#
#  Capture strategy (tried in order):
#
#  Windows:
#    1. Scapy + Npcap  → genuine promiscuous — sees ALL devices on segment
#    2. Npcap ctypes   → raw wpcap.dll pcap_loop — ALL devices
#    3. SIO_RCVALL     → Windows raw socket — only own-machine traffic
#       (limitation of Windows without Npcap — instruct user to install it)
#
#  Linux/macOS:
#    1. AF_PACKET SOCK_RAW ETH_P_ALL + IFF_PROMISC → ALL frames on wire
#       (requires root/CAP_NET_RAW)
#
#  Why SIO_RCVALL alone is NOT enough:
#    Windows NIC driver only delivers unicast frames addressed to the host MAC
#    to the raw socket even with RCVALL_ON. Npcap bypasses the driver stack
#    entirely via NDIS filter driver and sees ALL layer-2 frames.
# ════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════
#  REAL-WORLD PACKET FILTER  —  Drop loopback, multicast, link-local
# ═══════════════════════════════════════════════════════════════════
def _is_real_world_packet(pkt) -> bool:
    """
    Returns True only if the packet involves real, routable network devices.
    Drops:
      - Loopback (127.x.x.x)
      - Link-local / APIPA (169.254.x.x)
      - Unspecified source (0.0.0.0)
      - IPv4 multicast (224.x – 239.x)
      - Limited broadcast (255.255.255.255)
      - Packets with no src or dst IP (non-IP, e.g. pure L2 noise)
        EXCEPT ARP which is always useful for device discovery.
    """
    # Always keep ARP — useful for real device discovery
    if pkt.app_proto == "ARP":
        return True
    src = pkt.src_ip or ""
    dst = pkt.dst_ip or ""
    # Must have at least one routable IP
    if not src and not dst:
        return False
    for ip in (src, dst):
        if not ip:
            continue
        # Loopback
        if ip.startswith("127."):
            return False
        # Unspecified
        if ip == "0.0.0.0":
            return False
        # Link-local / APIPA
        if ip.startswith("169.254."):
            return False
        # Multicast range 224.0.0.0/4
        try:
            first = int(ip.split(".")[0])
            if 224 <= first <= 239:
                return False
        except Exception:
            pass
        # Limited broadcast
        if ip == "255.255.255.255":
            return False
    return True


class CaptureEngine(threading.Thread):
    # Synthetic Ethernet header prepended to Windows raw IP (no L2 header)
    _ETH_FAKE = b"\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x08\x00"

    def __init__(self, pkt_queue, stats, stop_ev, iface=None):
        super().__init__(daemon=True, name="RS-Capture")
        self.pkt_queue = pkt_queue
        self.stats     = stats
        self.stop_ev   = stop_ev
        self.iface     = iface   # interface name string
        self._seq      = 0
        self._bytes    = 0

    def run(self):
        try:
            if _OS == "win32":
                self._win_capture()
            else:
                self._linux_capture()
        except PermissionError:
            self.stats["error"] = (
                "PERMISSION DENIED\n\n"
                "Windows: Right-click → Run as Administrator\n"
                "Linux  : sudo python3 ReconShield.py\n\n"
                "For full network capture (all devices) install Npcap:\n"
                "  https://npcap.com/#download")
        except OSError as e:
            self.stats["error"] = f"Socket error: {e}"
        except Exception as e:
            self.stats["error"] = f"Capture error: {e}"

    # ════════════════════════════════════════════════════════════════
    #  LINUX / macOS  —  AF_PACKET promiscuous, sees all wire frames
    # ════════════════════════════════════════════════════════════════
    def _linux_capture(self):
        """
        AF_PACKET + ETH_P_ALL captures every Ethernet frame on the wire,
        including frames NOT addressed to this machine, after NIC is put
        into promiscuous mode. This is genuine full-network capture.
        """
        ETH_P_ALL = 0x0003
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                             socket.htons(ETH_P_ALL))

        # Set SO_RCVBUF large to avoid kernel drop
        try: sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
        except: pass

        target_iface = self.iface
        if target_iface and target_iface not in ("", "any", "ALL interfaces"):
            try:
                sock.bind((target_iface, 0))
                _set_promisc_linux(target_iface, True)
                self.stats["iface"]  = target_iface
                self.stats["method"] = "AF_PACKET promiscuous"
            except OSError as e:
                self.stats["error"] = f"Cannot bind {target_iface}: {e}"
                sock.close(); return
        else:
            # Bind to ALL interfaces — captures frames from every adapter
            # Promiscuous on all active non-loopback interfaces
            all_ifaces = get_all_iface_ips()
            for name, info in all_ifaces.items():
                if not info["ip"].startswith("127."):
                    _set_promisc_linux(name, True)
            self.stats["iface"]  = "ALL"
            self.stats["method"] = "AF_PACKET ETH_P_ALL (all ifaces)"

        sock.setblocking(False)
        import select as _select
        try:
            while not self.stop_ev.is_set():
                ready, _, _ = _select.select([sock], [], [], 0.3)
                if ready:
                    try:
                        raw, ancdata = sock.recvfrom(65535)
                        self._handle(raw)
                    except BlockingIOError: pass
                    except OSError: break
        finally:
            if target_iface and target_iface not in ("", "any", "ALL interfaces"):
                _set_promisc_linux(target_iface, False)
            else:
                all_ifaces = get_all_iface_ips()
                for name in all_ifaces:
                    if not all_ifaces[name]["ip"].startswith("127."):
                        _set_promisc_linux(name, False)
            try: sock.close()
            except: pass

    # ════════════════════════════════════════════════════════════════
    #  WINDOWS  —  Tries Scapy → Npcap ctypes → SIO_RCVALL fallback
    # ════════════════════════════════════════════════════════════════
    def _win_capture(self):
        # Strategy 1: Scapy with Npcap (best — full promiscuous)
        if _scapy_available():
            try:
                self._win_scapy()
                return
            except Exception as e:
                self.stats["warn"] = f"Scapy failed: {e}, trying Npcap direct"

        # Strategy 2: Direct Npcap wpcap.dll via ctypes
        if _npcap_available():
            try:
                self._win_npcap()
                return
            except Exception as e:
                self.stats["warn"] = f"Npcap direct failed: {e}, falling back to SIO_RCVALL"

        # Strategy 3: SIO_RCVALL fallback (own machine traffic only)
        self.stats["warn"] = (
            "⚠ Npcap not found — capturing own-machine traffic only.\n"
            "Install Npcap for full network capture:\n"
            "https://npcap.com/#download")
        self._win_rcvall()

    def _win_scapy(self):
        """Use Scapy's sniff() — requires Npcap. Sees ALL network devices."""
        from scapy.all import sniff, Raw, Ether  # noqa
        import scapy.all as sc

        iface_arg = None
        if self.iface and self.iface not in ("", "ALL interfaces"):
            iface_arg = self.iface
        self.stats["iface"]  = iface_arg or "ALL"
        self.stats["method"] = "Scapy + Npcap (full promiscuous)"

        def _pkt_cb(spkt):
            if self.stop_ev.is_set(): return
            try:
                raw = bytes(spkt)
                # Scapy gives Ethernet frames directly
                self._handle(raw)
            except: pass

        stop_filter = lambda p: self.stop_ev.is_set()  # noqa
        sc.sniff(
            iface=iface_arg,
            prn=_pkt_cb,
            store=False,
            promisc=True,
            stop_filter=stop_filter,
            count=0,
        )

    def _win_npcap(self):
        """
        Capture via wpcap.dll (Npcap) using ctypes pcap_next_ex().
        Genuine promiscuous — sees all devices on the network segment.
        """
        import ctypes, ctypes.wintypes as wt
        wpcap = ctypes.WinDLL("wpcap.dll")

        # Enumerate devices via pcap_findalldevs
        class pcap_if(ctypes.Structure): pass
        class pcap_addr(ctypes.Structure): pass
        pcap_if._fields_ = [
            ("next",        ctypes.POINTER(pcap_if)),
            ("name",        ctypes.c_char_p),
            ("description", ctypes.c_char_p),
            ("addresses",   ctypes.c_void_p),
            ("flags",       ctypes.c_uint),
        ]
        alldevs   = ctypes.POINTER(pcap_if)()
        errbuf    = ctypes.create_string_buffer(256)
        if wpcap.pcap_findalldevs(ctypes.byref(alldevs), errbuf) == -1:
            raise RuntimeError(f"pcap_findalldevs failed: {errbuf.value}")

        # Pick the right device
        chosen = None
        d = alldevs
        while d:
            name = d.contents.name.decode() if d.contents.name else ""
            desc = d.contents.description.decode() if d.contents.description else ""
            if self.iface and (self.iface in name or self.iface in desc):
                chosen = name; break
            # Prefer first non-loopback
            if not chosen and "loopback" not in desc.lower() and "npcap loopback" not in desc.lower():
                chosen = name
            d = d.contents.next if d.contents.next else None
        wpcap.pcap_freealldevs(alldevs)

        if not chosen:
            raise RuntimeError("No suitable Npcap device found")

        SNAPLEN    = 65535
        PROMISC    = 1
        TIMEOUT_MS = 50  # ms — low for responsiveness

        handle = wpcap.pcap_open_live(
            chosen.encode(), SNAPLEN, PROMISC, TIMEOUT_MS, errbuf)
        if not handle:
            raise RuntimeError(f"pcap_open_live failed: {errbuf.value}")

        self.stats["iface"]  = chosen
        self.stats["method"] = f"Npcap wpcap.dll promiscuous ({chosen[:40]})"

        # Packet header struct
        class timeval(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]
        class pcap_pkthdr(ctypes.Structure):
            _fields_ = [("ts", timeval), ("caplen", ctypes.c_uint),
                        ("len", ctypes.c_uint)]

        pkthdr_p  = ctypes.POINTER(pcap_pkthdr)()
        pktdata_p = ctypes.POINTER(ctypes.c_ubyte)()

        try:
            while not self.stop_ev.is_set():
                ret = wpcap.pcap_next_ex(
                    handle,
                    ctypes.byref(pkthdr_p),
                    ctypes.byref(pktdata_p))
                if ret == 1:
                    caplen = pkthdr_p.contents.caplen
                    raw    = bytes(pktdata_p[:caplen])
                    self._handle(raw)
                elif ret == 0:
                    pass  # timeout, try again
                else:
                    break  # error or EOF
        finally:
            try: wpcap.pcap_close(handle)
            except: pass

    def _win_rcvall(self):
        """
        SIO_RCVALL fallback — captures IP traffic to/from THIS machine only.
        Works without Npcap but limited to own-machine traffic.
        Multiple sockets — one per non-loopback adapter to catch all NICs.
        """
        ifaces  = get_all_iface_ips()
        sockets = []

        # If specific iface chosen, only that one
        if self.iface and self.iface in ifaces:
            bind_ips = [ifaces[self.iface]["ip"]]
        else:
            # ALL non-loopback adapters
            bind_ips = [v["ip"] for v in ifaces.values()
                        if not v["ip"].startswith("127.")]
        if not bind_ips:
            bind_ips = [get_local_ip()]

        for ip in bind_ips:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_IP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                try: s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,
                                  4 * 1024 * 1024)
                except: pass
                s.bind((ip, 0))
                s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
                s.setblocking(False)
                sockets.append((s, ip))
            except Exception as e:
                pass

        if not sockets:
            self.stats["error"] = "Could not open any capture socket"
            return

        bind_str = ", ".join(ip for _, ip in sockets)
        self.stats["iface"]  = bind_str
        self.stats["method"] = f"SIO_RCVALL on {bind_str} (own-machine only)"

        import select as _select
        try:
            while not self.stop_ev.is_set():
                rd = [s for s, _ in sockets]
                ready, _, _ = _select.select(rd, [], [], 0.3)
                for s in ready:
                    try:
                        raw, _ = s.recvfrom(65535)
                        # No Ethernet header — prepend synthetic one
                        self._handle(self._ETH_FAKE + raw)
                    except BlockingIOError: pass
                    except OSError: pass
        finally:
            for s, _ in sockets:
                try: s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                except: pass
                try: s.close()
                except: pass

    # ════════════════════════════════════════════════════════════════
    #  Shared packet handler
    # ════════════════════════════════════════════════════════════════
    def _handle(self, raw):
        if not raw: return
        self._seq   += 1
        self._bytes += len(raw)
        try:
            pkt = decode_packet(raw, self._seq)
        except Exception:
            return
        # ── Real-world filter: drop loopback, multicast, link-local, etc. ──
        if not _is_real_world_packet(pkt):
            return
        self.stats["total"]  = self._seq
        self.stats["bytes"]  = self._bytes
        proto = pkt.app_proto or pkt.proto or "OTHER"
        self.stats[proto] = self.stats.get(proto, 0) + 1
        try:
            self.pkt_queue.put_nowait(pkt)
        except queue.Full:
            try:    self.pkt_queue.get_nowait()
            except: pass
            try:    self.pkt_queue.put_nowait(pkt)
            except: pass


# ═══════════════════════════════════════════════════════════════════
#  THREAT ENGINE  —  12 Detection Rules
# ═══════════════════════════════════════════════════════════════════
class Alert:
    __slots__ = ["ts","ts_str","severity","rule","title","src","dst",
                 "desc","evidence","mitre"]
    def __init__(self, sev, rule, title, src, dst, desc, evidence, mitre=""):
        self.ts       = time.time()
        self.ts_str   = time.strftime("%H:%M:%S", time.localtime(self.ts))
        self.severity = sev; self.rule = rule; self.title = title
        self.src = src; self.dst = dst; self.desc = desc
        self.evidence = evidence; self.mitre = mitre


class ThreatEngine:
    WINDOW = 5.0

    def __init__(self, cb=None):
        self.cb        = cb
        self.alerts    = collections.deque(maxlen=2000)
        self.rule_hits = collections.defaultdict(int)
        self._lock     = threading.Lock()
        # State per source IP
        self._syn    = collections.defaultdict(list)
        self._udp    = collections.defaultdict(list)
        self._icmp   = collections.defaultdict(list)
        self._ports  = collections.defaultdict(lambda: collections.defaultdict(set))
        self._conns  = collections.defaultdict(list)
        self._dns    = collections.defaultdict(list)
        self._bytes  = collections.defaultdict(list)
        self._arp_map= {}
        self._seen   = set()
        self._ewma   = {}

    def feed(self, pkt):
        now = pkt.ts
        src = pkt.src_ip or ""; dst = pkt.dst_ip or ""

        def _alert(sev, rule, title, desc, evidence, mitre=""):
            key = hashlib.md5(f"{rule}{src}{dst}{title}".encode()).hexdigest()
            if key in self._seen: return
            self._seen.add(key)
            if len(self._seen) > 8000: self._seen.clear()
            a = Alert(sev, rule, title, src, dst, desc, evidence, mitre)
            with self._lock:
                self.alerts.append(a)
                self.rule_hits[rule] += 1
            if self.cb: self.cb(a)

        # R01 SYN Flood
        if (pkt.tcp_flags_str and "SYN" in pkt.tcp_flags_str
                and "ACK" not in pkt.tcp_flags_str):
            self._syn[src].append(now)
            self._syn[src] = [t for t in self._syn[src] if now-t < self.WINDOW]
            if len(self._syn[src]) >= 80:
                _alert("CRITICAL","R01-SYN-FLOOD",
                       f"SYN Flood from {src}",
                       f"{len(self._syn[src])} SYN packets in {self.WINDOW}s",
                       {"count":len(self._syn[src]),"dst":dst},
                       "T1499.001")

        # R02 UDP Flood
        if pkt.proto == "UDP" and src:
            self._udp[src].append(now)
            self._udp[src] = [t for t in self._udp[src] if now-t < self.WINDOW]
            if len(self._udp[src]) >= 200:
                _alert("HIGH","R02-UDP-FLOOD",
                       f"UDP Flood from {src}",
                       f"{len(self._udp[src])} UDP pkts in {self.WINDOW}s",
                       {"count":len(self._udp[src])},
                       "T1499.002")

        # R03 ICMP Flood
        if pkt.proto == "ICMP" and src:
            self._icmp[src].append(now)
            self._icmp[src] = [t for t in self._icmp[src] if now-t < self.WINDOW]
            if len(self._icmp[src]) >= 100:
                _alert("HIGH","R03-ICMP-FLOOD",
                       f"ICMP Flood from {src}",
                       f"{len(self._icmp[src])} ICMP pkts in {self.WINDOW}s",
                       {"count":len(self._icmp[src])},
                       "T1499.003")

        # R04 Port Scan
        if (pkt.dport and isinstance(pkt.dport, int) and
                pkt.tcp_flags_str and "SYN" in pkt.tcp_flags_str and src):
            self._ports[src][now//30].add(pkt.dport)
            bucket = int(now // 30)
            ports_set = self._ports[src][bucket]
            if len(ports_set) >= 25:
                sev = "HIGH" if len(ports_set) >= 50 else "MEDIUM"
                _alert(sev,"R04-PORT-SCAN",
                       f"Port Scan from {src}",
                       f"{len(ports_set)} distinct ports in 30s window",
                       {"ports":sorted(list(ports_set))[:20],"dst":dst},
                       "T1046")

        # R05 Brute-Force (SSH/RDP/FTP)
        if (pkt.tcp_flags_str and "SYN" in pkt.tcp_flags_str and
                pkt.dport in (22,3389,21,23,1433,3306,5432,5900) and src):
            self._conns[f"{src}:{pkt.dport}"].append(now)
            lst = self._conns[f"{src}:{pkt.dport}"]
            lst[:] = [t for t in lst if now-t < 30]
            if len(lst) >= 20:
                svc = SERVICE_DB.get(pkt.dport,"?")
                _alert("HIGH","R05-BRUTE-FORCE",
                       f"Brute-Force {svc} from {src}",
                       f"{len(lst)} connection attempts to {svc} in 30s",
                       {"count":len(lst),"port":pkt.dport,"service":svc},
                       "T1110")

        # R06 DNS Tunnelling
        if pkt.app_proto == "DNS" and src:
            if pkt.dns_query and len(pkt.dns_query) > 60:
                _alert("MEDIUM","R06-DNS-TUNNEL",
                       f"DNS Tunnel — long query from {src}",
                       f"Query length {len(pkt.dns_query)} chars: {pkt.dns_query[:80]}",
                       {"query":pkt.dns_query,"len":len(pkt.dns_query)},
                       "T1071.004")
            self._dns[src].append(now)
            self._dns[src] = [t for t in self._dns[src] if now-t < 10]
            if len(self._dns[src]) >= 50:
                _alert("MEDIUM","R06-DNS-FLOOD",
                       f"DNS Flood from {src}",
                       f"{len(self._dns[src])} DNS queries in 10s",
                       {"count":len(self._dns[src])},
                       "T1071.004")

        # R07 Data Exfiltration (high entropy + large)
        if (pkt.payload_entropy and pkt.payload_entropy > 7.2 and
                pkt.payload_len and pkt.payload_len > 500 and src):
            self._bytes[src].append((now, pkt.payload_len))
            self._bytes[src] = [(t,b) for t,b in self._bytes[src] if now-t < 60]
            total = sum(b for _,b in self._bytes[src])
            if total > 500_000:
                _alert("HIGH","R07-EXFILTRATION",
                       f"Data Exfiltration suspected from {src}",
                       f"Entropy={pkt.payload_entropy:.2f} | {total//1024}KB in 60s",
                       {"entropy":pkt.payload_entropy,"bytes":total},
                       "T1030")

        # R08 Volumetric DDoS (EWMA)
        proto_key = pkt.app_proto or pkt.proto or "?"
        self._ewma[proto_key] = (self._ewma.get(proto_key, 0) * 0.85
                                  + 1 * 0.15)
        if self._ewma.get(proto_key, 0) > 500:
            _alert("CRITICAL","R08-DDOS",
                   f"DDoS — {proto_key} volumetric attack",
                   f"EWMA rate {self._ewma[proto_key]:.0f} pkt/s",
                   {"proto":proto_key,"ewma":self._ewma[proto_key]},
                   "T1498")

        # R09 ARP Spoofing
        if pkt.app_proto == "ARP" and pkt.arp_op == "Reply" and pkt.arp_sip:
            prev_mac = self._arp_map.get(pkt.arp_sip)
            if prev_mac and prev_mac != pkt.arp_smac:
                _alert("CRITICAL","R09-ARP-SPOOF",
                       f"ARP Spoofing: {pkt.arp_sip}",
                       f"MAC changed {prev_mac} → {pkt.arp_smac}",
                       {"ip":pkt.arp_sip,"old_mac":prev_mac,
                        "new_mac":pkt.arp_smac},
                       "T1557.002")
            self._arp_map[pkt.arp_sip] = pkt.arp_smac

        # R10 Xmas Scan
        if (pkt.tcp_flags_str and
                all(f in pkt.tcp_flags_str for f in ("FIN","URG","PSH"))):
            _alert("HIGH","R10-XMAS-SCAN",
                   f"Xmas Scan from {src}",
                   f"FIN+URG+PSH flags to {dst}:{pkt.dport}",
                   {"flags":pkt.tcp_flags_str,"port":pkt.dport},
                   "T1046")

        # R11 TCP Null Scan
        if pkt.tcp_flags_str == "NONE" and pkt.proto == "TCP":
            _alert("HIGH","R11-NULL-SCAN",
                   f"TCP Null Scan from {src}",
                   f"Zero TCP flags to {dst}:{pkt.dport}",
                   {"port":pkt.dport},
                   "T1046")

        # R12 Backdoor / RAT port
        if pkt.dport in (4444,31337,1337,12345,6666,6667,5554,9001,4899):
            _alert("HIGH","R12-BACKDOOR",
                   f"Backdoor/RAT Port {pkt.dport} from {src}",
                   f"Connection to known backdoor port {pkt.dport}",
                   {"port":pkt.dport,"src":src,"dst":dst},
                   "T1219")

        # R13 Cleartext creds (Telnet/FTP/HTTP basic)
        if pkt.dport in (23,21) and pkt.payload_ascii:
            t = pkt.payload_ascii.lower()
            if any(k in t for k in ("pass","password","login","user")):
                _alert("CRITICAL","R13-CLEARTEXT-CREDS",
                       f"Cleartext credentials on port {pkt.dport}",
                       f"Protocol {SERVICE_DB.get(pkt.dport,'?')} — credentials in plaintext",
                       {"port":pkt.dport,"preview":pkt.payload_ascii[:60]},
                       "T1040")

        # R14 Suspicious TLS (outdated version)
        if pkt.tls_ver in ("SSL 2.0","SSL 3.0","TLS 1.0","TLS 1.1"):
            _alert("MEDIUM","R14-WEAK-TLS",
                   f"Weak TLS {pkt.tls_ver} from {src}",
                   f"Deprecated {pkt.tls_ver} detected",
                   {"version":pkt.tls_ver,"sni":pkt.tls_sni},
                   "T1040")

        # R15 ICMP redirect
        if pkt.icmp_type == 5:
            _alert("MEDIUM","R15-ICMP-REDIRECT",
                   f"ICMP Redirect from {src}",
                   "ICMP Type 5 Redirect — potential MITM",
                   {"code":pkt.icmp_code,"src":src,"dst":dst},
                   "T1557")

    def get_alerts(self, n=100):
        with self._lock:
            return list(self.alerts)[-n:]


# ═══════════════════════════════════════════════════════════════════
#  AI AGENT
# ═══════════════════════════════════════════════════════════════════
class AIAgent:
    MODEL = "claude-sonnet-4-20250514"
    SYSTEM = """You are an elite SOC analyst and penetration tester embedded in ReconShield v1.0 — 
a professional network security platform. You have deep expertise in:
- Network forensics and packet analysis
- MITRE ATT&CK framework mapping
- Vulnerability assessment and CVE analysis  
- Incident response and threat hunting
- IDS/IPS rule development
- Malware analysis and IOC extraction
- Zero-day threat detection

Respond concisely but comprehensively. Use structured output with severity labels,
MITRE tactics/techniques, and actionable remediation steps. Format key findings
with severity markers: [CRITICAL], [HIGH], [MEDIUM], [LOW], [INFO]."""

    def __init__(self):
        self.history  = []
        self.key_var  = None
        self.last_err = ""

    def _key(self):
        if self.key_var:
            k = self.key_var.get().strip()
            if k: return k
        return os.environ.get("ANTHROPIC_API_KEY","")

    def build_context(self, host_db, alerts, cap_stats, engine):
        lines = [f"=== RECONSHIELD v1.0 CONTEXT [{time.strftime('%H:%M:%S')}] ==="]
        lines.append(f"Hosts: {len(host_db)} | Packets: {cap_stats.get('total',0):,} | "
                     f"Alerts: {len(alerts)}")
        if host_db:
            lines.append("\nHOSTS:")
            for ip,h in list(host_db.items())[:20]:
                lines.append(f"  {ip:16s} {h.get('os','?'):20s} "
                              f"risk={h.get('risk','?'):8s} ports={len(h.get('ports',{}))}"
                              + (f" hn={h.get('hostname','')}" if h.get('hostname') else ""))
        if alerts:
            lines.append("\nLATEST ALERTS:")
            for a in alerts[-10:]:
                lines.append(f"  [{a.severity}] {a.rule} {a.src}→{a.dst}: {a.title}")
        lines.append(f"\nPROTOCOL STATS: " +
                     " | ".join(f"{k}={v}" for k,v in cap_stats.items()
                                if k not in ("total","bytes","error","iface")
                                and isinstance(v,int) and v>0)[:200])
        return "\n".join(lines)

    def ask(self, question, context="", on_chunk=None, on_done=None):
        def _run():
            key = self._key()
            if not key:
                if on_done: on_done("", "No API key set.")
                return
            msgs = []
            if context:
                msgs.append({"role":"user","content":
                             f"[Context]\n{context}\n\n{question}"})
            else:
                msgs.append({"role":"user","content":question})
            history_payload = self.history[-14:] + msgs
            body = json.dumps({
                "model": self.MODEL,
                "max_tokens": 2048,
                "stream": False,
                "system": self.SYSTEM,
                "messages": history_payload,
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=body,
                headers={"Content-Type":"application/json",
                         "x-api-key": key,
                         "anthropic-version":"2023-06-01"},
                method="POST")
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
                    text = data.get("content",[{}])[0].get("text","")
                    self.history.append({"role":"user","content":question})
                    self.history.append({"role":"assistant","content":text})
                    if len(self.history) > 20: self.history = self.history[-20:]
                    if on_done: on_done(text, "")
            except urllib.error.HTTPError as e:
                err = f"API Error {e.code}: {e.read().decode()[:200]}"
                if on_done: on_done("", err)
            except Exception as e:
                if on_done: on_done("", str(e))
        threading.Thread(target=_run, daemon=True).start()

# ═══════════════════════════════════════════════════════════════════
#  TAB 1: NETWORK RECON
# ═══════════════════════════════════════════════════════════════════
class ReconTab(tk.Frame):
    def __init__(self, nb, app):
        super().__init__(nb, bg=C["bg2"])
        self.app = app
        self._stop = threading.Event()
        self._build()

    def _build(self):
        hdr = SecHdr(self,
                     "🛰  Network Recon  —  Host Discovery  ·  Port Scanner  ·  Service Detection  ·  CVE Mapping",
                     C["cyan"],
                     sub="ICMP + TCP fallback  ·  Non-blocking batch scanner  ·  UDP probe  ·  Banner & version grab  ·  ARP + MAC vendor  ·  OS fingerprinting")
        if ROOT:
            tk.Label(hdr, text="  ✅ ADMIN / ROOT  ", bg=C["btn_g"],
                     fg=C["green"], font=("Segoe UI Semibold",9)).pack(side="right",padx=10)
        else:
            tk.Label(hdr, text="  ⚠ LIMITED — run as Admin/sudo for full features  ",
                     bg=C["btn_r"], fg=C["orange"],
                     font=("Segoe UI Semibold",9)).pack(side="right",padx=10)

        # ── Control bar ────────────────────────────────────────────
        cf = tk.Frame(self, bg=C["panel2"], pady=5); cf.pack(fill="x")
        r1 = tk.Frame(cf, bg=C["panel2"]); r1.pack(fill="x", padx=12, pady=2)

        Lbl(r1,"Target:",bg=C["panel2"],fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._tgt = tk.StringVar()
        te = tk.Entry(r1, textvariable=self._tgt,
                      bg=C["card"], fg=C["cyan"],
                      font=("Consolas",10), width=32,
                      relief="flat", insertbackground=C["cyan"],
                      highlightthickness=1, highlightbackground=C["border"])
        te.pack(side="left", padx=6)
        te.bind("<Return>", lambda _: self._start())
        # Placeholder hint
        Lbl(r1, "e.g.  192.168.1.1  ·  192.168.0.0/24  ·  scanme.nmap.org",
            bg=C["panel2"], fg=C["text_muted"],
            font=("Segoe UI",8,"italic")).pack(side="left", padx=(0,10))

        Lbl(r1,"Scan Mode:",bg=C["panel2"],fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left",padx=(8,4))
        self._mode = tk.StringVar(value="service")
        for lbl2,val,tip in [
            ("Quick","service","~220 known ports — fast"),
            ("Top 1000","top1000","ports 1–1024 + known"),
            ("Full Scan","full","all 65535 ports"),
        ]:
            f2 = tk.Frame(r1,bg=C["panel2"]); f2.pack(side="left",padx=3)
            tk.Radiobutton(f2, text=lbl2, variable=self._mode, value=val,
                           bg=C["panel2"], fg=C["text"],
                           selectcolor=C["card"],
                           activebackground=C["panel2"],
                           font=("Segoe UI Semibold",9)).pack()
            tk.Label(f2,text=tip,bg=C["panel2"],fg=C["text_muted"],
                     font=("Segoe UI",7)).pack()

        # Options row
        r1b = tk.Frame(cf,bg=C["panel2"]); r1b.pack(fill="x",padx=12,pady=(0,2))
        self._do_ports  = tk.BooleanVar(value=True)
        self._do_banner = tk.BooleanVar(value=True)
        self._do_udp    = tk.BooleanVar(value=False)
        self._do_vuln   = tk.BooleanVar(value=True)
        self._threads   = tk.IntVar(value=512)   # fixed internally, not exposed

        opts_frame = tk.Frame(r1b, bg=C["panel2"]); opts_frame.pack(side="left")
        for text2, var, tip2 in [
            ("Port Scan",    self._do_ports,  "TCP connect scan on all ports"),
            ("Banner Grab",  self._do_banner, "Grab service banners & versions"),
            ("UDP Probe",    self._do_udp,    "Probe common UDP services"),
            ("CVE Check",    self._do_vuln,   "Map open ports to CVE database"),
        ]:
            cb_frame = tk.Frame(opts_frame, bg=C["panel2"]); cb_frame.pack(side="left", padx=4)
            tk.Checkbutton(cb_frame, text=text2, variable=var,
                           bg=C["panel2"], fg=C["text"],
                           selectcolor=C["card"],
                           activebackground=C["panel2"],
                           font=("Segoe UI Semibold", 9)).pack()
            tk.Label(cb_frame, text=tip2, bg=C["panel2"], fg=C["text_muted"],
                     font=("Segoe UI", 7)).pack()

        # Buttons
        bf = tk.Frame(r1b,bg=C["panel2"]); bf.pack(side="right",padx=4)
        GBtn(bf,"▶  Start Scan",  self._start,  padx=16, pady=7).pack(side="left",padx=4)
        RBtn(bf,"■  Stop",        self._stop_scan, padx=12, pady=7).pack(side="left",padx=2)
        Btn(bf, "🗑  Clear",      self._clear,  padx=10, pady=7).pack(side="left",padx=2)
        Btn(bf, "💾  Export",     self._export, padx=10, pady=7).pack(side="left",padx=2)
        Btn(bf, "🌐  Topology",   self._topology, padx=10, pady=7).pack(side="left",padx=2)
        Btn(bf, "↺  Auto-Detect", self._auto_detect, padx=10, pady=7).pack(side="left",padx=2)
        Btn(bf, "⚡  Quick Ping", self._quick_ping, padx=10, pady=7).pack(side="left",padx=2)

        # ── Progress row ────────────────────────────────────────────
        r2 = tk.Frame(cf,bg=C["panel2"]); r2.pack(fill="x",padx=12,pady=(0,4))
        self._pbar = ttk.Progressbar(r2, mode="determinate",
                                     style="Horizontal.TProgressbar", length=340)
        self._pbar.pack(side="left",padx=(0,8))
        self._prog_lbl = tk.StringVar(value="Ready  —  enter a target IP, hostname, or CIDR range (e.g. 192.168.1.0/24)  then click ▶ Start Scan")
        tk.Label(r2,textvariable=self._prog_lbl,
                 bg=C["panel2"],fg=C["text_dim"],
                 font=("Segoe UI",8,"italic")).pack(side="left")

        # Stats strip
        self._sv = {}
        sf = tk.Frame(r2,bg=C["panel2"]); sf.pack(side="right")
        for key,label,col in [
            ("hosts","Hosts",    C["cyan"]),
            ("open", "TCP Open", C["green"]),
            ("udp",  "UDP Open", C["lime"]),
            ("crit", "Critical", C["red"]),
            ("high", "High",     C["orange"]),
            ("med",  "Medium",   C["yellow"]),
            ("time", "Scan Time",C["blue"]),
            ("speed","Ports/sec",C["purple"]),
        ]:
            f3 = tk.Frame(sf,bg=C["card"],padx=7,pady=2,
                         highlightbackground=col,highlightthickness=1)
            f3.pack(side="left",padx=2)
            v = tk.StringVar(value="—"); self._sv[key]=v
            tk.Label(f3,text=label,bg=C["card"],fg=C["text_dim"],
                     font=("Segoe UI",6,"bold")).pack()
            tk.Label(f3,textvariable=v,bg=C["card"],fg=col,
                     font=("Consolas",10,"bold")).pack()

        # ── Main pane ───────────────────────────────────────────────
        pane = tk.PanedWindow(self, orient="horizontal",
                              bg=C["bg"], sashwidth=5)
        pane.pack(fill="both", expand=True, padx=4, pady=4)

        # Left: host list  (wider, more cols)
        lf = tk.Frame(pane,bg=C["bg2"]); pane.add(lf, width=700)
        hcols = ["IP","Hostname","OS / Fingerprint","Hops","TTL","RTT","MAC","Vendor","TCP","UDP","Risk","Scanned"]
        hwids = [118,155,175,40,40,68,135,100,40,40,74,76]
        self._htree = make_tree(lf, hcols, hwids, height=22)
        for t,col in [("Critical",C["sev_c"]),("High",C["sev_h"]),
                       ("Medium",C["sev_m"]),("Low",C["sev_l"]),
                       ("Unknown",C["blue"]),("odd",C["text"]),("even",C["text_dim"])]:
            self._htree.tag_configure(t, foreground=col)
        self._htree.bind("<Double-1>", self._host_detail)
        self._htree.bind("<Button-3>", self._host_context_menu)

        # Right: tabs
        rf = tk.Frame(pane,bg=C["bg2"]); pane.add(rf)
        nb2 = ttk.Notebook(rf); nb2.pack(fill="both",expand=True)

        # Ports tab
        pf = tk.Frame(nb2,bg=C["bg2"]); nb2.add(pf,text="  🔌 Ports & Services  ")
        pcols = ["Port","Proto","Service","Version","State","Risk","Banner","CVE Refs"]
        pwids = [55,45,110,120,55,72,220,280]
        self._ptree = make_tree(pf, pcols, pwids, height=18)
        for t,col in [("Critical",C["sev_c"]),("High",C["sev_h"]),
                       ("Medium",C["sev_m"]),("Low",C["sev_l"])]:
            self._ptree.tag_configure(t, foreground=col)
        self._ptree.bind("<Double-1>", self._port_detail)

        # Vuln summary tab
        vf = tk.Frame(nb2,bg=C["bg2"]); nb2.add(vf,text="  🛡 Vuln Summary  ")
        self._vuln_txt = scrolledtext.ScrolledText(
            vf,bg=C["bg"],fg=C["orange"],font=("Consolas",8),
            state="disabled",relief="flat",wrap="word")
        self._vuln_txt.pack(fill="both",expand=True,padx=4,pady=4)
        for t2,c2 in [("crit",C["red"]),("high",C["orange"]),
                       ("med",C["yellow"]),("low",C["green"]),
                       ("info",C["cyan"]),("hdr",C["cyan"]),
                       ("dim",C["text_dim"]),("url",C["blue"])]:
            self._vuln_txt.tag_config(t2,foreground=c2,
                font=("Consolas",8))

        # Scan Log tab
        lf2 = tk.Frame(nb2,bg=C["bg2"]); nb2.add(lf2,text="  📋 Scan Log  ")
        self._log = scrolledtext.ScrolledText(
            lf2,bg=C["bg"],fg=C["text_dim"],
            font=("Consolas",8),relief="flat",
            state="disabled",wrap="word")
        self._log.pack(fill="both",expand=True,padx=4,pady=4)
        for t3,c3 in [("err",C["red"]),("ok",C["green"]),
                       ("info",C["cyan"]),("warn",C["yellow"]),
                       ("phase",C["purple"])]:
            self._log.tag_config(t3,foreground=c3)

    def _auto_detect(self):
        ip = get_local_ip()
        base = ".".join(ip.split(".")[:3])
        self._tgt.set(f"{base}.0/24")
        self._log_w(f"Auto-detected subnet: {base}.0/24", "info")

    def _quick_ping(self):
        """Ping a single host instantly and show result in a small popup."""
        target = self._tgt.get().strip()
        if not target:
            messagebox.showwarning("No target", "Enter an IP or hostname first")
            return
        # Resolve hostname if needed
        ip = target.split("/")[0]
        self._log_w(f"Quick ping → {ip} …", "info")

        def _run():
            try:
                resolved = socket.gethostbyname(ip)
            except Exception:
                resolved = ip
            alive, rtt, ttl = icmp_ping(resolved, timeout=1.5)
            if not alive:
                alive = _tcp_probe(resolved)
                rtt = None; ttl = None
            os_g = ttl_os(ttl) if ttl else "?"
            if alive:
                msg  = (f"✅  {resolved}  is ALIVE\n\n"
                        f"RTT:  {rtt:.1f} ms" if rtt else
                        f"✅  {resolved}  is ALIVE\n\nRTT:  via TCP probe")
                msg += f"\nTTL:  {ttl}" if ttl else ""
                msg += f"\nOS :  {os_g}" if ttl else ""
                tag  = "ok"
            else:
                msg = f"❌  {resolved}  is UNREACHABLE\n\nNo ICMP reply and no TCP response."
                tag = "err"
            self.after(0, lambda: (
                self._log_w(f"Ping {resolved}: {'ALIVE' if alive else 'DEAD'}"
                            + (f" rtt={rtt:.1f}ms ttl={ttl}" if rtt else ""), tag),
                messagebox.showinfo("Quick Ping Result", msg)
            ))

        threading.Thread(target=_run, daemon=True).start()

    def _log_w(self, msg, tag="info"):
        self._log.configure(state="normal")
        ts = time.strftime("%H:%M:%S")
        self._log.insert("end", f"[{ts}] {msg}\n", tag)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear(self):
        self._htree.delete(*self._htree.get_children())
        self._ptree.delete(*self._ptree.get_children())
        self.app.host_db.clear()
        for v in self._sv.values(): v.set("—")
        self._prog_lbl.set("Cleared")
        self._pbar["value"] = 0
        self._log_w("Scan data cleared.", "info")

    def _stop_scan(self):
        self._stop.set()
        self._pbar.stop()
        self._prog_lbl.set("⏹  Stopped")

    def _start(self):
        self._stop.clear(); self._clear()
        target = self._tgt.get().strip()
        if not target:
            messagebox.showwarning("No target", "Enter an IP, hostname, or CIDR range")
            return
        self._scan_t0 = time.time()
        self._pbar.configure(mode="indeterminate")
        self._pbar.start(10)
        self._prog_lbl.set(f"Phase 1 — Discovering hosts in {target} …")
        self.app.status.set(f"🛰 Scanning {target}")
        self._log_w(f"═══ Scan started ═══  target={target}  mode={self._mode.get()}", "info")
        threading.Thread(target=self._do_scan, args=(target,), daemon=True).start()

    def _do_scan(self, target):
        # ── Phase 1: Host discovery ────────────────────────────────────
        phase1_t0 = time.time()

        def disc_cb(done, total, found):
            pct = int(done / max(total, 1) * 100)
            self.after(0, lambda: (
                self._prog_lbl.set(f"Phase 1 — Probing {done}/{total}  |  {found} alive  |  {pct}%"),
                self._pbar.configure(mode="determinate", value=pct),
            ))

        hosts = subnet_scan(target, stop_ev=self._stop, cb=disc_cb)
        phase1_elapsed = time.time() - phase1_t0
        n = len(hosts)
        self.after(0, lambda: self._log_w(
            f"Phase 1 done in {phase1_elapsed:.1f}s — {n} live hosts found", "ok"))

        if not hosts or self._stop.is_set():
            self.after(0, self._done)
            return

        # Add all hosts to db immediately (shows them with Unknown risk)
        for ip, h in hosts.items():
            self.app.host_db[ip] = h
            self.after(0, lambda ih=h: self._insert_host(ih))

        if not self._do_ports.get():
            self.after(0, self._done)
            return

        # ── Phase 2: Parallel port scan ALL hosts simultaneously ───────
        phase2_t0 = time.time()
        self.after(0, lambda: (
            self._pbar.configure(mode="determinate", value=0),
            self._prog_lbl.set(f"Phase 2 — Port scanning {n} hosts in PARALLEL …"),
            self._log_w(f"Phase 2 — parallel port scan  mode={self._mode.get()}  hosts={n}", "info"),
        ))

        def port_progress(done, total, ip):
            pct = int(done / max(total, 1) * 100)
            elapsed = time.time() - phase2_t0
            rate = done / max(elapsed, 0.1)
            eta  = (total - done) / max(rate, 0.01)
            self.after(0, lambda: (
                self._pbar.configure(value=pct),
                self._prog_lbl.set(
                    f"Phase 2 — {done}/{total} hosts  |  {pct}%  |  "
                    f"elapsed {elapsed:.0f}s  |  ETA {eta:.0f}s"),
            ))

        def port_result(ip, ports):
            if self._stop.is_set(): return
            h = self.app.host_db.get(ip)
            if not h: return
            h["ports"] = ports
            h["risk"]  = classify_risk(ports)
            # Update existing tree row
            self.after(0, lambda hip=ip, hh=h: self._update_host_row(hip, hh))
            p_count = len(ports)
            risk_str = h["risk"]
            self.after(0, lambda: self._log_w(
                f"  {ip:<16}  {p_count:3d} open ports  risk={risk_str}", "ok"))
            # ── Async CVE fetch for every open port (if CVE Check enabled) ──
            if self._do_vuln.get():
                for pnum, info_d in ports.items():
                    def _cve_done(p, res, _ip=ip, _port=pnum, _info=info_d):
                        _info["cve_list"] = res
                        _info["cve"]      = format_cve_summary(res, 4)
                        live_count = sum(1 for c in res
                                         if c.get("source") in ("Exploit-DB","NVD")
                                         and not c.get("error"))
                        self.after(0, lambda: self._log_w(
                            f"  {_ip}:{p}  {_info.get('service','')}  "
                            f"→ {live_count} live CVEs", "info"))
                    fetch_cves_async(
                        pnum,
                        service=info_d.get("service",""),
                        banner=info_d.get("banner",""),
                        version=info_d.get("version",""),
                        callback=_cve_done,
                    )

        parallel_port_scan(
            hosts,
            port_range=self._mode.get(),
            stop_ev=self._stop,
            progress_cb=port_progress,
            result_cb=port_result,
        )

        self.after(0, self._done)

    def _update_host_row(self, ip, h):
        """Update existing tree row for a host after port scan completes."""
        pd   = h.get("ports", {})
        risk = h.get("risk", "?")
        rtt  = f"{h['rtt']:.1f}ms" if h.get("rtt") else "—"
        tmap = {"Critical": "Critical", "High": "High",
                "Medium": "Medium", "Low": "Low"}
        tag  = tmap.get(risk, "odd")
        # Find and update or re-insert
        for iid in self._htree.get_children():
            if self._htree.item(iid, "values")[0] == ip:
                self._htree.item(iid, values=(
                    ip,
                    (h.get("hostname") or "")[:30],
                    h.get("os", "?"),
                    h.get("ttl", "—"),
                    rtt,
                    (h.get("mac") or "")[:17],
                    h.get("vendor", ""),
                    len(pd),
                    risk,
                ), tags=(tag,))
                break
        self._update_stats()

    def _insert_host(self, h):
        pd   = h.get("ports", {})
        risk = h.get("risk", "?")
        tmap = {"Critical":"Critical","High":"High","Medium":"Medium","Low":"Low"}
        tag  = tmap.get(risk, "")
        if not tag:
            n   = len(self._htree.get_children())
            tag = "even" if n%2 == 0 else "odd"
        rtt  = f"{h['rtt']:.1f}ms" if h.get("rtt") else "—"
        self._htree.insert("", "end", values=(
            h["ip"],
            (h.get("hostname") or "")[:30],
            h.get("os","?"),
            h.get("ttl","—"),
            rtt,
            (h.get("mac") or "")[:17],
            h.get("vendor",""),
            len(pd),
            risk,
        ), tags=(tag,))
        self._update_stats()

    def _update_stats(self):
        items = self._htree.get_children()
        n = len(items)
        risks = [self._htree.item(i,"values")[8] for i in items]
        lats  = []
        op    = 0
        for ip, h in self.app.host_db.items():
            if h.get("rtt"): lats.append(h["rtt"])
            op += len(h.get("ports",{}))
        self._sv["hosts"].set(str(n))
        self._sv["open"].set(str(op))
        self._sv["crit"].set(str(risks.count("Critical")))
        self._sv["high"].set(str(risks.count("High")))
        self._sv["med"].set(str(risks.count("Medium")))
        self._sv["rtt"].set(f"{sum(lats)/len(lats):.0f}ms" if lats else "—")

    def _host_detail(self, event):
        sel = self._htree.selection()
        if not sel: return
        ip = self._htree.item(sel[0],"values")[0]
        h  = self.app.host_db.get(ip)
        if not h: return
        self._ptree.delete(*self._ptree.get_children())
        for port, info in sorted(h.get("ports",{}).items()):
            risk  = info.get("risk","?")
            clist = info.get("cve_list", [])
            # Build CVE refs string: prefer live data, fall back to static
            if clist:
                top_cves = [c.get("cve_id") or f"EDB-{c.get('edb_id','')}"
                            for c in clist if not c.get("error")][:4]
                cve_ref = ", ".join(filter(None, top_cves)) or info.get("cve","")[:80]
            else:
                cve_ref = info.get("cve","")[:80]
            self._ptree.insert("","end",
                values=(port,
                        info.get("protocol","tcp").upper(),
                        info.get("service","?"),
                        (info.get("version") or "")[:22],
                        info.get("state","open"),
                        risk,
                        (info.get("banner") or "")[:100],
                        cve_ref),
                tags=(risk,))
        self._show_host_popup(ip, h)

    def _show_host_popup(self, ip, h):
        w = tk.Toplevel(self.app); w.title(f"Host  {ip}")
        w.configure(bg=C["bg"]); w.geometry("960x700")
        risk = h.get("risk","Unknown")
        rc   = {"Critical":C["sev_c"],"High":C["sev_h"],
                "Medium":C["sev_m"],"Low":C["sev_l"],
                "Unknown":C["blue"]}.get(risk, C["blue"])
        tk.Frame(w, bg=rc, height=4).pack(fill="x")
        hf = tk.Frame(w, bg=C["panel"]); hf.pack(fill="x")
        tk.Label(hf, text=f"  🖥  {ip}",
                 bg=C["panel"], fg=rc,
                 font=("Segoe UI Semibold",14)).pack(side="left", padx=12, pady=8)
        tk.Label(hf, text=f"{h.get('hostname','—')}  |  {h.get('os','?')}  |  "
                           f"MAC: {h.get('mac','?')}  |  Risk: {risk}",
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI",9)).pack(side="left")

        nb2 = ttk.Notebook(w); nb2.pack(fill="both", expand=True, padx=6, pady=4)

        # Overview tab
        ov = tk.Frame(nb2, bg=C["bg2"]); nb2.add(ov, text="  Overview  ")
        fields = [
            ("IP Address", h["ip"]),
            ("Hostname",   h.get("hostname") or "N/A"),
            ("OS Guess",   h.get("os","?")),
            ("TTL",        str(h.get("ttl","?"))),
            ("RTT",        f"{h['rtt']:.1f}ms" if h.get("rtt") else "N/A"),
            ("MAC",        h.get("mac") or "N/A"),
            ("Vendor",     h.get("vendor","N/A")),
            ("Open Ports", str(len(h.get("ports",{})))),
            ("Risk Level", risk),
        ]
        for i,(k,v) in enumerate(fields):
            bg2 = C["card"] if i%2==0 else C["card2"]
            f2  = tk.Frame(ov, bg=bg2); f2.pack(fill="x")
            tk.Label(f2, text=f"  {k}", bg=bg2, fg=C["text_dim"],
                     width=18, anchor="w",
                     font=("Segoe UI Semibold",10)).pack(side="left", pady=6)
            vc  = rc if k=="Risk Level" else C["text_hi"]
            tk.Label(f2, text=v, bg=bg2, fg=vc,
                     font=("Consolas",10)).pack(side="left", padx=12)

        # Ports tab — with live CVE data
        pf2 = tk.Frame(nb2, bg=C["bg2"]); nb2.add(pf2, text="  Ports & CVEs  ")
        pt2 = make_tree(pf2,
                        ["Port","Service","Ver","Risk","Banner","CVE Count","Top CVE"],
                        [60, 110, 90, 70, 200, 80, 360], height=14)
        for t, c in [("Critical",C["sev_c"]),("High",C["sev_h"]),
                      ("Medium",C["sev_m"]),("Low",C["sev_l"])]:
            pt2.tag_configure(t, foreground=c)
        for port, info in sorted(h.get("ports",{}).items()):
            rsk   = info.get("risk","?")
            clist = info.get("cve_list", [])
            top   = ""
            if clist:
                for c2 in clist:
                    if not c2.get("error"):
                        top = f"[{c2.get('severity','?')}] {c2.get('cve_id') or c2.get('edb_id','')} — {c2.get('title','')[:60]}"
                        break
            elif info.get("cve"):
                top = info["cve"][:120]
            pt2.insert("","end", values=(
                port, info.get("service","?"),
                (info.get("version") or "")[:20],
                rsk,
                (info.get("banner") or "")[:100],
                len(clist) if clist else ("?" if info.get("cve") else "0"),
                top[:120],
            ), tags=(rsk,))

        # ── Live CVE detail panel ────────────────────────────────────
        cve_frame = tk.Frame(pf2, bg=C["bg2"]); cve_frame.pack(fill="both", expand=True, padx=4, pady=4)

        cve_hdr = tk.Frame(cve_frame, bg=C["panel2"]); cve_hdr.pack(fill="x")
        tk.Label(cve_hdr, text="  🔴  Live CVE / Exploit Details  (Exploit-DB + NVD)",
                 bg=C["panel2"], fg=C["red"],
                 font=("Segoe UI Semibold",10)).pack(side="left", padx=8, pady=5)
        cve_status_var = tk.StringVar(value="Select a port above to view live CVEs")
        tk.Label(cve_hdr, textvariable=cve_status_var,
                 bg=C["panel2"], fg=C["text_dim"],
                 font=("Segoe UI",8)).pack(side="right", padx=8)

        cve_txt = scrolledtext.ScrolledText(
            cve_frame, bg=C["bg"], fg=C["text"],
            font=("Consolas", 9), relief="flat", wrap="word", height=10)
        cve_txt.pack(fill="both", expand=True, padx=2, pady=2)
        for tag2, col2 in [
            ("crit", C["red"]),("high", C["orange"]),("med", C["yellow"]),
            ("low",  C["lime"]),("hdr",  C["cyan"]),("dim",  C["text_dim"]),
            ("edb",  C["purple"]),("nvd", C["blue"]),
            ("url",  C["cyan"]),("ok",  C["green"]),("title", C["text_hi"]),
        ]:
            cve_txt.tag_config(tag2, foreground=col2)

        def _render_cves(port_n, info_d, cve_list):
            """Render CVE list into the scrolled text widget — live Exploit-DB + NVD only."""
            cve_txt.configure(state="normal")
            cve_txt.delete("1.0","end")
            svc_n = info_d.get("service","?")
            ver_n = info_d.get("version","")
            ban_n = (info_d.get("banner") or "")[:120]
            cve_txt.insert("end",
                f"\n  ╔═ PORT {port_n}  ·  {svc_n}"
                + (f"  ·  {ver_n}" if ver_n else "")
                + f"  ══════════════════════════════════╗\n","hdr")
            cve_txt.insert("end",
                f"  ║  Source: 🔴 exploit-db.com  +  🔵 NVD (NIST)  —  100% live data\n","dim")
            if ban_n:
                cve_txt.insert("end", f"  ║  Banner: {ban_n}\n","dim")
            cve_txt.insert("end","  ╚════════════════════════════════════════════════════════╝\n\n","hdr")

            if not cve_list:
                cve_txt.insert("end","  ⏳ Fetching live data from exploit-db.com and NVD…\n","dim")
                cve_txt.configure(state="disabled"); return

            edb_entries = [c for c in cve_list if c.get("source")=="Exploit-DB" and not c.get("error")]
            nvd_entries = [c for c in cve_list if c.get("source")=="NVD"        and not c.get("error")]
            errors      = [c for c in cve_list if c.get("error")]

            # ── Exploit-DB entries ──
            if edb_entries:
                cve_txt.insert("end",
                    f"  ┌─ 🔴 Exploit-DB  ({len(edb_entries)} exploits found)  "
                    f"https://www.exploit-db.com ─────────\n","edb")
                for e in edb_entries:
                    sev  = e.get("severity","?")
                    stag = {"CRITICAL":"crit","HIGH":"high","MEDIUM":"med","LOW":"low"}.get(sev,"dim")
                    eid  = e.get("edb_id","")
                    cid  = e.get("cve_id","")
                    etype= e.get("type","")
                    plat = e.get("platform","")
                    date = e.get("date","")
                    cve_txt.insert("end", f"  │  [{sev}] ", stag)
                    cve_txt.insert("end", f"EDB-{eid}", "edb")
                    if cid: cve_txt.insert("end", f"  {cid}", "nvd")
                    cve_txt.insert("end", f"  {e.get('title','')}\n","title")
                    meta = "  ".join(filter(None, [date, etype, plat]))
                    if meta:
                        cve_txt.insert("end", f"  │     {meta}\n","dim")
                    cve_txt.insert("end", f"  │     🔗 {e.get('url','')}\n","url")
                cve_txt.insert("end","  └──────────────────────────────────────────────────────────\n","edb")

            # ── NVD entries ──
            if nvd_entries:
                cve_txt.insert("end",
                    f"\n  ┌─ 🔵 NVD / NIST  ({len(nvd_entries)} CVEs)  "
                    f"https://nvd.nist.gov ─────────────────\n","nvd")
                for e in nvd_entries:
                    sev  = e.get("severity","?")
                    stag = {"CRITICAL":"crit","HIGH":"high","MEDIUM":"med","LOW":"low"}.get(sev,"dim")
                    cid  = e.get("cve_id","")
                    cvss = e.get("cvss","?")
                    pub  = e.get("published","")
                    cve_txt.insert("end", f"  │  [{sev}]", stag)
                    cve_txt.insert("end", f"  CVSS:{cvss}  ", "nvd")
                    cve_txt.insert("end", f"{cid}","title")
                    cve_txt.insert("end", f"  Published: {pub}\n","dim")
                    cve_txt.insert("end", f"  │     {e.get('title','')}\n","dim")
                    cve_txt.insert("end", f"  │     🔗 {e.get('url','')}\n","url")
                cve_txt.insert("end","  └──────────────────────────────────────────────────────────\n","nvd")

            if not edb_entries and not nvd_entries:
                cve_txt.insert("end",
                    "  No results returned from Exploit-DB or NVD.\n"
                    "  This may mean the service is not commonly exploited,\n"
                    "  or the internet connection is unavailable.\n\n","dim")
                cve_txt.insert("end",
                    f"  Manual search: https://www.exploit-db.com/search?q={svc_n}\n","url")

            # ── Errors ──
            for e in errors:
                cve_txt.insert("end",
                    f"\n  ⚠  {e.get('source','?')} error: {e.get('error','')}\n","high")

            cve_txt.configure(state="disabled")

        def _on_port_select(event):
            sel = pt2.selection()
            if not sel: return
            vals = pt2.item(sel[0],"values")
            try:
                pnum = int(vals[0])
            except: return
            info_d = h.get("ports",{}).get(pnum,{})
            clist  = info_d.get("cve_list")
            if clist is not None:
                cve_status_var.set(f"Showing {len(clist)} results for port {pnum}")
                _render_cves(pnum, info_d, clist)
            else:
                # Not yet fetched — fetch now
                cve_status_var.set(f"⏳ Fetching live CVEs for port {pnum} …")
                cve_txt.configure(state="normal")
                cve_txt.delete("1.0","end")
                cve_txt.insert("end",f"\n  Fetching Exploit-DB + NVD data for port {pnum} ({info_d.get('service','?')})…\n","dim")
                cve_txt.configure(state="disabled")
                def _cb(p, res, _id=pnum, _info=info_d):
                    info_d["cve_list"] = res
                    info_d["cve"]      = format_cve_summary(res, 4)
                    try:
                        w.after(0, lambda: (
                            cve_status_var.set(f"✅ {len(res)} results for port {_id}"),
                            _render_cves(_id, _info, res),
                        ))
                    except Exception: pass
                fetch_cves_async(pnum,
                                  service=info_d.get("service",""),
                                  banner=info_d.get("banner",""),
                                  version=info_d.get("version",""),
                                  callback=_cb)

        pt2.bind("<<TreeviewSelect>>", _on_port_select)

        def _refresh_all_cves():
            """Re-fetch CVEs for all open ports of this host."""
            ports_list = sorted(h.get("ports",{}).keys())
            cve_status_var.set(f"⏳ Refreshing CVEs for {len(ports_list)} ports …")
            fetched = [0]
            for pnum in ports_list:
                info_d = h["ports"][pnum]
                def _cb(p, res, _id=pnum, _info=info_d):
                    _info["cve_list"] = res
                    _info["cve"]      = format_cve_summary(res, 4)
                    fetched[0] += 1
                    try:
                        w.after(0, lambda: cve_status_var.set(
                            f"✅ {fetched[0]}/{len(ports_list)} ports refreshed"))
                    except: pass
                # Force re-fetch by clearing cache
                cache_key = f"{pnum}:{info_d.get('service','')}:{(info_d.get('version') or '')[:20]}"
                with _CVE_LOCK:
                    _CVE_CACHE.pop(cache_key, None)
                fetch_cves_async(pnum,
                                  service=info_d.get("service",""),
                                  banner=info_d.get("banner",""),
                                  version=info_d.get("version",""),
                                  callback=_cb)

        Btn(cve_hdr, "⟳  Refresh All CVEs", _refresh_all_cves,
            bg=C["btn_r"], fg=C["red"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="right", padx=4)
        Btn(cve_hdr, "🌐  Open Exploit-DB",
            lambda: __import__("webbrowser").open("https://www.exploit-db.com/"),
            bg=C["btn_b"], fg=C["blue"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="right", padx=2)

        cve_txt.configure(state="normal")
        cve_txt.insert("end",
            "\n  🔴 Live CVE database powered by:\n"
            "     • Exploit-DB   (https://www.exploit-db.com)\n"
            "     • NVD / NIST   (https://nvd.nist.gov)\n\n"
            "  ✅ No static CVE data — all results fetched LIVE from Exploit-DB.\n\n"
            "  Select a port in the table above to load live CVE data.\n"
            "  Click ⟳ Refresh All CVEs to prefetch all open ports.\n\n"
            "  Results include: EDB-ID, CVE-ID, CVSS score, severity, publish date, direct links.\n","dim")
        cve_txt.configure(state="disabled")

        # Raw JSON tab
        jf = tk.Frame(nb2, bg=C["bg2"]); nb2.add(jf, text="  Raw JSON  ")
        jt = scrolledtext.ScrolledText(jf, bg=C["bg"], fg=C["green"],
                                       font=("Consolas",9), relief="flat")
        jt.pack(fill="both", expand=True, padx=4, pady=4)
        jt.insert("end", json.dumps(h, indent=2, default=str))
        jt.configure(state="disabled")

        bf = tk.Frame(w, bg=C["bg"]); bf.pack(fill="x", pady=6)
        Btn(bf, "🤖  Ask AI Analyst",
            lambda: self._ask_ai_host(ip, h, w),
            bg=C["btn_g"], fg=C["green"]).pack(side="left", padx=10)
        Btn(bf, "Close", w.destroy,
            bg=C["btn_r"], fg=C["red"]).pack(side="right", padx=10)

    def _ask_ai_host(self, ip, h, parent=None):
        self.app.nb.select(self.app.tab_ai)
        q = (f"Analyse host {ip}:\n"
             f"OS: {h.get('os','?')}  MAC: {h.get('mac','?')}  "
             f"Vendor: {h.get('vendor','?')}\n"
             f"Risk: {h.get('risk','?')}\n"
             f"Open ports: {json.dumps(h.get('ports',{}), default=str)[:1000]}\n\n"
             f"Provide full vulnerability analysis, MITRE ATT&CK mapping, "
             f"and prioritised remediation plan.")
        ctx = self.app.ai.build_context(self.app.host_db,
              self.app.engine.get_alerts(20), self.app.cap_stats, self.app.engine)
        self.app.tab_ai._send(q, ctx)
        if parent: parent.destroy()

    def _done(self):
        n = len(self._htree.get_children())
        self._prog_lbl.set(f"✓ Scan complete — {n} hosts  |  CVE fetch running …")
        self._pbar.stop(); self._pbar["value"] = 100
        self.app.status.set(f"✓ Scan complete: {n} hosts — fetching live CVEs")
        self._log_w(f"Scan finished. {n} hosts discovered. Fetching live CVEs …", "ok")
        # Populate the Vuln Summary tab after a short delay to let CVE threads run
        self.after(4000, self._build_vuln_summary)

    def _build_vuln_summary(self):
        """Write a live CVE vulnerability summary into the Vuln Summary tab."""
        vt = self._vuln_txt
        vt.configure(state="normal")
        vt.delete("1.0","end")
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        vt.insert("end",
            f"╔══════════════════════════════════════════════════════════════╗\n"
            f"║  LIVE CVE VULNERABILITY REPORT  ·  {ts}  ║\n"
            f"║  Sources: 🔴 Exploit-DB  +  🔵 NVD/NIST  (100% live data)  ║\n"
            f"╚══════════════════════════════════════════════════════════════╝\n\n",
            "hdr")
        total_cves = 0; total_exploits = 0
        for ip, h in sorted(self.app.host_db.items()):
            ports = h.get("ports",{})
            if not ports: continue
            risk = h.get("risk","?")
            rtag = {"Critical":"crit","High":"high","Medium":"med","Low":"low"}.get(risk,"low")
            vt.insert("end", f"  🖥  {ip}  ", rtag)
            vt.insert("end",
                f"  {h.get('hostname','—')}  ·  {h.get('os','?')}  ·  Risk: {risk}  ·  {len(ports)} ports\n",
                "dim")
            vt.insert("end","  " + "─"*70 + "\n","dim")
            for port, info in sorted(ports.items()):
                clist = info.get("cve_list",[])
                svc   = info.get("service","?")
                ver   = info.get("version","")
                live  = [c for c in clist if c.get("source") in ("Exploit-DB","NVD") and not c.get("error")]
                total_cves    += len([c for c in clist if c.get("cve_id")])
                total_exploits+= len([c for c in clist if c.get("edb_id")])
                prisk = info.get("risk","Low")
                ptag  = {"Critical":"crit","High":"high","Medium":"med","Low":"low"}.get(prisk,"low")
                vt.insert("end", f"    [{prisk:8s}] Port {port:5d}  {svc}", ptag)
                if ver: vt.insert("end", f"  ({ver})","dim")
                vt.insert("end", f"  — {len(live)} CVEs live (Exploit-DB + NVD)\n","dim")
                for c in live[:4]:
                    sev  = c.get("severity","?")
                    stag = {"CRITICAL":"crit","HIGH":"high","MEDIUM":"med","LOW":"low"}.get(sev,"dim")
                    cid  = c.get("cve_id") or f"EDB-{c.get('edb_id','')}"
                    vt.insert("end", f"         [{sev}] ","dim")
                    vt.insert("end", cid, stag)
                    vt.insert("end", f"  {c.get('title','')[:80]}\n","dim")
                    vt.insert("end", f"         🔗 {c.get('url','')}\n","url")
                if len(live) > 4:
                    vt.insert("end", f"         … +{len(live)-4} more — open host detail for full list\n","dim")
            vt.insert("end","\n","dim")

        vt.insert("end",
            f"\n  ══ SUMMARY ══════════════════════════════════════════════════\n"
            f"  Hosts scanned    : {len(self.app.host_db)}\n"
            f"  Total CVE IDs    : {total_cves}\n"
            f"  Total Exploits   : {total_exploits}\n"
            f"  Data from        : Exploit-DB (exploit-db.com) + NVD (nvd.nist.gov)\n"
            f"  Refresh          : Re-scan or open host detail → Refresh All CVEs\n"
            f"  ══════════════════════════════════════════════════════════════\n",
            "hdr")
        vt.configure(state="disabled")
        self._prog_lbl.set(f"✓ Scan complete — {len(self.app.host_db)} hosts  |  {total_cves} CVEs found")
        self.app.status.set(f"✓ Done: {len(self.app.host_db)} hosts, {total_cves} live CVEs")

    def _export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON","*.json"),("CSV","*.csv")])
        if not path: return
        if path.endswith(".csv"):
            import csv
            with open(path,"w",newline="") as f:
                w2 = csv.writer(f)
                w2.writerow(["IP","Hostname","OS","TTL","RTT","MAC",
                              "Vendor","OpenPorts","Risk"])
                for ip, h in self.app.host_db.items():
                    w2.writerow([ip, h.get("hostname",""),
                                 h.get("os",""), h.get("ttl",""),
                                 h.get("rtt",""), h.get("mac",""),
                                 h.get("vendor",""),
                                 len(h.get("ports",{})), h.get("risk","")])
        else:
            with open(path,"w") as f:
                json.dump(self.app.host_db, f, indent=2, default=str)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def _host_context_menu(self, event):
        """Right-click context menu on host tree row."""
        row = self._htree.identify_row(event.y)
        if not row: return
        self._htree.selection_set(row)
        ip = self._htree.item(row, "values")[0]
        h  = self.app.host_db.get(ip, {})

        menu = tk.Menu(self, tearoff=0,
                       bg=C["card"], fg=C["text_hi"],
                       activebackground=C["tsel"],
                       activeforeground=C["cyan"],
                       font=("Segoe UI", 9))
        menu.add_command(label=f"  🖥  {ip}  —  {h.get('hostname','?')}",
                         state="disabled")
        menu.add_separator()
        menu.add_command(label="  📋  View Full Detail",
                         command=lambda: self._show_host_popup(ip, h))
        menu.add_command(label="  🔌  Show Ports",
                         command=lambda: self._host_detail(None))
        menu.add_command(label="  ⚡  Quick Ping",
                         command=lambda: self._ping_host(ip))
        menu.add_command(label="  🔍  Re-scan Ports",
                         command=lambda: self._rescan_host(ip, h))
        menu.add_separator()
        menu.add_command(label="  🤖  Ask AI Analyst",
                         command=lambda: self._ask_ai_host(ip, h))
        menu.add_separator()
        menu.add_command(label="  📋  Copy IP",
                         command=lambda: (self.clipboard_clear(),
                                          self.clipboard_append(ip)))
        menu.tk_popup(event.x_root, event.y_root)

    def _ping_host(self, ip):
        """Background ping with result in log."""
        self._log_w(f"Pinging {ip} …", "info")
        def _run():
            alive, rtt, ttl = icmp_ping(ip, timeout=1.5)
            if not alive: alive = _tcp_probe(ip)
            msg = (f"ALIVE  rtt={rtt:.1f}ms  ttl={ttl}  os={ttl_os(ttl)}"
                   if alive else "UNREACHABLE")
            self.after(0, lambda: self._log_w(f"Ping {ip}: {msg}",
                                               "ok" if alive else "err"))
        threading.Thread(target=_run, daemon=True).start()

    def _rescan_host(self, ip, h):
        """Re-scan ports for a single already-discovered host, then fetch live CVEs."""
        self._log_w(f"Re-scanning {ip} …", "info")
        def _run():
            ports = scan_ports(ip, port_range=self._mode.get())
            h["ports"] = ports
            h["risk"]  = classify_risk(ports)
            self.app.host_db[ip] = h
            self.after(0, lambda: (
                self._update_host_row(ip, h),
                self._log_w(f"Re-scan {ip}: {len(ports)} ports  risk={h['risk']}", "ok"),
            ))
            # Fetch live CVEs for all newly-found ports
            for pnum, info_d in ports.items():
                # Clear stale cache entry so we get fresh data
                cache_key = f"{pnum}:{info_d.get('service','')}:{(info_d.get('version') or '')[:20]}"
                with _CVE_LOCK:
                    _CVE_CACHE.pop(cache_key, None)
                def _cve_done(p, res, _info=info_d):
                    _info["cve_list"] = res
                    _info["cve"]      = format_cve_summary(res, 4)
                fetch_cves_async(pnum,
                                  service=info_d.get("service",""),
                                  banner=info_d.get("banner",""),
                                  version=info_d.get("version",""),
                                  callback=_cve_done)
        threading.Thread(target=_run, daemon=True).start()

    def _port_detail(self, event):
        """Double-click on a port row → show full port detail popup."""
        sel = self._ptree.selection()
        if not sel: return
        vals = self._ptree.item(sel[0], "values")
        if not vals: return
        port    = vals[0]
        service = vals[2] if len(vals) > 2 else ""
        version = vals[3] if len(vals) > 3 else ""
        risk    = vals[5] if len(vals) > 5 else ""
        banner  = vals[6] if len(vals) > 6 else ""
        cve     = vals[7] if len(vals) > 7 else ""

        w = tk.Toplevel(self.app)
        w.title(f"Port {port}  —  {service}")
        w.configure(bg=C["bg"]); w.geometry("780x520")
        rc = {"Critical":C["sev_c"],"High":C["sev_h"],
              "Medium":C["sev_m"],"Low":C["sev_l"]}.get(risk, C["blue"])
        tk.Frame(w, bg=rc, height=4).pack(fill="x")
        tk.Label(w, text=f"  🔌  Port {port}  /  {service}  /  {risk}",
                 bg=C["panel"], fg=rc,
                 font=("Segoe UI Semibold", 13)).pack(fill="x", pady=6)

        nb2 = ttk.Notebook(w); nb2.pack(fill="both", expand=True, padx=6, pady=4)

        # Overview
        of = tk.Frame(nb2, bg=C["bg2"]); nb2.add(of, text="  Overview  ")
        fields = [("Port",    str(port)),
                  ("Service", service),
                  ("Version", version or "—"),
                  ("Risk",    risk),
                  ("State",   "open")]
        for i,(k,v) in enumerate(fields):
            bg2 = C["card"] if i%2==0 else C["card2"]
            ff  = tk.Frame(of, bg=bg2); ff.pack(fill="x")
            tk.Label(ff, text=f"  {k}", bg=bg2, fg=C["text_dim"],
                     width=16, anchor="w",
                     font=("Segoe UI Semibold",10)).pack(side="left", pady=5)
            tk.Label(ff, text=v, bg=bg2, fg=rc if k=="Risk" else C["text_hi"],
                     font=("Consolas",10)).pack(side="left", padx=10)

        # Banner
        bf2 = tk.Frame(nb2, bg=C["bg2"]); nb2.add(bf2, text="  Banner  ")
        bt  = scrolledtext.ScrolledText(bf2, bg=C["bg"], fg=C["green"],
                                         font=("Consolas",9), relief="flat")
        bt.pack(fill="both", expand=True, padx=4, pady=4)
        bt.insert("end", banner or "(no banner captured)")
        bt.configure(state="disabled")

        # CVE — live lookup panel
        cf2 = tk.Frame(nb2, bg=C["bg2"]); nb2.add(cf2, text="  🔴 Live CVEs  ")
        chdr2 = tk.Frame(cf2, bg=C["panel2"]); chdr2.pack(fill="x")
        tk.Label(chdr2, text=f"  Exploit-DB + NVD live results for port {port} / {service}",
                 bg=C["panel2"], fg=C["red"],
                 font=("Segoe UI Semibold",9)).pack(side="left", padx=8, pady=4)
        cst2 = tk.StringVar(value="Loading …")
        tk.Label(chdr2, textvariable=cst2, bg=C["panel2"], fg=C["text_dim"],
                 font=("Segoe UI",8)).pack(side="right", padx=8)

        ct = scrolledtext.ScrolledText(cf2, bg=C["bg"], fg=C["text"],
                                        font=("Consolas",9), relief="flat", wrap="word")
        ct.pack(fill="both", expand=True, padx=4, pady=4)
        for tg, col2 in [("crit",C["red"]),("high",C["orange"]),("med",C["yellow"]),
                          ("low",C["lime"]),("hdr",C["cyan"]),("dim",C["text_dim"]),
                          ("edb",C["purple"]),("nvd",C["blue"]),("url",C["cyan"]),
                          ("title",C["text_hi"])]:
            ct.tag_config(tg, foreground=col2)

        def _fill_cve(p_str, svc_str, ver_str, ban_str):
            try:
                pnum2 = int(p_str)
            except:
                pnum2 = 0
            ct.configure(state="normal")
            ct.delete("1.0","end")
            ct.insert("end", f"\n  Querying Exploit-DB and NVD for port {pnum2} ({svc_str}) …\n", "dim")
            ct.configure(state="disabled")

            def _cb(p, res):
                def _upd():
                    ct.configure(state="normal")
                    ct.delete("1.0","end")
                    edb_e = [c for c in res if c.get("source")=="Exploit-DB" and not c.get("error")]
                    nvd_e = [c for c in res if c.get("source")=="NVD" and not c.get("error")]
                    cst2.set(f"✅ {len(edb_e)} Exploit-DB  +  {len(nvd_e)} NVD CVEs  (live)")

                    ct.insert("end",
                        f"\n  ╔═ Port {p}  ·  {svc_str}"+(f"  ·  {ver_str}" if ver_str else "")+"  ═══════════╗\n","hdr")
                    ct.insert("end","  ║  Source: 🔴 exploit-db.com  +  🔵 NVD (NIST)  —  100% live\n","dim")
                    if ban_str:
                        ct.insert("end",f"  ║  Banner: {ban_str[:100]}\n","dim")
                    ct.insert("end","  ╚════════════════════════════════════════════════════╝\n\n","hdr")

                    if edb_e:
                        ct.insert("end",
                            f"  ┌─ 🔴 Exploit-DB  ({len(edb_e)} exploits)  https://www.exploit-db.com ───\n","edb")
                        for e in edb_e:
                            sev=e.get("severity","?")
                            ct.insert("end",f"  │  [{sev}] ","edb")
                            ct.insert("end",f"EDB-{e.get('edb_id','')}","edb")
                            if e.get("cve_id"): ct.insert("end",f"  {e['cve_id']}","nvd")
                            ct.insert("end",f"  {e.get('title','')[:80]}\n","title")
                            meta = "  ".join(filter(None,[e.get('date',''),e.get('type',''),e.get('platform','')]))
                            if meta: ct.insert("end",f"  │     {meta}\n","dim")
                            ct.insert("end",f"  │     🔗 {e.get('url','')}\n","url")
                        ct.insert("end","  └──────────────────────────────────────────────────\n","edb")

                    if nvd_e:
                        ct.insert("end",
                            f"\n  ┌─ 🔵 NVD / NIST  ({len(nvd_e)} CVEs)  https://nvd.nist.gov ──────────\n","nvd")
                        for e in nvd_e:
                            sev=e.get("severity","?")
                            ct.insert("end",f"  │  [{sev}] CVSS:{e.get('cvss','?')}  ","nvd")
                            ct.insert("end",f"{e.get('cve_id','')}","title")
                            ct.insert("end",f"  {e.get('published','')}\n","dim")
                            ct.insert("end",f"  │     {e.get('title','')[:100]}\n","dim")
                            ct.insert("end",f"  │     🔗 {e.get('url','')}\n","url")
                        ct.insert("end","  └──────────────────────────────────────────────────\n","nvd")

                    if not (edb_e or nvd_e):
                        ct.insert("end",
                            "  No results found on Exploit-DB or NVD.\n"
                            "  Try a manual search below.\n","dim")
                    ct.configure(state="disabled")
                try: w.after(0, _upd)
                except: pass

            fetch_cves_async(pnum2, service=svc_str, banner=ban_str,
                              version=ver_str, callback=_cb)

        _fill_cve(port, service, version, banner)

        def _open_edb():
            import webbrowser
            q = urllib.request.quote((service or f"port {port}").split()[0])
            webbrowser.open(f"https://www.exploit-db.com/search?q={q}")
        Btn(chdr2, "🌐 Exploit-DB", _open_edb,
            bg=C["btn_b"], fg=C["blue"],
            font=("Segoe UI",8), padx=6, pady=2).pack(side="right", padx=4)

        nb2.select(cf2)  # open directly on CVE tab
        Btn(w, "Close", w.destroy, bg=C["btn_r"], fg=C["red"]).pack(pady=6)

    def _topology(self):
        if not MPLOT or not NX:
            messagebox.showinfo("Missing","pip install matplotlib networkx"); return
        if not self.app.host_db:
            messagebox.showinfo("Empty","Run a scan first"); return
        self._draw_topology()

    def _draw_topology(self):
        w = tk.Toplevel(self.app)
        w.title("Network Topology — ReconShield v1.0")
        w.configure(bg=C["bg"]); w.geometry("1360x900")
        w.resizable(True,True)

        tk.Frame(w, bg=C["cyan"], height=3).pack(fill="x")
        hf = tk.Frame(w, bg=C["panel"]); hf.pack(fill="x")
        tk.Label(hf, text=" 🌐  Network Topology  —  Router-Centric Star Map",
                 bg=C["panel"], fg=C["cyan"],
                 font=("Segoe UI Semibold",13)).pack(side="left",padx=12,pady=8)
        n_hosts = len(self.app.host_db)
        rc_cnt  = collections.Counter(h.get("risk","?")
                                      for h in self.app.host_db.values())
        tk.Label(hf,
                 text=(f"Hosts: {n_hosts}  "
                       f"Critical: {rc_cnt.get('Critical',0)}  "
                       f"High: {rc_cnt.get('High',0)}  "
                       f"Medium: {rc_cnt.get('Medium',0)}"),
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI",9)).pack(side="right",padx=14)

        fig = Figure(figsize=(14,9), facecolor=C["bg"])
        fig.subplots_adjust(left=0.01, right=0.80, top=0.94, bottom=0.03)
        ax  = fig.add_subplot(111, facecolor=C["bg"])
        ax.axis("off")

        G   = nx.Graph()
        gw  = get_local_ip()
        base= ".".join(gw.split(".")[:3])
        router_ip = gw
        for ip in self.app.host_db:
            if ip.rsplit(".",1)[-1] in ("1","254"):
                router_ip = ip; break

        G.add_node(router_ip, kind="router")
        for ip, h in self.app.host_db.items():
            G.add_node(ip, kind="host",
                       risk=h.get("risk","Unknown"),
                       ports=len(h.get("ports",{})),
                       os=h.get("os","?"),
                       hn=h.get("hostname",""),
                       vendor=h.get("vendor",""))
            G.add_edge(router_ip, ip,
                       weight=max(1, len(h.get("ports",{}))))

        hosts_only = [n for n in G.nodes() if n != router_ip]
        pos = {router_ip: (0.0, 0.0)}
        ring_r = [1.8, 3.2, 4.6, 6.0, 7.4]
        ring_cap = [8, 16, 24, 32, 999]
        ring_i = 0; ring_count = 0; aoff = 0.0
        for ip in hosts_only:
            cap = ring_cap[ring_i]
            angle = 2*math.pi * ring_count/cap + aoff
            r = ring_r[ring_i]
            pos[ip] = (r*math.cos(angle), r*math.sin(angle))
            ring_count += 1
            if ring_count >= cap:
                ring_i = min(ring_i+1, len(ring_r)-1)
                ring_count = 0
                aoff += math.pi/(cap+1)

        RCOL = {"Critical":C["red"],"High":C["orange"],"Medium":C["yellow"],
                "Low":C["lime"],"Unknown":C["blue"]}

        # Draw edges
        for u,v in G.edges():
            host   = v if u==router_ip else u
            risk   = G.nodes[host].get("risk","Unknown")
            col    = RCOL.get(risk,"#1A3060")
            px,py  = pos[u]; qx,qy = pos[v]
            ax.plot([px,qx],[py,qy], color=col,
                    linewidth=0.5+G.edges[u,v].get("weight",1)*0.08,
                    alpha=0.45, zorder=1)

        # Draw host nodes
        for ip in hosts_only:
            x,y = pos[ip]; h=self.app.host_db.get(ip,{})
            risk = G.nodes[ip].get("risk","Unknown")
            col  = RCOL.get(risk,C["blue"])
            ports= G.nodes[ip].get("ports",0)
            sz   = 80 + ports*25
            ax.scatter([x],[y], s=sz, c=[col], marker="o",
                       alpha=0.85, zorder=3,
                       edgecolors="white", linewidths=0.6)
            hn = (G.nodes[ip].get("hn") or "")[:14]
            lines=[ip]
            if hn: lines.append(hn)
            lines.append(G.nodes[ip].get("os","")[:12] or "")
            if ports: lines.append(f"{ports}p")
            cx,cy = x,y
            mag = math.hypot(cx,cy) or 1
            ox,oy = cx/mag*0.55, cy/mag*0.55
            ax.annotate("\n".join(l for l in lines if l),
                        xy=(x,y), xytext=(x+ox, y+oy),
                        color=col, fontsize=5.5, ha="center", va="center",
                        zorder=5,
                        bbox=dict(boxstyle="round,pad=0.2",
                                  facecolor=C["bg"], edgecolor=col,
                                  alpha=0.82, linewidth=0.7),
                        arrowprops=dict(arrowstyle="-",color=col,
                                        lw=0.5,alpha=0.5))

        # Router node
        rx,ry = pos[router_ip]
        ax.scatter([rx],[ry], s=4000, marker="*",
                   c=[C["cyan"]], alpha=0.95, zorder=6,
                   edgecolors="white", linewidths=1.2)
        ax.annotate(f"  ROUTER\n  {router_ip}",
                    xy=(rx,ry), xytext=(rx+0.2,ry+0.45),
                    color=C["cyan"], fontsize=9, fontweight="bold", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.3",
                              facecolor=C["card"],edgecolor=C["cyan"],alpha=0.9))

        n_str = len(self.app.host_db)
        ax.set_title(f"Network Topology  ·  {n_str} hosts  ·  Gateway {router_ip}",
                     color=C["cyan"], fontsize=12, pad=10, fontweight="bold")

        # Legend
        la = fig.add_axes([0.81,0.05,0.17,0.88])
        la.set_facecolor(C["panel"]); la.axis("off")
        la.text(0.1,0.97,"LEGEND",color=C["cyan"],fontsize=10,fontweight="bold",va="top")
        y=0.90
        for lbl2,c in [("★ Router/GW",C["cyan"]),("● Host",C["text_dim"])]:
            la.text(0.1,y,lbl2,color=c,fontsize=8,va="top"); y-=0.05
        y-=0.03
        la.text(0.1,y,"Risk Level",color=C["text_dim"],fontsize=8,va="top"); y-=0.05
        for rk,c in [("Critical",C["red"]),("High",C["orange"]),
                      ("Medium",C["yellow"]),("Low",C["lime"]),
                      ("Unknown",C["blue"])]:
            la.scatter([0.1],[y],s=60,c=[c],marker="o",zorder=3)
            cnt=rc_cnt.get(rk,0)
            la.text(0.25,y,f"{rk} ({cnt})",color=c,fontsize=7.5,va="center"); y-=0.05
        y-=0.03
        la.text(0.1,y,"Node size ∝ open ports",color=C["text_dim"],fontsize=7,va="top"); y-=0.05
        la.text(0.1,y,"Edge width ∝ open ports",color=C["text_dim"],fontsize=7,va="top"); y-=0.07
        # Risk summary
        la.text(0.1,y,"Summary",color=C["text_dim"],fontsize=8,va="top"); y-=0.05
        for k2,v2 in rc_cnt.most_common():
            la.text(0.1,y,f"  {k2}: {v2}",
                    color=RCOL.get(k2,C["text"]),fontsize=7,va="top")
            y-=0.04
        y-=0.03
        tot_ports = sum(len(h.get("ports",{})) for h in self.app.host_db.values())
        la.text(0.1,y,f"Total open ports: {tot_ports}",
                color=C["text_dim"],fontsize=7,va="top"); y-=0.04
        la.text(0.1,y,f"Avg ports/host: {tot_ports/max(n_hosts,1):.1f}",
                color=C["text_dim"],fontsize=7,va="top")
        la.set_xlim(0,1); la.set_ylim(0,1)
        for sp in la.spines.values(): sp.set_edgecolor(C["border"])

        canvas = FigureCanvasTkAgg(fig, master=w)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)
        canvas.draw()

        def _click(event):
            if event.inaxes is not ax: return
            ex,ey = event.xdata,event.ydata
            if ex is None: return
            best,bd = None,0.5
            for ip2,(x2,y2) in pos.items():
                d = math.hypot(ex-x2,ey-y2)
                if d < bd: best,bd = ip2,d
            if best and best != router_ip:
                hh = self.app.host_db.get(best)
                if hh: self._show_host_popup(best, hh)
        canvas.mpl_connect("button_press_event", _click)
        tk.Label(w, text="  💡 Click any host node to view full detail",
                 bg=C["panel2"],fg=C["text_dim"],font=("Segoe UI",8)).pack(fill="x",pady=2)

# ═══════════════════════════════════════════════════════════════════
#  TAB 2: PACKET ANALYZER
# ═══════════════════════════════════════════════════════════════════
class PacketTab(tk.Frame):
    MAX_PKTS = 50000

    def __init__(self, nb, app):
        super().__init__(nb, bg=C["bg2"])
        self.app        = app
        self._engine    = None
        self._stop_ev   = threading.Event()
        self._pkts      = collections.deque(maxlen=50000)
        self._seq_map   = {}
        self._polling   = False
        self._poll_id   = None
        self._host_cache  = {}
        self._dns_pending = set()
        self._session_tracker = SessionTracker()
        self._http_threat_count = 0
        self._sess_tick = 0
        self._build()

    def _build(self):
        hdr = SecHdr(self,
                     "📡  Packet Analyzer  —  Real-time Promiscuous Capture  ·  HTTP Inspector  ·  GeoIP  ·  Session Tracker",
                     C["green"],
                     sub="HTTP Attack Detection (SQLi / XSS / RCE / SSRF / Path Traversal)  ·  50+ fields/packet  ·  Hex dump  ·  OSI stack  ·  Sessions  ·  Right-click for context menu")

        # ── Control bar ────────────────────────────────────────────────
        cf = tk.Frame(self, bg=C["panel2"], pady=5); cf.pack(fill="x")
        r1 = tk.Frame(cf, bg=C["panel2"]); r1.pack(fill="x", padx=10, pady=2)

        Lbl(r1,"Interface:", bg=C["panel2"], fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._iface  = tk.StringVar()
        self._iface_cb = ttk.Combobox(r1, textvariable=self._iface,
                                       width=24, state="readonly")
        self._refresh_ifaces()
        self._iface_cb.pack(side="left", padx=6)
        Btn(r1,"↺",self._refresh_ifaces,
            font=("Segoe UI",9),padx=6,pady=4).pack(side="left",padx=(0,8))

        Lbl(r1,"Proto:", bg=C["panel2"], fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._filt_proto = ttk.Combobox(r1, width=8, state="readonly",
            values=["ALL","TCP","UDP","DNS","HTTP","TLS","ICMP","ARP",
                    "DHCP","NTP","SNMP","SSH","FTP","SMTP"])
        self._filt_proto.set("ALL"); self._filt_proto.pack(side="left",padx=6)

        Lbl(r1,"IP:", bg=C["panel2"], fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._filt_ip = tk.StringVar()
        tk.Entry(r1, textvariable=self._filt_ip, bg=C["card"],
                 fg=C["cyan"], font=("Consolas",9), width=14,
                 relief="flat", insertbackground=C["cyan"],
                 highlightthickness=1,
                 highlightbackground=C["border"]).pack(side="left",padx=4)

        Lbl(r1,"Port:", bg=C["panel2"], fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._filt_port = tk.StringVar()
        tk.Entry(r1, textvariable=self._filt_port, bg=C["card"],
                 fg=C["cyan"], font=("Consolas",9), width=7,
                 relief="flat", insertbackground=C["cyan"],
                 highlightthickness=1,
                 highlightbackground=C["border"]).pack(side="left",padx=4)

        Lbl(r1,"Search:", bg=C["panel2"], fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._filt_text = tk.StringVar()
        tk.Entry(r1, textvariable=self._filt_text, bg=C["card"],
                 fg=C["cyan"], font=("Consolas",9), width=16,
                 relief="flat", insertbackground=C["cyan"],
                 highlightthickness=1,
                 highlightbackground=C["border"]).pack(side="left",padx=4)

        GBtn(r1,"▶  Start Capture", self._start, padx=14, pady=6).pack(side="left",padx=8)
        RBtn(r1,"■  Stop",          self._stop,  padx=12, pady=6).pack(side="left",padx=3)
        Btn(r1,"🗑  Clear",         self._clear_pkts, padx=10, pady=6).pack(side="left",padx=3)
        Btn(r1,"💾  Export",        self._export_json, padx=10, pady=6).pack(side="left",padx=3)
        Btn(r1,"📊  Charts",        self._proto_chart, padx=10, pady=6).pack(side="left",padx=3)

        # Status/mode row
        r2 = tk.Frame(cf, bg=C["panel2"]); r2.pack(fill="x", padx=10, pady=(0,4))
        self._cap_status = tk.StringVar(value="⏹  Not capturing")
        tk.Label(r2, textvariable=self._cap_status,
                 bg=C["panel2"], fg=C["text_dim"],
                 font=("Segoe UI",8,"italic")).pack(side="left")

        # Npcap availability badge
        if _OS == "win32":
            if _scapy_available():
                badge_txt = "✅ Scapy+Npcap — full network capture"
                badge_col = C["green"]
            elif _npcap_available():
                badge_txt = "✅ Npcap — full network capture"
                badge_col = C["green"]
            else:
                badge_txt = "⚠ No Npcap — own machine only  [click to fix]"
                badge_col = C["orange"]
            badge = tk.Label(r2, text=f"  {badge_txt}  ",
                             bg=C["panel2"], fg=badge_col,
                             font=("Segoe UI Semibold", 8),
                             cursor="hand2" if "fix" in badge_txt else "arrow")
            badge.pack(side="right", padx=6)
            if "fix" in badge_txt:
                badge.bind("<Button-1>", lambda e: self._show_npcap_guide())
        else:
            # Linux — AF_PACKET is native
            mode_txt = ("🟢 AF_PACKET promiscuous — full network capture"
                        if ROOT else
                        "🟡 Run with sudo for full promiscuous capture")
            tk.Label(r2, text=f"  {mode_txt}  ",
                     bg=C["panel2"],
                     fg=C["green"] if ROOT else C["yellow"],
                     font=("Segoe UI Semibold", 8)).pack(side="right", padx=6)

        # Stats strip
        sf = tk.Frame(cf, bg=C["panel2"]); sf.pack(fill="x", padx=10, pady=2)
        self._sv = {}
        for key,label,col in [
            ("total","Total",C["text"]),("TCP","TCP",C["blue"]),
            ("UDP","UDP",C["purple"]),("DNS","DNS",C["yellow"]),
            ("HTTP","HTTP",C["green"]),("TLS","TLS",C["cyan"]),
            ("ICMP","ICMP",C["orange"]),("ARP","ARP",C["teal"]),
            ("SSH","SSH",C["teal"]),("FTP","FTP",C["pink"]),
            ("SMTP","SMTP",C["orange"]),("OTHER","Other",C["indigo"]),
            ("ALERTS","🚨 Alerts",C["red"]),
            ("HTTP_THREATS","🌐 HTTP Threats",C["red"]),
        ]:
            f = tk.Frame(sf, bg=C["card"], padx=7, pady=2,
                         highlightbackground=col, highlightthickness=1)
            f.pack(side="left", padx=1)
            v = tk.StringVar(value="0"); self._sv[key] = v
            tk.Label(f,text=label,bg=C["card"],fg=C["text_dim"],
                     font=("Segoe UI",6,"bold")).pack()
            tk.Label(f,textvariable=v,bg=C["card"],fg=col,
                     font=("Consolas",11,"bold")).pack()

        # ── Main pane ──────────────────────────────────────────────────
        pane = tk.PanedWindow(self, orient="vertical",
                              bg=C["bg"], sashwidth=5)
        pane.pack(fill="both", expand=True, padx=4, pady=4)

        # Packet list  —  full device identity columns
        top = tk.Frame(pane, bg=C["bg2"]); pane.add(top, height=320)
        pcols = ["#","Time","Src IP","Src MAC","Src Host",
                 "Dst IP","Dst MAC","Dst Host",
                 "Proto","App","Spt","Dpt","Len","TTL","Flags","Ent","Risk","Info"]
        pwids = [44,88,112,130,130, 112,130,130,
                 54,68,50,50,50,40,110,50,46,260]
        self._tree = make_tree(top, pcols, pwids, height=14)

        PTAGS = [
            ("TCP",   C["blue"],   "#03091A"),
            ("HTTP",  C["green"],  "#041004"),
            ("TLS",   C["cyan"],   "#031214"),
            ("DNS",   C["yellow"], "#141000"),
            ("UDP",   C["purple"], "#0C0514"),
            ("ICMP",  C["orange"], "#140800"),
            ("ARP",   C["teal"],   "#041210"),
            ("DHCP",  C["lime"],   "#0A1404"),
            ("SSH",   "#00C0A8",   "#031210"),
            ("FTP",   C["pink"],   "#14050C"),
            ("SMTP",  C["orange"], "#140A00"),
            ("ALERT", C["red"],    "#1A0005"),
            ("CRIT",  C["red"],    "#200008"),
            ("odd",   C["text"],   C["card"]),
            ("even",  C["text"],   C["card2"]),
        ]
        for t,fg2,bg2 in PTAGS:
            self._tree.tag_configure(t, foreground=fg2, background=bg2)
        self._tree.bind("<Double-1>",        self._pkt_detail_popup)
        self._tree.bind("<<TreeviewSelect>>", self._pkt_select)
        self._tree.bind("<Button-3>",         self._pkt_context_menu)

        # Detail pane
        bot = tk.Frame(pane, bg=C["bg2"]); pane.add(bot, height=300)
        dnb = ttk.Notebook(bot); dnb.pack(fill="both", expand=True)

        self._detail_txt = scrolledtext.ScrolledText(
            dnb, bg=C["bg"], fg=C["text"],
            font=("Consolas",9), state="disabled",
            relief="flat", wrap="none")
        dnb.add(self._detail_txt, text="  📋 Full Detail  ")

        self._hex_txt = scrolledtext.ScrolledText(
            dnb, bg=C["bg"], fg=C["green"],
            font=("Consolas",9), state="disabled",
            relief="flat", wrap="none")
        dnb.add(self._hex_txt, text="  🔢 Hex Dump  ")

        self._layer_txt = scrolledtext.ScrolledText(
            dnb, bg=C["bg"], fg=C["text_dim"],
            font=("Consolas",9), state="disabled",
            relief="flat", wrap="none")
        dnb.add(self._layer_txt, text="  🗂 OSI Layers  ")

        self._flow_txt = scrolledtext.ScrolledText(
            dnb, bg=C["bg"], fg=C["cyan"],
            font=("Consolas",9), state="disabled",
            relief="flat", wrap="none")
        dnb.add(self._flow_txt, text="  🔗 Flow Analysis  ")

        # ── HTTP Inspector tab ────────────────────────────────────────
        self._http_frame = tk.Frame(dnb, bg=C["bg"])
        dnb.add(self._http_frame, text="  🌐 HTTP Inspector  ")
        self._http_txt = scrolledtext.ScrolledText(
            self._http_frame, bg=C["bg"], fg=C["text"],
            font=("Consolas",9), state="disabled",
            relief="flat", wrap="word")
        self._http_txt.pack(fill="both", expand=True)
        for tag, fg2, style in [
            ("hdr",  C["cyan"],     "bold"), ("key", C["text_dim"], ""),
            ("val",  C["text_hi"],  ""),     ("crit", C["red"],     "bold"),
            ("warn", C["orange"],   "bold"), ("ok",   C["green"],   ""),
            ("info", C["cyan"],     ""),     ("dim",  C["text_dim"],""),
            ("sep",  C["border"],   ""),     ("addr", C["yellow"],  "bold"),
            ("asc",  C["teal"],     ""),     ("port", C["purple"],  "bold"),
            ("flag", C["orange"],   "bold"), ("hex",  C["green"],   ""),
        ]:
            self._http_txt.tag_config(tag, foreground=fg2,
                font=("Consolas",9,style) if style else ("Consolas",9))

        # ── Session Tracker tab ─────────────────────────────────────
        self._sess_outer = tk.Frame(dnb, bg=C["bg"])
        dnb.add(self._sess_outer, text="  🔀 Sessions  ")
        sess_top = tk.Frame(self._sess_outer, bg=C["panel2"], pady=3)
        sess_top.pack(fill="x")
        Btn(sess_top, "↺ Refresh", self._refresh_sessions,
            font=("Segoe UI",8), padx=8, pady=3).pack(side="left", padx=6)
        Btn(sess_top, "🗑 Clear", self._clear_sessions,
            bg=C["btn_r"], fg=C["red"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="left", padx=2)
        self._sess_count_var = tk.StringVar(value="Sessions: 0")
        tk.Label(sess_top, textvariable=self._sess_count_var,
                 bg=C["panel2"], fg=C["cyan"],
                 font=("Consolas",8)).pack(side="right", padx=8)
        sess_cols = ["Flow","Proto","State","Src","Dst","Pkts","Bytes","HTTP","Risk","Duration"]
        sess_wids = [190,55,90,120,120,50,70,55,55,75]
        self._sess_tree = make_tree(self._sess_outer, sess_cols, sess_wids, height=8)
        for t, c in [("CRITICAL",C["red"]),("HIGH",C["orange"]),
                     ("MEDIUM",C["yellow"]),("DATA",C["green"]),("NEW",C["blue"])]:
            self._sess_tree.tag_configure(t, foreground=c)
        self._sess_tree.bind("<<TreeviewSelect>>", self._sess_select)

    def _refresh_ifaces(self):
        ifaces = get_all_iface_ips()
        entries = ["ALL interfaces"]
        for name, info in ifaces.items():
            entries.append(f"{name}  [{info['ip']}]")
        self._iface_cb["values"] = entries
        if not self._iface.get():
            self._iface.set(entries[0])

    def _resolve_iface(self):
        sel = self._iface.get()
        if not sel or sel.startswith("ALL"): return None
        return sel.split("[")[0].strip()

    def _start(self):
        self._stop_ev.set(); self._stop_ev.clear()
        while True:
            try: self.app.pkt_queue.get_nowait()
            except queue.Empty: break
        self.app.cap_stats.clear()
        self.app.cap_stats["total"] = 0
        iface = self._resolve_iface()
        self._engine = CaptureEngine(self.app.pkt_queue, self.app.cap_stats,
                                      self._stop_ev, iface=iface)
        self._engine.start()
        label = iface or "ALL interfaces"
        self._cap_status.set(f"🟡  Starting capture on {label} …")
        self.app.status.set(f"📡 Capturing on {label}")
        self._polling = True
        if self._poll_id:
            try: self.after_cancel(self._poll_id)
            except: pass
        self._poll_id = self.after(80, self._poll)
        # Check method + errors after 2.5s
        self.after(2500, self._check_engine_error)
        self.after(2500, self._update_method_label)

    def _update_method_label(self):
        """Show which capture method is active and warn if limited."""
        method = self.app.cap_stats.get("method", "")
        warn   = self.app.cap_stats.get("warn", "")
        if "Scapy" in method or "Npcap" in method:
            self._cap_status.set(f"🟢  {method}")
        elif "AF_PACKET" in method:
            self._cap_status.set(f"🟢  {method}")
        elif method:
            self._cap_status.set(f"🟡  {method}")
            if warn:
                self.after(100, lambda: messagebox.showwarning(
                    "Limited Capture — Install Npcap",
                    f"{warn}\n\nCurrently only capturing traffic to/from THIS machine.\n\n"
                    f"To capture ALL devices on the network:\n"
                    f"1. Download Npcap: https://npcap.com/#download\n"
                    f"2. Install with 'WinPcap API compatibility' checked\n"
                    f"3. Restart ReconShield as Administrator\n\n"
                    f"Alternatively: pip install scapy"))
        if warn and not method:
            self._cap_status.set(f"🟡  {warn[:80]}")

    def _show_npcap_guide(self):
        w = tk.Toplevel(self.app)
        w.title("Install Npcap for Full Network Capture")
        w.configure(bg=C["bg"]); w.geometry("680x520")
        w.resizable(False, False)
        tk.Frame(w, bg=C["orange"], height=4).pack(fill="x")
        tk.Label(w, text="  ⚠  Install Npcap for Full Network Packet Capture",
                 bg=C["panel"], fg=C["orange"],
                 font=("Segoe UI Semibold", 12)).pack(fill="x", pady=8)

        txt = scrolledtext.ScrolledText(w, bg=C["bg"], fg=C["text"],
                                         font=("Segoe UI", 10),
                                         relief="flat", wrap="word",
                                         state="normal")
        txt.pack(fill="both", expand=True, padx=16, pady=8)
        guide = """WHY YOU NEED NPCAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Windows raw sockets (SIO_RCVALL) only deliver packets addressed TO
this machine. You cannot see traffic between other devices on the
network without a packet capture driver.

Npcap is a free Windows packet capture driver (successor to WinPcap)
that installs an NDIS filter driver and enables true promiscuous mode —
you can see ALL packets on the network segment.

OPTION 1 — Npcap (recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Download:  https://npcap.com/#download
2. Run installer as Administrator
3. ✅ Check "WinPcap API-compatible Mode"
4. ✅ Check "Install Npcap in WinPcap API-compatible Mode"
5. Restart this tool as Administrator

OPTION 2 — Scapy + Npcap (adds Python API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Install Npcap as above
2. Open Admin command prompt:
   pip install scapy
3. Restart ReconShield as Administrator

ReconShield will automatically use Scapy if available.

WITHOUT NPCAP — what you get
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Traffic TO this machine (inbound)
• Traffic FROM this machine (outbound)
• Broadcast/multicast to subnet

NOT VISIBLE without Npcap:
• Traffic between other devices (e.g. phone ↔ router)
• Traffic to/from other PCs on the LAN
• VLAN-tagged frames to other hosts
"""
        txt.insert("end", guide)
        txt.configure(state="disabled")

        bf = tk.Frame(w, bg=C["bg"]); bf.pack(fill="x", pady=8)
        def _open_npcap():
            import webbrowser
            webbrowser.open("https://npcap.com/#download")
        Btn(bf, "🌐  Open Npcap Download Page", _open_npcap,
            bg=C["btn_g"], fg=C["green"]).pack(side="left", padx=12)
        Btn(bf, "Close", w.destroy,
            bg=C["btn_r"], fg=C["red"]).pack(side="right", padx=12)

    def _stop(self):
        self._stop_ev.set()
        self._polling = False
        self._cap_status.set("⏹  Capture stopped")
        self.app.status.set("⏹ Stopped")

    def _poll(self):
        if not self._polling:
            if self.winfo_exists(): self._poll_id = self.after(200, self._poll)
            return

        # Drain up to 500 packets per tick for maximum throughput
        batch = []
        get = self.app.pkt_queue.get_nowait
        try:
            for _ in range(500):
                batch.append(get())
        except queue.Empty:
            pass

        if batch:
            fproto = self._filt_proto.get()
            fip    = self._filt_ip.get().strip()
            fport  = self._filt_port.get().strip()
            ftext  = self._filt_text.get().strip().lower()
            try:    fport_int = int(fport)
            except: fport_int = None

            display_batch = []
            engine_feed   = self.app.engine.feed

            for pkt in batch:
                # Feed threat engine (always, for every packet)
                engine_feed(pkt)
                # Feed session tracker
                self._session_tracker.feed(pkt)
                # Count HTTP threats
                if pkt.app_proto == "HTTP":
                    if analyze_http_security(pkt):
                        self._http_threat_count += 1

                # Store packet — O(1) deque vs O(n) list.pop(0)
                if len(self._pkts) >= self.MAX_PKTS:
                    removed = self._pkts.popleft()
                    self._seq_map.pop(removed.seq, None)
                    children = self._tree.get_children()
                    if children:
                        self._tree.delete(children[0])
                self._pkts.append(pkt)
                self._seq_map[pkt.seq] = pkt   # direct reference

                # Filter
                if fproto and fproto != "ALL":
                    if pkt.app_proto != fproto and pkt.proto != fproto:
                        continue
                if fip:
                    if fip not in (pkt.src_ip or "") and \
                       fip not in (pkt.dst_ip or ""):
                        continue
                if fport_int is not None:
                    if pkt.sport != fport_int and pkt.dport != fport_int:
                        continue
                if ftext:
                    combined = (f"{pkt.info or ''}{pkt.dns_query or ''}"
                                f"{pkt.http_uri or ''}{pkt.tls_sni or ''}"
                                f"{pkt.src_ip or ''}{pkt.dst_ip or ''}").lower()
                    if ftext not in combined:
                        continue

                display_batch.append(pkt)

            # Batch-insert into tree (one disable/enable cycle)
            if display_batch:
                auto_scroll = not self._tree.selection()
                for pkt in display_batch:
                    self._insert_pkt(pkt)
                if auto_scroll:
                    self._tree.yview_moveto(1)

        # Update stats counters
        s = self.app.cap_stats
        # Count HTTP threats in recent packets
        if not hasattr(self, "_http_threat_count"): self._http_threat_count = 0
        for key in self._sv:
            if key == "ALERTS":
                self._sv[key].set(str(len(self.app.engine.get_alerts(500))))
            elif key == "HTTP_THREATS":
                self._sv[key].set(str(self._http_threat_count))
            else:
                self._sv[key].set(str(s.get(key, 0)))

        # Auto-refresh session view every ~5 seconds
        if not hasattr(self, "_sess_tick"): self._sess_tick = 0
        self._sess_tick += 1
        if self._sess_tick >= 50:
            self._sess_tick = 0
            try: self._refresh_sessions()
            except: pass

        if self.winfo_exists():
            # Adaptive poll rate: faster when packets are flowing
            interval = 50 if batch else 100
            self._poll_id = self.after(interval, self._poll)

    def _insert_pkt(self, pkt):
        app_p = pkt.app_proto or pkt.proto or "?"
        risk  = ("CRIT"  if pkt.risk_score >= 70 else
                 "ALERT" if pkt.risk_score >= 40 else
                 app_p   if app_p in ("TCP","UDP","DNS","HTTP","TLS","ICMP",
                                      "ARP","DHCP","SSH","FTP","SMTP") else
                 ("odd"  if pkt.seq % 2 == 0 else "even"))

        flags = pkt.tcp_flags_str or ""
        ent   = f"{pkt.payload_entropy:.2f}" if pkt.payload_entropy else "—"
        rs    = str(pkt.risk_score or 0)

        # ── Device identity enrichment ───────────────────────────────
        src_ip  = pkt.src_ip  or ""
        dst_ip  = pkt.dst_ip  or ""
        src_mac = pkt.eth_src or (pkt.arp_smac or "")
        dst_mac = pkt.eth_dst or (pkt.arp_tmac or "")

        # ARP packets carry MAC in dedicated fields
        if pkt.app_proto == "ARP":
            src_mac = pkt.arp_smac or src_mac
            dst_mac = pkt.arp_tmac or dst_mac

        # Vendor from MAC OUI
        src_vendor = _mac_vendor(src_mac) if src_mac else ""
        dst_vendor = _mac_vendor(dst_mac) if dst_mac else ""

        # Hostname — use known host_db first, then cached reverse-DNS
        src_host = self._resolve_host(src_ip, src_mac)
        dst_host = self._resolve_host(dst_ip, dst_mac)

        # If DNS response — annotate with resolved name
        if pkt.app_proto == "DNS" and pkt.dns_answers:
            ans_str = ",".join(pkt.dns_answers[:2])
            src_host = src_host or pkt.dns_query or ""

        # Build rich Info string
        info = pkt.info or ""
        if pkt.app_proto == "HTTP":
            info = (f"HTTP {pkt.http_method or ''} {pkt.http_host or ''}"
                    f"{pkt.http_uri or ''}"
                    + (f" → {pkt.http_status}" if pkt.http_status else ""))
        elif pkt.app_proto == "TLS":
            info = (f"TLS {pkt.tls_ver or ''}"
                    + (f" SNI:{pkt.tls_sni}" if pkt.tls_sni else "")
                    + (f" [{pkt.tls_record_type}]" if pkt.tls_record_type else ""))
        elif pkt.app_proto == "DNS":
            info = (f"DNS {pkt.dns_qr or ''} {pkt.dns_query or ''}"
                    + (f"→{','.join(pkt.dns_answers[:2])}" if pkt.dns_answers else ""))
        elif pkt.app_proto == "ARP":
            info = f"ARP {pkt.arp_op} {pkt.arp_sip}({pkt.arp_smac}) → {pkt.arp_dip}"
        elif pkt.app_proto == "DHCP":
            info = f"DHCP {src_ip} → {dst_ip}"

        self._tree.insert("", "end", iid=str(pkt.seq), values=(
            pkt.seq,
            pkt.ts_str  or "",
            src_ip,
            src_mac,
            (src_vendor + ("·" + src_host if src_host else ""))[:28],
            dst_ip,
            dst_mac,
            (dst_vendor + ("·" + dst_host if dst_host else ""))[:28],
            pkt.proto   or "",
            app_p,
            pkt.sport   or "",
            pkt.dport   or "",
            pkt.length  or 0,
            pkt.ip_ttl  or "",
            flags[:28],
            ent, rs,
            info[:160],
        ), tags=(risk,))

    def _resolve_host(self, ip, mac=""):
        """Fast hostname lookup: host_db → DNS cache → async reverse-DNS."""
        if not ip: return ""
        # 1. Already in scan host_db
        h = self.app.host_db.get(ip, {})
        hn = h.get("hostname","")
        if hn: return hn
        # 2. Local reverse-DNS cache
        if ip in self._host_cache:
            return self._host_cache[ip]
        # 3. Known local names
        local_ip = get_local_ip()
        if ip == local_ip:
            self._host_cache[ip] = "this-machine"
            return "this-machine"
        if ip.endswith(".1") or ip.endswith(".254"):
            self._host_cache[ip] = "router/gateway"
            return "router/gateway"
        if ip == "255.255.255.255":
            return "broadcast"
        if ip.startswith("224.") or ip.startswith("239."):
            return "multicast"
        # 4. Trigger async reverse-DNS (non-blocking)
        if ip not in self._dns_pending:
            self._dns_pending.add(ip)
            threading.Thread(target=self._rdns, args=(ip,),
                             daemon=True).start()
        return ""

    def _rdns(self, ip):
        """Background reverse-DNS — populates cache when done."""
        try:
            hn = socket.gethostbyaddr(ip)[0]
            self._host_cache[ip] = hn[:32]
        except Exception:
            self._host_cache[ip] = ""
        finally:
            self._dns_pending.discard(ip)

    def _refresh_sessions(self):
        """Populate the session tree from the session tracker."""
        self._sess_tree.delete(*self._sess_tree.get_children())
        sessions = self._session_tracker.get_sessions(200)
        now = time.time()
        for s in sessions:
            dur = now - s["start_ts"]
            dur_str = (f"{dur:.0f}s" if dur < 60 else
                       f"{dur/60:.1f}m" if dur < 3600 else
                       f"{dur/3600:.1f}h")
            risk = s["risk_max"]
            tag  = ("CRITICAL" if risk >= 70 else "HIGH" if risk >= 40 else
                    s["state"] if s["state"] in ("DATA","NEW") else "MEDIUM")
            sport = s.get("sport") or ""
            dport = s.get("dport") or ""
            src = f"{s['src_ip']}:{sport}" if sport else s.get("src_ip","?")
            dst = f"{s['dst_ip']}:{dport}" if dport else s.get("dst_ip","?")
            self._sess_tree.insert("", "end", iid=s["flow_key"], values=(
                s["flow_key"][:38],
                s["proto"],
                s["state"],
                src[:22],
                dst[:22],
                s["packets"],
                f"{s['bytes']:,}",
                len(s["http_reqs"]),
                str(risk),
                dur_str,
            ), tags=(tag,))
        self._sess_count_var.set(f"Sessions: {len(sessions)}")

    def _clear_sessions(self):
        self._session_tracker.clear()
        self._sess_tree.delete(*self._sess_tree.get_children())
        self._sess_count_var.set("Sessions: 0")

    def _sess_select(self, event):
        """Show session detail when a session row is selected."""
        sel = self._sess_tree.selection()
        if not sel: return
        fk = sel[0]
        s  = self._session_tracker.get_session(fk)
        if not s: return
        # Show HTTP requests in a popup
        if s["http_reqs"]:
            self._show_session_http(s)

    def _show_session_http(self, s):
        """Popup showing all HTTP requests in a session."""
        w = tk.Toplevel(self.app)
        w.title(f"HTTP Session — {s['flow_key'][:60]}")
        w.configure(bg=C["bg"]); w.geometry("1100x700")
        tk.Frame(w, bg=C["green"], height=3).pack(fill="x")
        hf = tk.Frame(w, bg=C["panel"]); hf.pack(fill="x")
        tk.Label(hf, text=f"  🌐 HTTP Session  ·  {s['src_ip']} → {s['dst_ip']}  ·  "
                           f"{len(s['http_reqs'])} requests  ·  {s['packets']} packets",
                 bg=C["panel"], fg=C["green"],
                 font=("Segoe UI Semibold",11)).pack(side="left",padx=12,pady=6)

        txt = scrolledtext.ScrolledText(w, bg=C["bg"], fg=C["text"],
                                         font=("Consolas",9), relief="flat", wrap="word")
        txt.pack(fill="both", expand=True, padx=6, pady=4)

        for tag, fg2, style in [
            ("hdr",C["cyan"],"bold"),("val",C["text_hi"],""),
            ("crit",C["red"],"bold"),("warn",C["orange"],"bold"),
            ("ok",C["green"],""),("info",C["cyan"],""),
            ("dim",C["text_dim"],""),("sep",C["border"],""),
            ("addr",C["yellow"],"bold"),
        ]:
            txt.tag_config(tag, foreground=fg2,
                font=("Consolas",9,style) if style else ("Consolas",9))

        for i, req in enumerate(s["http_reqs"], 1):
            txt.insert("end", f"\n  ┌─ Request #{i}  {req['ts']} ──────────────────────────\n","sep")
            mtag = {"GET":"ok","POST":"warn","DELETE":"crit",
                    "PUT":"warn","PATCH":"warn"}.get(req["method"],"val")
            txt.insert("end", f"  │  {req['method']} ", mtag)
            txt.insert("end", f"{req['uri']}\n","info")
            if req["host"]:
                txt.insert("end", f"  │  Host: {req['host']}\n","addr")
            if req["ua"]:
                txt.insert("end", f"  │  UA: {req['ua'][:80]}\n","dim")
            if req["threats"]:
                txt.insert("end", "  │  ⚠ THREATS:\n","crit")
                for cat, sev, detail in req["threats"]:
                    stag = "crit" if sev=="CRITICAL" else "warn"
                    txt.insert("end", f"  │    [{sev}] {cat}: {detail[:60]}\n", stag)
            txt.insert("end", "  └──────────────────────────────────────────────────────\n","sep")

        txt.configure(state="disabled")
        Btn(w, "Close", w.destroy, bg=C["btn_r"], fg=C["red"]).pack(pady=6)

    def _pkt_select(self, event):
        sel = self._tree.selection()
        if not sel: return
        try:
            seq = int(sel[0])
            pkt = self._seq_map.get(seq)
            if pkt: self._show_detail(pkt)
        except: pass

    def _pkt_detail_popup(self, event):
        sel = self._tree.selection()
        if not sel: return
        try:
            seq = int(sel[0])
            pkt = self._seq_map.get(seq)
            if pkt: self._detail_popup(pkt)
        except: pass

    def _show_detail(self, pkt):
        """Rich colour-coded packet detail across all 4 pane tabs."""

        def _wset(widget, content_tuples):
            """Insert (text, tag) tuples into a ScrolledText cleanly."""
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            for text, tag in content_tuples:
                widget.insert("end", text, tag)
            widget.configure(state="disabled")
            widget.yview_moveto(0)

        # ── Ensure tags exist ────────────────────────────────────────
        for w in (self._detail_txt, self._hex_txt,
                  self._layer_txt, self._flow_txt):
            try:
                w.tag_config("hdr",  foreground=C["cyan"],
                             font=("Consolas",9,"bold"))
                w.tag_config("key",  foreground=C["text_dim"],
                             font=("Consolas",9))
                w.tag_config("val",  foreground=C["text_hi"],
                             font=("Consolas",9))
                w.tag_config("crit", foreground=C["red"],
                             font=("Consolas",9,"bold"))
                w.tag_config("warn", foreground=C["orange"],
                             font=("Consolas",9,"bold"))
                w.tag_config("ok",   foreground=C["green"],
                             font=("Consolas",9))
                w.tag_config("info", foreground=C["cyan"],
                             font=("Consolas",9))
                w.tag_config("dim",  foreground=C["text_dim"],
                             font=("Consolas",8))
                w.tag_config("sep",  foreground=C["border"],
                             font=("Consolas",8))
                w.tag_config("hex",  foreground=C["green"],
                             font=("Consolas",9))
                w.tag_config("asc",  foreground=C["teal"],
                             font=("Consolas",9))
                w.tag_config("addr", foreground=C["yellow"],
                             font=("Consolas",9,"bold"))
                w.tag_config("port", foreground=C["purple"],
                             font=("Consolas",9,"bold"))
                w.tag_config("flag", foreground=C["orange"],
                             font=("Consolas",9,"bold"))
            except: pass

        def _kv(key, val, val_tag="val"):
            if val is None or val == "" or val == 0: return []
            return [
                (f"  {key:<22}", "key"),
                (f"{val}\n", val_tag),
            ]

        def _section(title):
            bar = "─" * 56
            return [(f"\n  ╔{'═'*(len(title)+2)}╗\n", "sep"),
                    (f"  ║ {title} ║\n", "hdr"),
                    (f"  ╚{'═'*(len(title)+2)}╝\n", "sep")]

        # ════════════════════════════════════════════
        # TAB 1: Full Detail  (colour-coded fields)
        # ════════════════════════════════════════════
        d = []
        # Risk banner
        rs = pkt.risk_score or 0
        risk_tag = "crit" if rs>=70 else "warn" if rs>=40 else "ok"
        risk_bar = "█" * (rs//5) + "░" * (20 - rs//5)
        d += [(f"\n  ┌─ RISK SCORE ──────────────────────────────────┐\n","sep")]
        d += [(f"  │  {risk_bar}  {rs:3d}/100\n","crit" if rs>=70 else "warn" if rs>=40 else "ok")]
        d += [(f"  └───────────────────────────────────────────────┘\n","sep")]

        d += _section("SOURCE DEVICE")
        src_ip   = pkt.src_ip  or "?"
        src_mac  = pkt.eth_src or (pkt.arp_smac or "—")
        src_vend = _mac_vendor(src_mac) if src_mac else "—"
        src_host = self._resolve_host(src_ip, src_mac) or "—"
        src_os   = ttl_os(pkt.ip_ttl) if pkt.ip_ttl else "—"
        src_hops = (64 - pkt.ip_ttl if pkt.ip_ttl and pkt.ip_ttl <= 64 else
                    128 - pkt.ip_ttl if pkt.ip_ttl and pkt.ip_ttl <= 128 else
                    255 - pkt.ip_ttl if pkt.ip_ttl else None)
        d += _kv("IP Address",  src_ip,   "addr")
        d += _kv("MAC Address", src_mac,  "addr")
        d += _kv("Vendor / OUI",src_vend)
        d += _kv("Hostname",    src_host, "info")
        d += _kv("OS Guess",    src_os)
        d += _kv("Est. Hops",   str(src_hops) if src_hops is not None else "")
        d += _kv("Host Port",   str(pkt.sport) if pkt.sport else "")

        d += _section("DESTINATION DEVICE")
        dst_ip   = pkt.dst_ip  or "?"
        dst_mac  = pkt.eth_dst or (pkt.arp_tmac or "—")
        dst_vend = _mac_vendor(dst_mac) if dst_mac else "—"
        dst_host = self._resolve_host(dst_ip, dst_mac) or "—"
        # Special destination labels
        if dst_ip == "255.255.255.255": dst_host = "Broadcast"
        elif dst_ip.startswith("224.") or dst_ip.startswith("239."): dst_host = "Multicast"
        elif dst_ip.endswith(".1") or dst_ip.endswith(".254"): dst_host = dst_host or "Router/Gateway"
        d += _kv("IP Address",  dst_ip,   "addr")
        d += _kv("MAC Address", dst_mac,  "addr")
        d += _kv("Vendor / OUI",dst_vend)
        d += _kv("Hostname",    dst_host, "info")
        d += _kv("Service Port",
                 f"{pkt.dport} ({SERVICE_DB.get(pkt.dport,'?')})" if pkt.dport else "")
        d += _kv("Port Risk",
                 RISK_PORTS.get(pkt.dport,""),
                 "crit" if RISK_PORTS.get(pkt.dport,"")=="Critical" else
                 "warn" if RISK_PORTS.get(pkt.dport,"")=="High" else "ok")

        d += _section("PACKET METADATA")
        d += _kv("Seq #",        f"#{pkt.seq:,}")
        d += _kv("Timestamp",    pkt.ts_str)
        d += _kv("Total Length", f"{pkt.length} bytes")
        d += _kv("Proto Stack",
                 f"{pkt.eth_type_name or '?'} › {pkt.proto or '?'} › {pkt.app_proto or '?'}")
        d += _kv("Flow Key",     pkt.flow_key)

        d += _section("ETHERNET  L2")
        d += _kv("Src MAC",   pkt.eth_src, "addr")
        d += _kv("Dst MAC",   pkt.eth_dst, "addr")
        d += _kv("EtherType", pkt.eth_type_name)
        if pkt.vlan_id:
            d += _kv("VLAN ID", str(pkt.vlan_id), "warn")

        if pkt.ip_proto is not None:
            d += _section("IPv4  L3")
            d += _kv("Src IP",       pkt.src_ip, "addr")
            d += _kv("Dst IP",       pkt.dst_ip, "addr")
            d += _kv("TTL",          str(pkt.ip_ttl))
            d += _kv("Protocol",     pkt.ip_proto_name)
            d += _kv("IP ID",        f"0x{pkt.ip_id:04X}" if pkt.ip_id else "")
            d += _kv("DF/MF Flags",  str(pkt.ip_flags))
            d += _kv("Fragment Off", str(pkt.ip_frag) if pkt.ip_frag else "")
            d += _kv("DSCP",         str(pkt.ip_dscp) if pkt.ip_dscp else "")
            d += _kv("ECN",          str(pkt.ip_ecn)  if pkt.ip_ecn  else "")
            d += _kv("Total Len",    str(pkt.ip_total_len))
            d += _kv("Checksum",     pkt.ip_checksum)

        if pkt.proto == "TCP":
            d += _section("TCP  L4")
            d += _kv("Src Port", str(pkt.sport), "port")
            d += _kv("Dst Port", str(pkt.dport), "port")
            d += _kv("Service",
                     SERVICE_DB.get(pkt.dport, SERVICE_DB.get(pkt.sport,"")))
            d += _kv("Seq Number",  f"{pkt.tcp_seq:,}")
            d += _kv("Ack Number",  f"{pkt.tcp_ack_num:,}")
            d += _kv("Data Offset", str(pkt.tcp_data_off))
            flags_tag = "crit" if "SYN" in (pkt.tcp_flags_str or "") else "flag"
            d += _kv("Flags (raw)", pkt.tcp_flags_raw)
            d += _kv("Flags",       pkt.tcp_flags_str, flags_tag)
            d += _kv("Window",      f"{pkt.tcp_win:,} bytes")
            d += _kv("Checksum",    pkt.tcp_checksum)
            d += _kv("Urgent Ptr",  str(pkt.tcp_urg) if pkt.tcp_urg else "")
            d += _kv("Options",     pkt.tcp_opts)

        elif pkt.proto == "UDP":
            d += _section("UDP  L4")
            d += _kv("Src Port",  str(pkt.sport), "port")
            d += _kv("Dst Port",  str(pkt.dport), "port")
            d += _kv("Service",   SERVICE_DB.get(pkt.dport,
                                   SERVICE_DB.get(pkt.sport,"")))
            d += _kv("UDP Length",str(pkt.udp_len))
            d += _kv("Checksum",  pkt.udp_checksum)

        elif pkt.proto == "ICMP":
            d += _section("ICMP")
            d += _kv("Type",      f"{pkt.icmp_type} — {pkt.icmp_type_name}",
                     "warn" if pkt.icmp_type in (3,5,11) else "val")
            d += _kv("Code",      str(pkt.icmp_code))
            d += _kv("ID",        str(pkt.icmp_id))
            d += _kv("Sequence",  str(pkt.icmp_seq))

        # App-layer
        if pkt.app_proto == "TLS":
            d += _section("TLS  L7")
            tls_tag = "crit" if pkt.tls_ver in ("SSL 2.0","SSL 3.0","TLS 1.0","TLS 1.1") else "ok"
            d += _kv("TLS Version",   pkt.tls_ver, tls_tag)
            d += _kv("Record Type",   pkt.tls_record_type)
            d += _kv("SNI (domain)",  pkt.tls_sni, "info")
            d += _kv("Cipher Suite",  pkt.tls_cipher_suite)

        elif pkt.app_proto == "HTTP":
            d += _section("HTTP  L7")
            d += _kv("Method",       pkt.http_method, "warn")
            d += _kv("URI",          pkt.http_uri,    "info")
            d += _kv("HTTP Version", pkt.http_ver)
            d += _kv("Host",         pkt.http_host,   "addr")
            d += _kv("Status",       pkt.http_status)
            d += _kv("User-Agent",   pkt.http_user_agent)
            d += _kv("Server",       pkt.http_server)
            d += _kv("Content-Type", pkt.http_content_type)
            d += _kv("Content-Len",  pkt.http_content_len)
            if pkt.http_cookie:
                d += _kv("Cookie", pkt.http_cookie[:100]+"…", "warn")
            if pkt.http_headers:
                d += [("\n  All Headers:\n","dim")]
                for hk,hv in list(pkt.http_headers.items())[:15]:
                    d += [(f"    {hk}: {hv}\n","dim")]

        elif pkt.app_proto == "DNS":
            d += _section("DNS  L7")
            d += _kv("Tx ID",    f"0x{pkt.dns_txid:04X}" if pkt.dns_txid else "")
            d += _kv("Type",     pkt.dns_qr, "info")
            d += _kv("Opcode",   str(pkt.dns_opcode))
            d += _kv("Flags",    pkt.dns_flags)
            d += _kv("Rcode",    str(pkt.dns_rcode))
            d += _kv("Auth Ans", str(pkt.dns_aa))
            d += _kv("Truncated",str(pkt.dns_tc))
            dns_q_tag = "crit" if pkt.dns_query and len(pkt.dns_query)>60 else "info"
            d += _kv("Query",    pkt.dns_query, dns_q_tag)
            d += _kv("QType",    pkt.dns_qtype)
            if pkt.dns_answers:
                d += _kv("Answers", ", ".join(pkt.dns_answers), "ok")

        elif pkt.app_proto == "ARP":
            d += _section("ARP")
            d += _kv("Operation",  pkt.arp_op,  "warn" if pkt.arp_op=="Reply" else "val")
            d += _kv("Sender MAC", pkt.arp_smac,"addr")
            d += _kv("Sender IP",  pkt.arp_sip, "addr")
            d += _kv("Target MAC", pkt.arp_tmac,"addr")
            d += _kv("Target IP",  pkt.arp_dip, "addr")

        elif pkt.app_proto == "SSH":
            d += _section("SSH  L7")
            d += _kv("Banner",  pkt.ssh_banner, "ok")
            d += _kv("Version", pkt.ssh_ver)

        elif pkt.app_proto in ("FTP",):
            d += _section("FTP  L7")
            d += _kv("Command",  pkt.ftp_cmd)
            d += _kv("Response", pkt.ftp_resp)

        elif pkt.app_proto in ("SMTP",):
            d += _section("SMTP  L7")
            d += _kv("Command",  pkt.smtp_cmd)
            d += _kv("Response", pkt.smtp_resp)

        # Payload
        d += _section("PAYLOAD ANALYSIS")
        d += _kv("Payload Len",  f"{pkt.payload_len} bytes")
        ent = pkt.payload_entropy or 0
        ent_tag = "crit" if ent>7.4 else "warn" if ent>7.0 else "ok"
        ent_label = ("⚠ HIGH — possible encryption/compression/exfil"
                     if ent>7.2 else "Normal")
        d += _kv("Entropy",
                 f"{ent:.4f}  [{ent_label}]", ent_tag)
        if pkt.payload_ascii:
            d += [("\n  ASCII preview:\n","dim")]
            d += [(f"  {pkt.payload_ascii}\n","asc")]

        # CVE / Security notes — live from Exploit-DB + NVD
        port_for_cve = pkt.dport or pkt.sport
        if port_for_cve:
            cached = _CVE_CACHE.get(f"{port_for_cve}::{''[:20]}")
            if cached:
                live = [c for c in cached if not c.get("error")]
                if live:
                    d += _section("CVE / SECURITY NOTES  (live · exploit-db.com + NVD)")
                    for c in live[:6]:
                        sev   = c.get("severity","?")
                        label = c.get("cve_id") or f"EDB-{c.get('edb_id','')}"
                        title = c.get("title","")[:90]
                        src   = c.get("source","")
                        d += [(f"  ⚠ [{sev}] {label}  ({src})  —  {title}\n","warn")]
                        if c.get("url"):
                            d += [(f"    🔗 {c['url']}\n","dim")]
            else:
                d += _section("CVE / SECURITY NOTES  (live · exploit-db.com + NVD)")
                d += [("  ⏳ Fetching live from exploit-db.com …\n","dim")]
                svc = SERVICE_DB.get(port_for_cve, "")
                fetch_cves_async(port_for_cve, service=svc)

        _wset(self._detail_txt, d)

        # ════════════════════════════════════════════
        # TAB 2: Hex Dump  (Wireshark-style)
        # ════════════════════════════════════════════
        raw = pkt.payload_raw or b""
        h = []
        if raw:
            h += [(f"\n  Payload Hex Dump  ({len(raw)} bytes shown of "
                   f"{pkt.payload_len} total)\n\n","hdr")]
            h += [(f"  Offset   00 01 02 03 04 05 06 07  "
                   f"08 09 0A 0B 0C 0D 0E 0F   ASCII\n","dim")]
            h += [("  " + "─"*74 + "\n","sep")]
            for i in range(0, min(len(raw), 512), 16):
                chunk  = raw[i:i+16]
                h1     = " ".join(f"{b:02X}" for b in chunk[:8])
                h2     = " ".join(f"{b:02X}" for b in chunk[8:])
                asc    = "".join(chr(b) if 32<=b<127 else "·" for b in chunk)
                h += [(f"  {i:04X}   ", "dim")]
                h += [(f"{h1:<23}  {h2:<23}  ","hex")]
                h += [(f" {asc}\n","asc")]
            if len(raw) < (pkt.payload_len or 0):
                h += [(f"\n  … {(pkt.payload_len or 0)-len(raw)} more bytes "
                       f"(truncated to 512)\n","dim")]
        else:
            h = [("  (no payload / header-only packet)\n","dim")]
        _wset(self._hex_txt, h)

        # ════════════════════════════════════════════
        # TAB 3: OSI Layer Stack
        # ════════════════════════════════════════════
        osi_layers = [
            ("L7 Application",  pkt.app_proto or "—",
             pkt.http_uri or pkt.dns_query or pkt.tls_sni or
             pkt.ssh_banner or pkt.ftp_cmd or pkt.smtp_cmd or ""),
            ("L6 Presentation",
             "TLS/SSL" if pkt.tls_ver else "Raw/Plaintext",
             pkt.tls_ver or ("CLEAR — credentials exposed!"
                             if pkt.dport in (23,21) else "")),
            ("L5 Session",      "TCP/UDP Streams",
             f"Flow: {pkt.flow_key or '—'}"),
            ("L4 Transport",    pkt.proto or "—",
             (f"Flags: [{pkt.tcp_flags_str}]  Win: {pkt.tcp_win:,}"
              if pkt.proto=="TCP" else
              f"Len: {pkt.udp_len}" if pkt.proto=="UDP" else
              pkt.icmp_type_name or "")),
            ("L3 Network",      "IPv4",
             f"{pkt.src_ip or '?'} → {pkt.dst_ip or '?'}  "
             f"TTL={pkt.ip_ttl}  ID=0x{pkt.ip_id or 0:04X}"),
            ("L2 Data Link",    "Ethernet II",
             f"{pkt.eth_src} [{_mac_vendor(pkt.eth_src or '')}] → "
             f"{pkt.eth_dst} [{_mac_vendor(pkt.eth_dst or '')}]"
             + (f"  VLAN={pkt.vlan_id}" if pkt.vlan_id else "")),
            ("L1 Physical",     "Wire / Wi-Fi / Fiber", ""),
        ]
        ol = []
        ol += [("\n  ╔══════════════════════════════════════════════════════╗\n","sep")]
        ol += [("  ║              OSI LAYER STACK ANALYSIS                ║\n","hdr")]
        ol += [("  ╚══════════════════════════════════════════════════════╝\n\n","sep")]
        ol += [(f"  {'Layer':<22} {'Protocol':<22} {'Details'}\n","hdr")]
        ol += [("  " + "─"*72 + "\n","sep")]
        for lname, proto2, detail in osi_layers:
            is_app = "L7" in lname
            tag = "info" if is_app else "val"
            ol += [(f"  {lname:<22} ","dim")]
            ol += [(f"{proto2:<22} ", tag)]
            ol += [(f"{detail}\n","dim")]
        ol += [("\n","")]
        # TCP state inference
        if pkt.proto == "TCP" and pkt.tcp_flags_str:
            fl = pkt.tcp_flags_str
            state = ("SYN-SENT (new connection)" if fl=="SYN" else
                     "SYN-ACK (server responding)" if "SYN" in fl and "ACK" in fl else
                     "ESTABLISHED (data transfer)" if fl=="ACK" else
                     "FIN-WAIT (closing)" if "FIN" in fl else
                     "RESET (abrupt close)" if "RST" in fl else
                     "XMAS SCAN (recon)" if all(x in fl for x in ("FIN","URG","PSH")) else
                     "NULL SCAN (recon)" if fl=="NONE" else fl)
            ol += [(f"  TCP State Inference:  {state}\n","warn" if "scan" in state.lower() else "ok")]
        _wset(self._layer_txt, ol)

        # ════════════════════════════════════════════
        # TAB 4: Flow Analysis (threat context)
        # ════════════════════════════════════════════
        fl2 = []
        fl2 += [("\n  ╔══════════════════════════════════════════════════════╗\n","sep")]
        fl2 += [("  ║            FLOW & THREAT ANALYSIS                    ║\n","hdr")]
        fl2 += [("  ╚══════════════════════════════════════════════════════╝\n\n","sep")]

        fl2 += [(f"  Packet #      {pkt.seq:,}\n","val")]
        fl2 += [(f"  Flow Key      {pkt.flow_key or '—'}\n","info")]

        # Full device identity in flow tab
        src_ip  = pkt.src_ip or "?"
        dst_ip  = pkt.dst_ip or "?"
        src_mac = pkt.eth_src or ""
        dst_mac = pkt.eth_dst or ""
        src_host= self._resolve_host(src_ip, src_mac) or "—"
        dst_host= self._resolve_host(dst_ip, dst_mac) or "—"
        src_vend= _mac_vendor(src_mac) or "—"
        dst_vend= _mac_vendor(dst_mac) or "—"
        src_os  = ttl_os(pkt.ip_ttl) if pkt.ip_ttl else "—"

        fl2 += [("\n  SOURCE\n","hdr")]
        fl2 += [(f"  IP       {src_ip}\n","addr")]
        fl2 += [(f"  MAC      {src_mac or '—'}\n","val")]
        fl2 += [(f"  Vendor   {src_vend}\n","dim")]
        fl2 += [(f"  Host     {src_host}\n","info")]
        fl2 += [(f"  OS       {src_os}\n","dim")]
        fl2 += [(f"  Port     {pkt.sport or '—'}\n","port")]

        fl2 += [("\n  DESTINATION\n","hdr")]
        fl2 += [(f"  IP       {dst_ip}\n","addr")]
        fl2 += [(f"  MAC      {dst_mac or '—'}\n","val")]
        fl2 += [(f"  Vendor   {dst_vend}\n","dim")]
        fl2 += [(f"  Host     {dst_host}\n","info")]
        svc  = SERVICE_DB.get(pkt.dport,"?")
        fl2 += [(f"  Port     {pkt.dport or '—'} ({svc})\n","port")]
        fl2 += [("\n","")]

        fl2 += [(f"  Direction     {src_ip}:{pkt.sport}  →  "
                 f"{dst_ip}:{pkt.dport}\n","addr")]
        fl2 += [(f"  Proto Stack   {pkt.eth_type_name or '?'} › "
                 f"{pkt.proto or '?'} › {pkt.app_proto or '?'}\n","val")]
        fl2 += [(f"  Risk Score    {rs}/100  ", risk_tag)]
        fl2 += [(f"{'▓'*(rs//5)}{'░'*(20-rs//5)}\n\n", risk_tag)]

        # Entropy analysis
        if ent > 0:
            fl2 += [("  ENTROPY ANALYSIS\n","hdr")]
            fl2 += [(f"  Value:    {ent:.6f} bits/byte\n","val")]
            fl2 += [(f"  Category: ","dim")]
            if ent > 7.6:
                fl2 += [("HIGH — almost certainly encrypted/compressed\n","crit")]
                fl2 += [("  Threat:   Possible data exfiltration or C2 tunnelling\n","warn")]
            elif ent > 7.2:
                fl2 += [("ELEVATED — encryption or high compression\n","warn")]
            elif ent > 5.0:
                fl2 += [("NORMAL — typical protocol/text data\n","ok")]
            else:
                fl2 += [("LOW — structured/repetitive data\n","ok")]
            fl2 += [("\n","")]

        # Port intelligence
        svc = SERVICE_DB.get(pkt.dport, SERVICE_DB.get(pkt.sport,""))
        risk_p = RISK_PORTS.get(pkt.dport, RISK_PORTS.get(pkt.sport,""))
        if svc or risk_p:
            fl2 += [("  PORT INTELLIGENCE\n","hdr")]
            fl2 += [(f"  Service:  {svc}\n","val")]
            pt = "crit" if risk_p=="Critical" else "warn" if risk_p=="High" else "ok"
            fl2 += [(f"  Port Risk: {risk_p}\n",pt)]
            fl2 += [("\n","")]

        # CVE / Security notes — live from Exploit-DB + NVD
        port_for_cve2 = pkt.dport or pkt.sport
        if port_for_cve2:
            cached2 = _CVE_CACHE.get(f"{port_for_cve2}::{''[:20]}")
            if cached2:
                live2 = [c for c in cached2 if not c.get("error")]
                if live2:
                    fl2 += [("  CVE / KNOWN VULNERABILITIES  (live · exploit-db.com + NVD)\n","hdr")]
                    for c in live2[:5]:
                        sev   = c.get("severity","?")
                        label = c.get("cve_id") or f"EDB-{c.get('edb_id','')}"
                        title = c.get("title","")[:85]
                        src   = c.get("source","")
                        fl2 += [(f"  ⚠ [{sev}] {label}  ({src})  —  {title}\n","warn")]
                        if c.get("url"):
                            fl2 += [(f"    🔗 {c['url']}\n","dim")]
                    fl2 += [("\n","")]
            else:
                fl2 += [("  CVE / KNOWN VULNERABILITIES  (live · exploit-db.com + NVD)\n","hdr")]
                fl2 += [("  ⏳ Fetching live from exploit-db.com …\n","dim")]
                fl2 += [("\n","")]
                svc2 = SERVICE_DB.get(port_for_cve2, "")
                fetch_cves_async(port_for_cve2, service=svc2)

        # Active alerts on this flow
        alerts_flow = [a for a in self.app.engine.get_alerts(200)
                       if a.src == pkt.src_ip or a.dst == pkt.dst_ip]
        if alerts_flow:
            fl2 += [("  ACTIVE ALERTS ON THIS HOST\n","hdr")]
            for a in alerts_flow[-5:]:
                t = "crit" if a.severity=="CRITICAL" else "warn"
                fl2 += [(f"  [{a.severity}] {a.rule}: {a.title}\n",t)]
            fl2 += [("\n","")]

        # MITRE ATT&CK hints
        mitre = []
        if pkt.dport in (4444,31337,1337):
            mitre.append("T1219 Remote Access Software")
        if pkt.tcp_flags_str and "SYN" in pkt.tcp_flags_str and "ACK" not in (pkt.tcp_flags_str or ""):
            mitre.append("T1046 Network Service Discovery (SYN scan indicator)")
        if pkt.app_proto == "DNS" and pkt.dns_query and len(pkt.dns_query)>60:
            mitre.append("T1071.004 Application Layer Protocol: DNS (tunnel)")
        if pkt.payload_entropy and pkt.payload_entropy > 7.4:
            mitre.append("T1030 Data Transfer Size Limits / T1048 Exfiltration")
        if pkt.dport in (23,21) and pkt.payload_ascii:
            mitre.append("T1040 Network Sniffing (cleartext creds)")
        if mitre:
            fl2 += [("  MITRE ATT&CK INDICATORS\n","hdr")]
            for m in mitre:
                fl2 += [(f"  › {m}\n","info")]

        _wset(self._flow_txt, fl2)

        # ════════════════════════════════════════════
        # TAB 5: HTTP Inspector (only for HTTP packets)
        # ════════════════════════════════════════════
        self._http_txt.configure(state="normal")
        self._http_txt.delete("1.0", "end")
        if pkt.app_proto == "HTTP" or pkt.dport in (80,8080,8000,3000,8008,8888) \
                or pkt.sport in (80,8080,8000,3000,8008,8888):
            http_detail = build_http_detail_text(pkt)
            for text, tag in http_detail:
                if tag:
                    self._http_txt.insert("end", text, tag)
                else:
                    self._http_txt.insert("end", text)
        else:
            self._http_txt.insert("end",
                f"\n  (Not an HTTP packet — proto={pkt.app_proto or pkt.proto})\n\n"
                "  HTTP Inspector shows:\n"
                "  • Full request/response analysis\n"
                "  • Attack signature detection (SQLi, XSS, RCE, Path Traversal...)\n"
                "  • Header security audit\n"
                "  • Query parameter inspection\n"
                "  • Cookie analysis\n"
                "  • User-Agent profiling\n"
                "  • MITRE ATT&CK mapping\n\n"
                "  Select an HTTP packet (port 80/8080/8000) to activate.",
                "dim")
        self._http_txt.configure(state="disabled")
        self._http_txt.yview_moveto(0)

    def _detail_popup(self, pkt):
        """Full packet detail in a professional tabbed popup window."""
        w = tk.Toplevel(self.app)
        w.title(f"Packet #{pkt.seq}  ·  {pkt.proto}/{pkt.app_proto}  ·  "
                f"{pkt.src_ip}→{pkt.dst_ip}")
        w.configure(bg=C["bg"]); w.geometry("1280x820")
        w.resizable(True, True)

        rs  = pkt.risk_score or 0
        rc  = C["red"] if rs>=70 else C["orange"] if rs>=40 else C["green"]
        threats = analyze_http_security(pkt)
        tk.Frame(w, bg=rc, height=4).pack(fill="x")

        # ── Header bar ──────────────────────────────────────────────
        hf = tk.Frame(w, bg=C["panel"]); hf.pack(fill="x")
        tk.Label(hf,
                 text=f"  📦  #{pkt.seq}  |  {pkt.ts_str}  |  "
                      f"{pkt.proto}/{pkt.app_proto}  |  "
                      f"{pkt.src_ip}:{pkt.sport} → {pkt.dst_ip}:{pkt.dport}  |  "
                      f"Risk {rs}/100"
                      + (f"  |  ⚠ {len(threats)} HTTP Threats" if threats else ""),
                 bg=C["panel"], fg=rc,
                 font=("Segoe UI Semibold",11)).pack(side="left",padx=12,pady=6)

        nb2 = ttk.Notebook(w); nb2.pack(fill="both",expand=True,padx=6,pady=4)

        # ── Tab 1: Full structured JSON fields ──────────────────────
        sf = tk.Frame(nb2, bg=C["bg2"]); nb2.add(sf, text="  📋 Fields  ")
        st = scrolledtext.ScrolledText(sf, bg=C["bg"], fg=C["text"],
                                        font=("Consolas",9), relief="flat",wrap="none")
        st.pack(fill="both",expand=True,padx=4,pady=4)
        data_str = json.dumps(
            {k: getattr(pkt,k) for k in pkt.__slots__
             if getattr(pkt,k) is not None
             and k not in ("payload_raw","http_headers","dns_answers")},
            indent=2, default=str)
        st.insert("end", data_str)
        st.configure(state="disabled")

        # ── Tab 2: Enhanced Hex Dump ─────────────────────────────────
        hf2 = tk.Frame(nb2, bg=C["bg2"]); nb2.add(hf2, text="  🔢 Hex Dump  ")
        ht  = scrolledtext.ScrolledText(hf2, bg=C["bg"], fg=C["green"],
                                         font=("Consolas",9), relief="flat",wrap="none")
        ht.pack(fill="both",expand=True,padx=4,pady=4)
        ht.tag_config("hex",  foreground=C["green"])
        ht.tag_config("asc",  foreground=C["teal"])
        ht.tag_config("dim",  foreground=C["text_dim"])
        ht.tag_config("sep",  foreground=C["border"])
        ht.tag_config("hdr",  foreground=C["cyan"], font=("Consolas",9,"bold"))
        raw = pkt.payload_raw or b""
        if raw:
            ht.insert("end",
                f"\n  Payload Hex Dump — {len(raw)} bytes shown"
                f" of {pkt.payload_len or len(raw)} total\n\n","hdr")
            ht.insert("end",
                f"  Offset   00 01 02 03 04 05 06 07  "
                f"08 09 0A 0B 0C 0D 0E 0F   ASCII\n","dim")
            ht.insert("end", "  " + "─"*74 + "\n","sep")
            for i in range(0, min(len(raw),1024), 16):
                chunk = raw[i:i+16]
                h1  = " ".join(f"{b:02X}" for b in chunk[:8])
                h2  = " ".join(f"{b:02X}" for b in chunk[8:])
                asc = "".join(chr(b) if 32<=b<127 else "·" for b in chunk)
                ht.insert("end", f"  {i:04X}   ","dim")
                ht.insert("end", f"{h1:<23}  {h2:<23}  ","hex")
                ht.insert("end", f" {asc}\n","asc")
            if len(raw) < (pkt.payload_len or 0):
                ht.insert("end",
                    f"\n  … {pkt.payload_len - len(raw)} more bytes (truncated)\n","dim")
        else:
            ht.insert("end", "\n  (no payload / header-only packet)\n")
        ht.configure(state="disabled")

        # ── Tab 3: HTTP Inspector ────────────────────────────────────
        http_tab = tk.Frame(nb2, bg=C["bg2"])
        nb2.add(http_tab, text="  🌐 HTTP Inspector  " +
                ("⚠" if threats else ""))
        http_st = scrolledtext.ScrolledText(
            http_tab, bg=C["bg"], fg=C["text"],
            font=("Consolas",9), relief="flat", wrap="word")
        http_st.pack(fill="both",expand=True,padx=4,pady=4)
        for tag, fg2, style in [
            ("hdr",C["cyan"],"bold"),("val",C["text_hi"],""),
            ("crit",C["red"],"bold"),("warn",C["orange"],"bold"),
            ("ok",C["green"],""),("info",C["cyan"],""),
            ("dim",C["text_dim"],""),("sep",C["border"],""),
            ("addr",C["yellow"],"bold"),("asc",C["teal"],""),
            ("port",C["purple"],"bold"),("flag",C["orange"],"bold"),
            ("hex",C["green"],""),("key",C["text_dim"],""),
        ]:
            http_st.tag_config(tag, foreground=fg2,
                font=("Consolas",9,style) if style else ("Consolas",9))

        if pkt.app_proto == "HTTP" or pkt.dport in (80,8080,8000,3000,8008,8888) \
                or pkt.sport in (80,8080,8000,3000,8008,8888):
            for text, tag in build_http_detail_text(pkt):
                if tag: http_st.insert("end", text, tag)
                else:   http_st.insert("end", text)
        else:
            http_st.insert("end",
                f"\n  Proto: {pkt.app_proto or pkt.proto or '?'} — not HTTP\n\n"
                "  Switch to an HTTP packet (port 80/8080/8000)\n"
                "  to see full web request analysis here.\n","dim")
        http_st.configure(state="disabled")

        # ── Tab 4: GeoIP / WHOIS lookup ──────────────────────────────
        geo_tab = tk.Frame(nb2, bg=C["bg2"]); nb2.add(geo_tab, text="  🌍 GeoIP / WHOIS  ")
        geo_top = tk.Frame(geo_tab, bg=C["panel2"]); geo_top.pack(fill="x", pady=3)
        self._geo_result = scrolledtext.ScrolledText(
            geo_tab, bg=C["bg"], fg=C["text"],
            font=("Consolas",9), relief="flat", wrap="word")
        self._geo_result.pack(fill="both", expand=True, padx=4, pady=4)

        def _do_geo_lookup(ip):
            self._geo_result.configure(state="normal")
            self._geo_result.delete("1.0","end")
            self._geo_result.insert("end", f"\n  Looking up {ip} …\n","dim")
            self._geo_result.configure(state="disabled")
            def _run():
                results = []
                # ip-api.com free JSON lookup (no key required)
                try:
                    url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,query,lat,lon,timezone,mobile,proxy,hosting"
                    req = urllib.request.Request(url, headers={"User-Agent":"ReconShield/4.0"})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                    if data.get("status") == "success":
                        results += [
                            ("  ╔═ GEOLOCATION ══════════════════════════════════╗\n","hdr"),
                            (f"  ║  IP:        {data.get('query','?')}\n","val"),
                            (f"  ║  Country:   {data.get('country','?')}\n","val"),
                            (f"  ║  Region:    {data.get('regionName','?')}\n","val"),
                            (f"  ║  City:      {data.get('city','?')}\n","val"),
                            (f"  ║  ISP:       {data.get('isp','?')}\n","addr"),
                            (f"  ║  Org:       {data.get('org','?')}\n","addr"),
                            (f"  ║  AS:        {data.get('as','?')}\n","dim"),
                            (f"  ║  Timezone:  {data.get('timezone','?')}\n","dim"),
                            (f"  ║  Coords:    {data.get('lat','?')}, {data.get('lon','?')}\n","dim"),
                        ]
                        flags = []
                        if data.get("proxy"):  flags.append("⚠ PROXY DETECTED")
                        if data.get("hosting"): flags.append("⚠ DATACENTER/HOSTING")
                        if data.get("mobile"):  flags.append("ℹ Mobile Network")
                        for flag in flags:
                            col = "crit" if "PROXY" in flag or "HOSTING" in flag else "info"
                            results += [(f"  ║  {flag}\n", col)]
                        results += [("  ╚═══════════════════════════════════════════════╝\n","hdr")]
                    else:
                        results += [(f"\n  GeoIP lookup failed: {data.get('message','?')}\n","warn")]
                except Exception as e:
                    results += [(f"\n  GeoIP lookup error: {e}\n  (Check internet connection)\n","warn")]

                # Reverse DNS
                try:
                    rdn = socket.gethostbyaddr(ip)[0]
                    results += [("\n  REVERSE DNS\n","hdr"),
                                (f"  PTR: {rdn}\n","info")]
                except:
                    results += [("\n  REVERSE DNS: no PTR record\n","dim")]

                # Local network check
                try:
                    addr = ipaddress.ip_address(ip)
                    if addr.is_private:
                        results += [("\n  ℹ PRIVATE/RFC-1918 ADDRESS — no public GeoIP\n","info")]
                    if addr.is_loopback:
                        results += [("  ℹ LOOPBACK address\n","dim")]
                    if addr.is_multicast:
                        results += [("  ℹ MULTICAST address\n","dim")]
                except: pass

                def _update():
                    self._geo_result.configure(state="normal")
                    self._geo_result.delete("1.0","end")
                    for tag2,col2 in [("hdr",C["cyan"]),("val",C["text_hi"]),
                                      ("addr",C["yellow"]),("dim",C["text_dim"]),
                                      ("info",C["cyan"]),("warn",C["orange"]),
                                      ("crit",C["red"])]:
                        self._geo_result.tag_config(tag2, foreground=col2,
                            font=("Consolas",9))
                    self._geo_result.insert("end", f"\n  GeoIP + RDNS for: {ip}\n\n","hdr")
                    for txt, col2 in results:
                        self._geo_result.insert("end", txt, col2)
                    self._geo_result.configure(state="disabled")
                try: w.after(0, _update)
                except: pass
            threading.Thread(target=_run, daemon=True).start()

        btn_row = tk.Frame(geo_top, bg=C["panel2"]); btn_row.pack(fill="x", padx=6)
        Btn(btn_row, f"🌍 Lookup SRC: {pkt.src_ip or '?'}",
            lambda: _do_geo_lookup(pkt.src_ip or ""),
            bg=C["btn_b"], fg=C["blue"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="left", padx=3)
        Btn(btn_row, f"🌍 Lookup DST: {pkt.dst_ip or '?'}",
            lambda: _do_geo_lookup(pkt.dst_ip or ""),
            bg=C["btn_b"], fg=C["blue"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="left", padx=3)
        self._geo_result.configure(state="normal")
        self._geo_result.insert("end",
            "\n  Click a Lookup button above to query GeoIP + Reverse DNS.\n\n"
            "  Data provided by ip-api.com (free, no API key required).\n"
            "  Includes: Country, City, ISP, ASN, Proxy/VPN detection,\n"
            "  Datacenter detection, Mobile network flag.\n","dim")
        self._geo_result.configure(state="disabled")

        # ── Tab 5: Raw JSON ──────────────────────────────────────────
        jf = tk.Frame(nb2, bg=C["bg2"]); nb2.add(jf, text="  { } Raw JSON  ")
        jt = scrolledtext.ScrolledText(jf, bg=C["bg"], fg=C["cyan"],
                                        font=("Consolas",9), relief="flat")
        jt.pack(fill="both",expand=True,padx=4,pady=4)
        full_dict = {k: getattr(pkt,k) for k in pkt.__slots__
                     if getattr(pkt,k) is not None and k!="payload_raw"}
        if threats:
            full_dict["http_threats"] = [
                {"category":c,"severity":s,"match":det} for c,s,det in threats]
        jt.insert("end", json.dumps(full_dict, indent=2, default=str))
        jt.configure(state="disabled")

        # ── Bottom action bar ────────────────────────────────────────
        bf = tk.Frame(w, bg=C["bg"]); bf.pack(fill="x", pady=4)
        Btn(bf,"🤖 Ask AI",
            lambda: self._ask_ai_pkt(pkt,w),
            bg=C["btn_g"],fg=C["green"]).pack(side="left",padx=10)
        if threats:
            Btn(bf, f"⚠ {len(threats)} HTTP Threats Detected",
                lambda: nb2.select(http_tab),
                bg=C["btn_r"], fg=C["red"]).pack(side="left", padx=4)
        Btn(bf,"📋 Copy Info",
            lambda: (w.clipboard_clear(), w.clipboard_append(
                f"#{pkt.seq} {pkt.ts_str} {pkt.src_ip}:{pkt.sport}"
                f"→{pkt.dst_ip}:{pkt.dport} [{pkt.app_proto}] {pkt.info}")),
            bg=C["btn"],fg=C["text_hi"]).pack(side="left",padx=4)
        Btn(bf,"✖ Close",w.destroy,
            bg=C["btn_r"],fg=C["red"]).pack(side="right",padx=10)

        # Auto-switch to HTTP tab if packet is HTTP
        if pkt.app_proto == "HTTP" or pkt.dport in (80,8080,8000,3000,8008,8888):
            nb2.select(http_tab)

    def _ask_ai_pkt(self, pkt, parent=None):
        self.app.nb.select(self.app.tab_ai)
        threats = analyze_http_security(pkt)
        threat_str = ""
        if threats:
            threat_str = "\n  HTTP SECURITY THREATS:\n"
            for cat, sev, detail in threats:
                threat_str += f"    [{sev}] {cat}: {detail[:80]}\n"
        q = (f"Analyse this captured network packet:\n"
             f"  #{pkt.seq} | {pkt.ts_str} | {pkt.proto}/{pkt.app_proto}\n"
             f"  {pkt.src_ip}:{pkt.sport} → {pkt.dst_ip}:{pkt.dport}\n"
             f"  Flags: {pkt.tcp_flags_str}  Len: {pkt.length}  "
             f"TTL: {pkt.ip_ttl}  Entropy: {pkt.payload_entropy}\n"
             f"  Risk Score: {pkt.risk_score}/100\n"
             f"  Info: {pkt.info}\n"
             f"  DNS: {pkt.dns_query}  TLS-SNI: {pkt.tls_sni}\n"
             f"  HTTP: {pkt.http_method} {pkt.http_uri}"
             f"  Host: {pkt.http_host}  UA: {pkt.http_user_agent}\n"
             f"  HTTP Status: {pkt.http_status}  Server: {pkt.http_server}\n"
             f"{threat_str}\n"
             f"Provide a detailed security analysis:\n"
             f"1. Is this packet suspicious or malicious?\n"
             f"2. What attack technique does this represent (if any)?\n"
             f"3. MITRE ATT&CK technique IDs\n"
             f"4. CVEs that may be relevant\n"
             f"5. Recommended response/remediation")
        ctx = self.app.ai.build_context(self.app.host_db,
              self.app.engine.get_alerts(20),
              self.app.cap_stats, self.app.engine)
        self.app.tab_ai._send(q, ctx)
        if parent: parent.destroy()

    def _pkt_context_menu(self, event):
        """Right-click context menu on packet rows."""
        row = self._tree.identify_row(event.y)
        if not row: return
        self._tree.selection_set(row)
        try:
            seq = int(row)
            pkt = self._seq_map.get(seq)
        except: return
        if not pkt: return

        threats = analyze_http_security(pkt)
        menu = tk.Menu(self, tearoff=0,
                       bg=C["card"], fg=C["text_hi"],
                       activebackground=C["tsel"],
                       activeforeground=C["cyan"],
                       font=("Segoe UI", 9))
        proto = pkt.app_proto or pkt.proto or "?"
        menu.add_command(
            label=f"  📦 #{pkt.seq}  {pkt.src_ip}:{pkt.sport} → {pkt.dst_ip}:{pkt.dport}  [{proto}]",
            state="disabled")
        menu.add_separator()
        menu.add_command(label="  🔍 Full Packet Detail (double-click)",
                         command=lambda: self._detail_popup(pkt))
        menu.add_command(label="  🤖 Ask AI Analyst",
                         command=lambda: self._ask_ai_pkt(pkt))
        if pkt.app_proto == "HTTP" or pkt.dport in (80,8080,8000,3000,8008,8888):
            menu.add_command(
                label=f"  🌐 HTTP Inspector" + (f"  ⚠ {len(threats)} threats" if threats else ""),
                command=lambda: self._detail_popup(pkt))
        menu.add_separator()
        menu.add_command(label="  🔎 Filter by Source IP",
                         command=lambda: self._filt_ip.set(pkt.src_ip or ""))
        menu.add_command(label="  🔎 Filter by Dest IP",
                         command=lambda: self._filt_ip.set(pkt.dst_ip or ""))
        if pkt.dport:
            menu.add_command(label=f"  🔎 Filter by Port {pkt.dport}",
                             command=lambda: self._filt_port.set(str(pkt.dport)))
        menu.add_command(label=f"  🔎 Filter by Proto {proto}",
                         command=lambda: self._filt_proto.set(proto if proto in
                             ["TCP","UDP","DNS","HTTP","TLS","ICMP","ARP","DHCP","SSH","FTP","SMTP"]
                             else "ALL"))
        menu.add_separator()
        menu.add_command(label="  📋 Copy SRC IP",
                         command=lambda: (self.clipboard_clear(),
                                          self.clipboard_append(pkt.src_ip or "")))
        menu.add_command(label="  📋 Copy DST IP",
                         command=lambda: (self.clipboard_clear(),
                                          self.clipboard_append(pkt.dst_ip or "")))
        if pkt.http_uri:
            menu.add_command(label="  📋 Copy HTTP URI",
                             command=lambda: (self.clipboard_clear(),
                                              self.clipboard_append(pkt.http_uri)))
        if pkt.dns_query:
            menu.add_command(label=f"  📋 Copy DNS Query: {pkt.dns_query[:30]}",
                             command=lambda: (self.clipboard_clear(),
                                              self.clipboard_append(pkt.dns_query)))
        if pkt.tls_sni:
            menu.add_command(label=f"  📋 Copy TLS SNI: {pkt.tls_sni[:30]}",
                             command=lambda: (self.clipboard_clear(),
                                              self.clipboard_append(pkt.tls_sni)))
        menu.tk_popup(event.x_root, event.y_root)

    def _check_engine_error(self):
        err = self.app.cap_stats.get("error", "")
        if err:
            self.app.cap_stats.pop("error", None)
            self._cap_status.set("❌  Capture failed")
            msg = err
            if "Permission" in err or "denied" in err.lower():
                msg += ("\n\n─── HOW TO FIX ───\n"
                        "Windows: Right-click ReconShield.py → Run as Administrator\n"
                        "Linux  : sudo python3 ReconShield.py\n\n"
                        "For full network capture (all devices):\n"
                        "  pip install scapy\n"
                        "  + Install Npcap from https://npcap.com/#download")
            messagebox.showerror("Capture Error", msg)

    def _clear_pkts(self):
        self._tree.delete(*self._tree.get_children())
        self._pkts.clear()
        self._seq_map.clear()
        self._session_tracker.clear()
        self._http_threat_count = 0
        try:
            self._sess_tree.delete(*self._sess_tree.get_children())
            self._sess_count_var.set("Sessions: 0")
        except: pass
        for v in self._sv.values(): v.set("0")

    def _export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON (full detail)","*.json"),
                       ("CSV (tabular)","*.csv"),
                       ("Security Report (text)","*.txt")])
        if not path: return
        pkts_list = list(self._pkts)

        if path.endswith(".csv"):
            import csv
            with open(path,"w",newline="",encoding="utf-8") as f:
                w2 = csv.writer(f)
                w2.writerow(["Seq","Time","SrcIP","DstIP","Proto","App",
                              "SPort","DPort","Len","TTL","Flags",
                              "Entropy","RiskScore","DNS_Query","HTTP_Method",
                              "HTTP_URI","HTTP_Host","HTTP_Status","HTTP_UA",
                              "TLS_SNI","TLS_Ver","SSH_Banner",
                              "HTTP_Threats","Info"])
                for pkt in pkts_list:
                    threats = analyze_http_security(pkt)
                    threat_str = "; ".join(f"[{s}]{c}" for c,s,_ in threats)
                    w2.writerow([
                        pkt.seq, pkt.ts_str, pkt.src_ip, pkt.dst_ip,
                        pkt.proto, pkt.app_proto, pkt.sport, pkt.dport,
                        pkt.length, pkt.ip_ttl, pkt.tcp_flags_str,
                        pkt.payload_entropy, pkt.risk_score,
                        pkt.dns_query, pkt.http_method, pkt.http_uri,
                        pkt.http_host, pkt.http_status, pkt.http_user_agent,
                        pkt.tls_sni, pkt.tls_ver, pkt.ssh_banner,
                        threat_str, pkt.info,
                    ])

        elif path.endswith(".txt"):
            # Human-readable security report
            with open(path,"w",encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("  RECONSHIELD v1.0 — SECURITY CAPTURE REPORT\n")
                f.write(f"  Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  Packets analyzed: {len(pkts_list):,}\n")
                f.write("=" * 80 + "\n\n")

                # Protocol breakdown
                proto_cnt = collections.Counter(
                    (p.app_proto or p.proto or "?") for p in pkts_list)
                f.write("PROTOCOL BREAKDOWN\n" + "-"*40 + "\n")
                for proto, cnt in proto_cnt.most_common(15):
                    f.write(f"  {proto:<20} {cnt:>8,}\n")
                f.write("\n")

                # Threat summary
                all_threats = []
                for pkt in pkts_list:
                    ts = analyze_http_security(pkt)
                    for cat, sev, detail in ts:
                        all_threats.append({
                            "time": pkt.ts_str,
                            "src":  pkt.src_ip,
                            "dst":  f"{pkt.dst_ip}:{pkt.dport}",
                            "category": cat, "severity": sev,
                            "uri": pkt.http_uri or "",
                            "detail": detail,
                        })
                if all_threats:
                    f.write(f"HTTP SECURITY THREATS ({len(all_threats)} detected)\n")
                    f.write("-"*40 + "\n")
                    for t in all_threats[:200]:
                        f.write(f"  [{t['severity']}] {t['category']}\n")
                        f.write(f"    Time:   {t['time']}\n")
                        f.write(f"    Source: {t['src']} → {t['dst']}\n")
                        if t["uri"]:
                            f.write(f"    URI:    {t['uri'][:100]}\n")
                        f.write(f"    Match:  {t['detail']}\n\n")

                # Alert summary
                alerts = self.app.engine.get_alerts(500)
                if alerts:
                    f.write(f"\nTHREAT ENGINE ALERTS ({len(alerts)} total)\n")
                    f.write("-"*40 + "\n")
                    for a in alerts:
                        f.write(f"  [{a.severity}] {a.rule} — {a.title}\n")
                        f.write(f"    {a.ts_str}  {a.src} → {a.dst}\n")
                        f.write(f"    {a.desc}\n")
                        if a.mitre:
                            f.write(f"    MITRE: {a.mitre}\n")
                        f.write("\n")

                # Session summary
                sessions = self._session_tracker.get_sessions(500)
                if sessions:
                    f.write(f"\nTCP SESSION SUMMARY ({len(sessions)} sessions)\n")
                    f.write("-"*40 + "\n")
                    for s in sessions:
                        f.write(f"  {s['flow_key']}\n")
                        f.write(f"    Proto={s['proto']} State={s['state']} "
                                f"Pkts={s['packets']} Bytes={s['bytes']:,} "
                                f"HTTP={len(s['http_reqs'])}\n")
                        for req in s["http_reqs"][:5]:
                            f.write(f"      {req['method']} {req['uri'][:80]}\n")
                f.write("\n" + "="*80 + "\nEND OF REPORT\n")

        else:
            # Full JSON dump with HTTP threat annotations
            data = []
            for p in pkts_list[-10000:]:
                d = {k: getattr(p,k) for k in p.__slots__
                     if getattr(p,k) is not None and k not in ("payload_raw",)}
                threats = analyze_http_security(p)
                if threats:
                    d["http_threats"] = [
                        {"category":c,"severity":s,"match":det}
                        for c,s,det in threats
                    ]
                data.append(d)
            # Add session data
            export = {
                "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "tool": "ReconShield v1.0",
                "packet_count": len(pkts_list),
                "sessions": [
                    {k:v for k,v in s.items() if k not in ("flags_seen",)}
                    for s in self._session_tracker.get_sessions(500)
                ],
                "packets": data,
            }
            with open(path,"w",encoding="utf-8") as f:
                json.dump(export, f, indent=2, default=str)

        messagebox.showinfo("Exported",
                            f"✅ Saved {len(pkts_list):,} packets → {path}")

    def _proto_chart(self):
        if not MPLOT:
            messagebox.showinfo("Missing","pip install matplotlib"); return
        s    = self.app.cap_stats
        pkts = list(self._pkts)
        if not pkts: messagebox.showinfo("No data","Start capturing first"); return

        w2  = tk.Toplevel(self.app)
        w2.title("Traffic Statistics — ReconShield v1.0")
        w2.configure(bg=C["bg"]); w2.geometry("1300x860")
        w2.resizable(True,True)

        tk.Frame(w2, bg=C["cyan"], height=3).pack(fill="x")
        hf2 = tk.Frame(w2, bg=C["panel"]); hf2.pack(fill="x")
        tk.Label(hf2, text=f"  📊 Traffic Statistics  ·  {len(pkts):,} packets analysed",
                 bg=C["panel"], fg=C["cyan"],
                 font=("Segoe UI Semibold",12)).pack(side="left",padx=12,pady=7)
        Btn(hf2, "✖ Close", w2.destroy,
            bg=C["btn_r"], fg=C["red"],
            font=("Segoe UI",8), padx=8, pady=3).pack(side="right",padx=10)

        fig2 = Figure(figsize=(14,9), facecolor=C["bg"])
        fig2.subplots_adjust(hspace=0.45, wspace=0.35,
                             left=0.06, right=0.97, top=0.94, bottom=0.07)

        PAL = [C["blue"],C["green"],C["yellow"],C["orange"],C["purple"],
               C["cyan"],C["teal"],C["pink"],C["lime"],C["red"],C["indigo"],C["gold"]]

        def _cs(ax, title, col):
            ax.set_title(title, color=col, fontsize=8, fontweight="bold", pad=4)
            ax.tick_params(colors=C["text_dim"], labelsize=6)
            ax.set_facecolor(C["bg"])
            for sp in ax.spines.values(): sp.set_edgecolor(C["sep"])
            ax.xaxis.label.set_color(C["text_dim"])
            ax.yaxis.label.set_color(C["text_dim"])

        # ── 1: Protocol pie ─────────────────────────────────────────
        ax1 = fig2.add_subplot(3,4,1)
        protos = {k:v for k,v in s.items()
                  if k not in ("total","bytes","error","warn","iface","method")
                  and isinstance(v,int) and v>0}
        if protos:
            keys = list(protos.keys()); vals=[protos[k] for k in keys]
            wedges,_,autotexts = ax1.pie(
                vals, labels=keys, colors=PAL[:len(keys)],
                autopct="%1.1f%%", startangle=140,
                textprops={"color":C["text_dim"],"fontsize":5.5},
                wedgeprops={"edgecolor":C["sep"],"linewidth":0.5})
            for at in autotexts: at.set_fontsize(5)
        _cs(ax1, "Protocol Mix", C["cyan"])

        # ── 2: Top source IPs ───────────────────────────────────────
        ax2 = fig2.add_subplot(3,4,2)
        src_cnt = collections.Counter(p.src_ip for p in pkts if p.src_ip)
        if src_cnt:
            top_src = src_cnt.most_common(8)
            ips_s = [x[0][-14:] for x in top_src]
            cnts_s= [x[1] for x in top_src]
            ax2.barh(ips_s, cnts_s, color=C["blue"],
                     edgecolor=C["sep"], linewidth=0.3, height=0.6)
            for i,(ip,c) in enumerate(zip(ips_s,cnts_s)):
                ax2.text(c+max(cnts_s)*0.01, i, str(c),
                         va="center", color=C["text_dim"], fontsize=5.5)
        _cs(ax2, "Top Source IPs", C["blue"])

        # ── 3: Top dest IPs ─────────────────────────────────────────
        ax3 = fig2.add_subplot(3,4,3)
        dst_cnt = collections.Counter(p.dst_ip for p in pkts if p.dst_ip)
        if dst_cnt:
            top_dst = dst_cnt.most_common(8)
            ips_d = [x[0][-14:] for x in top_dst]
            cnts_d= [x[1] for x in top_dst]
            ax3.barh(ips_d, cnts_d, color=C["purple"],
                     edgecolor=C["sep"], linewidth=0.3, height=0.6)
        _cs(ax3, "Top Destination IPs", C["purple"])

        # ── 4: Top ports ────────────────────────────────────────────
        ax4 = fig2.add_subplot(3,4,4)
        port_cnt = collections.Counter(p.dport for p in pkts
                                        if p.dport and isinstance(p.dport,int))
        if port_cnt:
            top_p = port_cnt.most_common(10)
            port_lbl = [f"{p}\n{SERVICE_DB.get(p,'?')[:8]}" for p,_ in top_p]
            port_val  = [c for _,c in top_p]
            port_col  = [C["red"] if RISK_PORTS.get(p,"")in("Critical","High")
                         else C["blue"] for p,_ in top_p]
            ax4.bar(port_lbl, port_val, color=port_col,
                    edgecolor=C["sep"], linewidth=0.3, width=0.7)
        _cs(ax4, "Top Destination Ports", C["orange"])

        # ── 5: Packet size histogram ────────────────────────────────
        ax5 = fig2.add_subplot(3,4,5)
        sizes = [p.length for p in pkts if p.length]
        if sizes:
            ax5.hist(sizes, bins=30, color=C["teal"],
                     edgecolor=C["sep"], linewidth=0.3, alpha=0.8)
            ax5.axvline(sum(sizes)/len(sizes), color=C["yellow"],
                        linestyle="--", linewidth=1, label=f"avg={sum(sizes)//len(sizes)}")
            ax5.legend(fontsize=5, facecolor=C["card"],
                       labelcolor="white", edgecolor=C["sep"])
        _cs(ax5, "Packet Size Distribution", C["teal"])

        # ── 6: Risk score histogram ─────────────────────────────────
        ax6 = fig2.add_subplot(3,4,6)
        risks = [p.risk_score for p in pkts if p.risk_score and p.risk_score > 0]
        if risks:
            n,bins,patches = ax6.hist(risks, bins=20, color=C["orange"],
                                       edgecolor=C["sep"], linewidth=0.3, alpha=0.8)
            for patch,b in zip(patches,bins):
                if b >= 70: patch.set_facecolor(C["red"])
                elif b >= 40: patch.set_facecolor(C["orange"])
            ax6.axvline(40, color=C["orange"], linestyle="--",
                        linewidth=1, label="Alert ≥40")
            ax6.axvline(70, color=C["red"], linestyle="--",
                        linewidth=1, label="CRIT ≥70")
            ax6.legend(fontsize=5, facecolor=C["card"],
                       labelcolor="white", edgecolor=C["sep"])
        _cs(ax6, "Risk Score Distribution", C["red"])

        # ── 7: Entropy histogram ────────────────────────────────────
        ax7 = fig2.add_subplot(3,4,7)
        ents = [p.payload_entropy for p in pkts
                if p.payload_entropy and p.payload_entropy > 0]
        if ents:
            n,bins,patches = ax7.hist(ents, bins=26, color=C["indigo"],
                                       edgecolor=C["sep"], linewidth=0.3, alpha=0.8)
            for patch,b in zip(patches,bins):
                if b >= 7.2: patch.set_facecolor(C["red"])
            ax7.axvline(7.2, color=C["red"], linestyle="--",
                        linewidth=1, label="Thr 7.2")
            if ents:
                m_e = sum(ents)/len(ents)
                ax7.axvline(m_e, color=C["yellow"], linestyle=":",
                            linewidth=1, label=f"μ={m_e:.2f}")
            ax7.legend(fontsize=5, facecolor=C["card"],
                       labelcolor="white", edgecolor=C["sep"])
        _cs(ax7, "Payload Entropy (Exfil Detection)", C["indigo"])

        # ── 8: HTTP Methods breakdown ────────────────────────────────
        ax8 = fig2.add_subplot(3,4,8)
        http_pkts = [p for p in pkts if p.app_proto == "HTTP" and p.http_method]
        meth_cnt  = collections.Counter(p.http_method for p in http_pkts)
        if meth_cnt:
            meth_col = {"GET":C["green"],"POST":C["orange"],"PUT":C["yellow"],
                        "DELETE":C["red"],"HEAD":C["blue"],"OPTIONS":C["teal"],
                        "PATCH":C["orange"],"TRACE":C["red"],"CONNECT":C["red"]}
            ms = list(meth_cnt.keys()); mv=[meth_cnt[m] for m in ms]
            mc=[meth_col.get(m,C["text"]) for m in ms]
            ax8.bar(ms, mv, color=mc, edgecolor=C["sep"], linewidth=0.3, width=0.6)
        _cs(ax8, "HTTP Methods", C["green"])

        # ── 9: HTTP Threat categories ────────────────────────────────
        ax9 = fig2.add_subplot(3,4,9)
        threat_cnt = collections.Counter()
        for p in pkts:
            for cat, sev, _ in analyze_http_security(p):
                threat_cnt[cat] += 1
        if threat_cnt:
            tc = threat_cnt.most_common(8)
            t_lbl = [x[0][:14] for x in tc]; t_val=[x[1] for x in tc]
            t_col = [C["red"] if v > 10 else C["orange"] if v > 5 else C["yellow"]
                     for v in t_val]
            ax9.barh(t_lbl, t_val, color=t_col,
                     edgecolor=C["sep"], linewidth=0.3, height=0.6)
        else:
            ax9.text(0.5,0.5,"No HTTP threats detected",
                     ha="center",va="center",color=C["green"],
                     fontsize=7,transform=ax9.transAxes)
        _cs(ax9, "HTTP Attack Categories", C["red"])

        # ── 10: TCP flags distribution ──────────────────────────────
        ax10 = fig2.add_subplot(3,4,10)
        flag_cnt = collections.Counter()
        for p in pkts:
            if p.tcp_flags_str:
                for f in p.tcp_flags_str.split():
                    flag_cnt[f] += 1
        if flag_cnt:
            fc = flag_cnt.most_common(8)
            f_lbl=[x[0] for x in fc]; f_val=[x[1] for x in fc]
            f_col=[C["red"] if l=="SYN" else C["orange"] if l=="RST"
                   else C["teal"] if l=="ACK" else C["blue"]
                   for l in f_lbl]
            ax10.bar(f_lbl, f_val, color=f_col,
                     edgecolor=C["sep"], linewidth=0.3, width=0.6)
        _cs(ax10, "TCP Flag Distribution", C["blue"])

        # ── 11: DNS query rate ──────────────────────────────────────
        ax11 = fig2.add_subplot(3,4,11)
        dns_pkts = sorted([p for p in pkts if p.app_proto=="DNS"], key=lambda x:x.ts)
        if len(dns_pkts) > 2:
            t0 = dns_pkts[0].ts
            bucket_sz = max(1, (dns_pkts[-1].ts - t0) / 30)
            buckets = collections.Counter(
                int((p.ts - t0) / bucket_sz) for p in dns_pkts)
            xs = sorted(buckets.keys()); ys=[buckets[x] for x in xs]
            ax11.plot(xs, ys, color=C["yellow"], linewidth=1.2)
            ax11.fill_between(xs, ys, alpha=0.2, color=C["yellow"])
            top_dns = collections.Counter(
                p.dns_query for p in dns_pkts if p.dns_query).most_common(3)
            if top_dns:
                note = "Top: " + ", ".join(f"{q[:20]}({c})" for q,c in top_dns)
                ax11.set_xlabel(note[:50], fontsize=4.5)
        _cs(ax11, "DNS Query Rate Over Time", C["yellow"])

        # ── 12: Alerts by rule ──────────────────────────────────────
        ax12 = fig2.add_subplot(3,4,12)
        alert_hits = self.app.engine.rule_hits
        if alert_hits:
            ah = sorted(alert_hits.items(), key=lambda x:x[1], reverse=True)[:8]
            a_lbl=[x[0][:14] for x in ah]; a_val=[x[1] for x in ah]
            a_col=[C["red"] if v>5 else C["orange"] for v in a_val]
            ax12.barh(a_lbl, a_val, color=a_col,
                      edgecolor=C["sep"], linewidth=0.3, height=0.6)
        else:
            ax12.text(0.5,0.5,"No alerts triggered",
                      ha="center",va="center",color=C["green"],
                      fontsize=7,transform=ax12.transAxes)
        _cs(ax12, "Alert Rule Hits", C["red"])

        fig2.suptitle("ReconShield v1.0 — Traffic Analysis Dashboard",
                       color=C["cyan"], fontsize=11, fontweight="bold", y=0.98)

        canvas2 = FigureCanvasTkAgg(fig2, master=w2)
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)
        canvas2.draw()

# ═══════════════════════════════════════════════════════════════════
#  TAB 3: ALERTS
# ═══════════════════════════════════════════════════════════════════
class AlertsTab(tk.Frame):
    def __init__(self, nb, app):
        super().__init__(nb, bg=C["bg2"])
        self.app   = app
        self._shown = set()
        self._build()
        self.after(1500, self._poll)

    def _build(self):
        hdr = SecHdr(self,"🚨  Alerts & Threat Detection  —  15 Live Detection Rules  ·  MITRE ATT&CK Mapped",
                     C["red"],
                     sub="SWRA · EWMA · BPR · SES · StateComp · FlagSig  |  Real-time threat engine")
        tk.Label(hdr, text="  ReconShield v1.0  ",
                 bg=C["panel"], fg=C["red"],
                 font=("Segoe UI Semibold",8)).pack(side="right",padx=10)

        # Severity badges
        cf = tk.Frame(self, bg=C["panel2"], pady=6); cf.pack(fill="x")
        sf = tk.Frame(cf, bg=C["panel2"]); sf.pack(side="left", padx=12)
        self._sev_vars = {}
        for sev, col in [("TOTAL",C["text"]),("CRITICAL",C["red"]),
                          ("HIGH",C["orange"]),("MEDIUM",C["yellow"]),
                          ("LOW",C["green"]),("INFO",C["blue"])]:
            f = tk.Frame(sf, bg=C["card"], padx=14, pady=6,
                         highlightbackground=col, highlightthickness=2)
            f.pack(side="left", padx=4)
            v = tk.StringVar(value="0"); self._sev_vars[sev] = v
            tk.Label(f, text=sev, bg=C["card"], fg=col,
                     font=("Segoe UI",7,"bold")).pack()
            tk.Label(f, textvariable=v, bg=C["card"], fg=col,
                     font=("Consolas",17,"bold")).pack()

        bf = tk.Frame(cf, bg=C["panel2"]); bf.pack(side="right", padx=12)
        Btn(bf,"🗑 Clear",    self._clear).pack(side="left",padx=4)
        Btn(bf,"💾 Export",   self._export).pack(side="left",padx=4)
        Btn(bf,"📊 Rule Chart",self._rule_chart).pack(side="left",padx=4)

        # Main pane
        pane = tk.PanedWindow(self, orient="horizontal",
                              bg=C["bg"], sashwidth=5)
        pane.pack(fill="both", expand=True, padx=4, pady=4)

        # Left: alert table
        lf = tk.Frame(pane, bg=C["bg2"]); pane.add(lf, width=820)
        acols = ["Time","Severity","Rule","Title","Src","Dst","MITRE","Evidence"]
        awids = [90,90,120,280,130,130,100,300]
        self._atree = make_tree(lf, acols, awids, height=28)
        for sev, col in [("CRITICAL",C["sev_c"]),("HIGH",C["sev_h"]),
                          ("MEDIUM",C["sev_m"]),("LOW",C["sev_l"]),
                          ("INFO",C["sev_i"])]:
            self._atree.tag_configure(sev, foreground=col)
        self._atree.bind("<Double-1>", self._alert_detail)

        # Right: rule chart
        rf = tk.Frame(pane, bg=C["bg2"]); pane.add(rf)
        if MPLOT:
            self._fig  = Figure(figsize=(4,7), facecolor=C["bg2"])
            self._ax   = self._fig.add_subplot(111, facecolor=C["bg"])
            self._ax.set_title("Rule Hits",color=C["yellow"],fontsize=9)
            self._canvas = FigureCanvasTkAgg(self._fig, master=rf)
            self._canvas.get_tk_widget().pack(fill="both",expand=True)
        else:
            Lbl(rf,"No matplotlib",bg=C["bg2"],fg=C["text_dim"]).pack(expand=True)

    def _poll(self):
        alerts = self.app.engine.get_alerts(500)
        for a in alerts:
            aid = id(a)
            if aid not in self._shown:
                self._shown.add(aid)
                ev = json.dumps(a.evidence,default=str)[:100] if a.evidence else ""
                self._atree.insert("","0", values=(
                    a.ts_str, a.severity, a.rule, a.title,
                    (a.src or "")[:20], (a.dst or "")[:20],
                    a.mitre or "", ev,
                ), tags=(a.severity,))
        cnt = collections.Counter(a.severity for a in alerts)
        for sev, v in self._sev_vars.items():
            v.set(str(len(alerts)) if sev=="TOTAL" else str(cnt.get(sev,0)))
        self._update_chart()
        if self.winfo_exists(): self.after(1500, self._poll)

    def _update_chart(self):
        if not MPLOT: return
        hits = dict(self.app.engine.rule_hits)
        if not hits: return
        self._ax.clear(); self._ax.set_facecolor(C["bg"])
        labels = list(hits.keys())
        values = [hits[k] for k in labels]
        COLS = [C["red"],C["orange"],C["yellow"],C["green"],C["blue"],
                C["purple"],C["teal"],C["cyan"],C["pink"],C["lime"],
                C["indigo"],C["gold"],C["orange"],C["red"],C["pink"]]
        bars = self._ax.barh(labels, values,
                              color=COLS[:len(labels)],
                              edgecolor=C["sep"], linewidth=0.3, height=0.7)
        for bar,val in zip(bars,values):
            self._ax.text(bar.get_width()+max(values)*0.01,
                         bar.get_y()+bar.get_height()/2,
                         str(val), va="center",
                         color="white", fontsize=7)
        self._ax.set_title("Rule Hits",color=C["yellow"],fontsize=9,pad=4)
        self._ax.tick_params(colors=C["text_dim"],labelsize=7)
        for sp in self._ax.spines.values(): sp.set_edgecolor(C["sep"])
        self._ax.set_xlim(0, max(values)*1.2 if values else 5)
        self._fig.tight_layout()
        self._canvas.draw_idle()

    def _alert_detail(self, event):
        sel = self._atree.selection()
        if not sel: return
        vals = self._atree.item(sel[0],"values")
        title_str = vals[3]
        alerts = self.app.engine.get_alerts(500)
        alert = next((a for a in alerts if a.title==title_str), None)
        if not alert: return
        w = tk.Toplevel(self.app); w.title(f"Alert — {title_str}")
        w.configure(bg=C["bg"]); w.geometry("820x620")
        sc = {"CRITICAL":C["sev_c"],"HIGH":C["sev_h"],
              "MEDIUM":C["sev_m"],"LOW":C["sev_l"]}.get(alert.severity,C["text"])
        tk.Frame(w, bg=sc, height=4).pack(fill="x")
        tk.Label(w, text=f"  [{alert.severity}]  {alert.title}",
                 bg=C["panel"], fg=sc,
                 font=("Segoe UI Semibold",13)).pack(fill="x", pady=6)

        nb2 = ttk.Notebook(w); nb2.pack(fill="both",expand=True,padx=8,pady=4)
        df = tk.Frame(nb2,bg=C["bg2"]); nb2.add(df, text="  Detail  ")
        for i,(k,v) in enumerate([
            ("Time",       alert.ts_str),
            ("Severity",   alert.severity),
            ("Title",      alert.title),
            ("Rule ID",    alert.rule),
            ("MITRE",      alert.mitre),
            ("Source",     alert.src),
            ("Destination",alert.dst),
            ("Description",alert.desc),
        ]):
            bg2 = C["card"] if i%2==0 else C["card2"]
            f2  = tk.Frame(df, bg=bg2); f2.pack(fill="x")
            tk.Label(f2, text=f"  {k}", bg=bg2, fg=C["text_dim"],
                     width=16, anchor="w",
                     font=("Segoe UI Semibold",10)).pack(side="left",pady=4)
            tk.Label(f2, text=str(v), bg=bg2,
                     fg=sc if k=="Severity" else C["text_hi"],
                     font=("Segoe UI",10), wraplength=550,
                     anchor="w",justify="left").pack(side="left",padx=10)

        ef = tk.Frame(nb2,bg=C["bg2"]); nb2.add(ef, text="  Evidence  ")
        et = scrolledtext.ScrolledText(ef,bg=C["bg"],fg=C["green"],
                                       font=("Consolas",10),relief="flat")
        et.pack(fill="both",expand=True,padx=4,pady=4)
        et.insert("end",json.dumps(alert.evidence,indent=2,default=str))
        et.configure(state="disabled")

        bf = tk.Frame(w,bg=C["bg"]); bf.pack(fill="x",pady=6)
        Btn(bf,"🤖  Ask AI Analyst",
            lambda: self._ask_ai(alert,w),
            bg=C["btn_g"],fg=C["green"]).pack(side="left",padx=10)
        Btn(bf,"Close",w.destroy,
            bg=C["btn_r"],fg=C["red"]).pack(side="right",padx=10)

    def _ask_ai(self, alert, parent=None):
        self.app.nb.select(self.app.tab_ai)
        ctx = self.app.ai.build_context(self.app.host_db,
              self.app.engine.get_alerts(20),
              self.app.cap_stats, self.app.engine)
        q = (f"ALERT: Rule={alert.rule}  Severity={alert.severity}\n"
             f"Title: {alert.title}\nSrc: {alert.src}  Dst: {alert.dst}\n"
             f"MITRE: {alert.mitre}\n"
             f"Evidence: {json.dumps(alert.evidence,default=str)[:600]}\n\n"
             f"Provide: 1) Root cause analysis  2) MITRE ATT&CK chain  "
             f"3) Step-by-step remediation  4) IDS rule suggestions")
        self.app.tab_ai._send(q, ctx)
        if parent: parent.destroy()

    def _clear(self):
        with self.app.engine._lock: self.app.engine.alerts.clear()
        self._atree.delete(*self._atree.get_children())
        self._shown.clear()
        for v in self._sev_vars.values(): v.set("0")

    def _export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON","*.json")])
        if not path: return
        alerts = self.app.engine.get_alerts(2000)
        data = [{"ts":a.ts_str,"severity":a.severity,"rule":a.rule,
                 "title":a.title,"src":a.src,"dst":a.dst,
                 "mitre":a.mitre,"desc":a.desc,
                 "evidence":a.evidence} for a in alerts]
        with open(path,"w") as f: json.dump(data,f,indent=2,default=str)
        messagebox.showinfo("Exported",f"{len(data)} alerts saved to {path}")

    def _rule_chart(self):
        self._update_chart()


# ═══════════════════════════════════════════════════════════════════
#  TAB 4: AI ANALYST
# ═══════════════════════════════════════════════════════════════════
class AITab(tk.Frame):
    def __init__(self, nb, app):
        super().__init__(nb, bg=C["bg2"])
        self.app = app; self._build()

    def _build(self):
        hdr = SecHdr(self,
                     "🤖  AI Security Analyst  —  Claude Sonnet 4  ·  MITRE ATT&CK  ·  SOC Intelligence",
                     C["purple"],
                     sub="Deep threat analysis · CVE correlation · Incident response planning · IOC extraction")
        tk.Label(hdr, text="  ⚡ Deependra | NFSU  ",
                 bg=C["panel"], fg=C["purple"],
                 font=("Segoe UI Semibold",9)).pack(side="right",padx=10)

        # API key row
        kf = tk.Frame(self, bg=C["panel2"], pady=5); kf.pack(fill="x")
        r1 = tk.Frame(kf, bg=C["panel2"]); r1.pack(fill="x", padx=10)
        Lbl(r1,"🔑 API Key:",bg=C["panel2"],fg=C["text_dim"],
            font=("Segoe UI Semibold",9)).pack(side="left")
        self._key = tk.StringVar(value=os.environ.get("ANTHROPIC_API_KEY",""))
        self.app.ai.key_var = self._key
        self._key_entry = tk.Entry(r1, textvariable=self._key,
                                    bg=C["card"], fg=C["cyan"],
                                    font=("Consolas",9), width=70,
                                    relief="flat", show="*",
                                    insertbackground=C["cyan"],
                                    highlightthickness=1,
                                    highlightbackground=C["border"])
        self._key_entry.pack(side="left", padx=8)
        self._show_key = tk.BooleanVar(value=False)
        tk.Checkbutton(r1, text="Show", variable=self._show_key,
                       command=lambda: self._key_entry.configure(
                           show="" if self._show_key.get() else "*"),
                       bg=C["panel2"], fg=C["text_dim"],
                       selectcolor=C["card"],
                       activebackground=C["panel2"]).pack(side="left")
        Btn(r1,"🗑 Reset Chat",self._reset,bg=C["btn_r"],fg=C["red"]).pack(side="right",padx=6)

        # Quick prompts
        qf = tk.Frame(self, bg=C["panel2"], pady=4); qf.pack(fill="x")
        Lbl(qf,"Quick Prompts:",bg=C["panel2"],fg=C["text_dim"],
            font=("Segoe UI Semibold",8)).pack(side="left",padx=10)
        QUICK = [
            ("📊 Full Report",   "Provide a complete threat analysis of the current network state including all alerts, host vulnerabilities, traffic anomalies, and risk summary."),
            ("🔍 Algorithms",    "Explain all 15 detection rules in detail including algorithms, thresholds, and MITRE ATT&CK mapping."),
            ("🎯 MITRE Map",     "Map all active alerts to MITRE ATT&CK Enterprise tactics and techniques with confidence ratings."),
            ("🛡 Remediation",   "Provide a prioritised incident response plan for all active Critical and High severity alerts with step-by-step remediation."),
            ("📈 Anomalies",     "Analyse traffic statistics and packet capture data for anomalies, suspicious patterns, and potential threats."),
            ("🔑 IOCs",          "Extract all Indicators of Compromise (IOCs) from current alerts and network data: IPs, domains, ports, hashes."),
            ("⚔ Red Team",      "From a red team perspective, what vulnerabilities in this network are most exploitable? What attack paths exist?"),
            ("📝 SOC Report",    "Generate a formal SOC incident report with executive summary, technical details, and recommendations."),
        ]
        for label, prompt in QUICK:
            Btn(qf, label,
                lambda p=prompt: self._send(p,
                    self.app.ai.build_context(self.app.host_db,
                    self.app.engine.get_alerts(20),
                    self.app.cap_stats, self.app.engine)),
                font=("Segoe UI",8), padx=8, pady=4,
            ).pack(side="left", padx=2)

        # Main pane
        pane = tk.PanedWindow(self, orient="horizontal",
                              bg=C["bg"], sashwidth=5)
        pane.pack(fill="both", expand=True, padx=4, pady=4)

        # Chat panel
        cf = tk.Frame(pane, bg=C["bg2"]); pane.add(cf, width=920)
        tk.Label(cf, text="CONVERSATION",
                 bg=C["bg2"], fg=C["purple"],
                 font=("Segoe UI Semibold",9)).pack(anchor="w",padx=6,pady=(4,0))
        self._chat = scrolledtext.ScrolledText(
            cf, bg=C["bg"], fg=C["text"],
            font=("Segoe UI",10), state="disabled",
            relief="flat", wrap="word",
            insertbackground=C["cyan"])
        self._chat.pack(fill="both",expand=True,padx=4,pady=4)
        for tag,fg2,fnt in [
            ("user",  C["cyan"],     ("Segoe UI Semibold",10)),
            ("ai",    C["text_hi"],  ("Segoe UI",10)),
            ("sys",   C["text_dim"], ("Segoe UI",9,"italic")),
            ("err",   C["red"],      ("Segoe UI",9)),
            ("hdr",   C["green"],    ("Segoe UI Semibold",10)),
        ]:
            self._chat.tag_config(tag, foreground=fg2, font=fnt)

        inf = tk.Frame(cf, bg=C["panel2"], pady=5); inf.pack(fill="x")
        self._inp = scrolledtext.ScrolledText(
            inf, bg=C["card"], fg=C["text_hi"],
            font=("Segoe UI",10), height=3,
            relief="flat", insertbackground=C["cyan"], wrap="word")
        self._inp.pack(side="left",fill="both",expand=True,padx=(8,4))
        self._inp.bind("<Return>",    self._enter)
        self._inp.bind("<Shift-Return>", lambda e: None)
        GBtn(inf,"  Send\n[Enter]",self._send_input,width=10).pack(side="right",padx=8,pady=2)

        # Context panel
        xf = tk.Frame(pane, bg=C["bg2"]); pane.add(xf, width=380)
        tk.Label(xf, text="LIVE CONTEXT",
                 bg=C["bg2"], fg=C["cyan"],
                 font=("Segoe UI Semibold",9)).pack(anchor="w",padx=6,pady=(4,0))
        self._ctx = scrolledtext.ScrolledText(
            xf, bg=C["bg"], fg=C["text_dim"],
            font=("Consolas",8), relief="flat",
            insertbackground=C["cyan"])
        self._ctx.pack(fill="both",expand=True,padx=4,pady=4)
        Btn(xf,"↺  Refresh Context",self._refresh_ctx,
            font=("Segoe UI",8),pady=4).pack(fill="x",padx=4,pady=2)

        self._write(
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║     🤖  ReconShield AI Security Analyst  —  v1.0            ║\n"
            "║     Powered by Claude Sonnet 4 (Anthropic)                  ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n\n"
            "  Set your Anthropic API key above, then ask any security question\n"
            "  or click a Quick Prompt button to get started.\n\n"
            "  The AI analyst has full visibility into:\n"
            "    • Live captured packets and protocol statistics\n"
            "    • All discovered hosts, open ports, and CVE mappings\n"
            "    • Active threat alerts with MITRE ATT&CK context\n"
            "    • Session tracker, HTTP inspector, and GeoIP data\n\n"
            "  Tip: Use  [Shift+Enter]  for a new line in the input box.\n"
            "       Press  [Enter]  alone to send your message.\n\n", "sys")
        self._refresh_ctx()
        self.after(10000, self._auto_refresh_ctx)

    def _auto_refresh_ctx(self):
        self._refresh_ctx()
        if self.winfo_exists(): self.after(15000, self._auto_refresh_ctx)

    def _write(self, text, tag="ai"):
        self._chat.configure(state="normal")
        self._chat.insert("end", text, tag)
        self._chat.see("end")
        self._chat.configure(state="disabled")

    def _refresh_ctx(self):
        ctx = self.app.ai.build_context(self.app.host_db,
              self.app.engine.get_alerts(20),
              self.app.cap_stats, self.app.engine)
        self._ctx.configure(state="normal")
        self._ctx.delete("1.0","end")
        self._ctx.insert("end", ctx)
        self._ctx.configure(state="disabled")

    def _enter(self, event):
        if not (event.state & 0x1):  # Shift not held
            self._send_input(); return "break"

    def _send_input(self):
        text = self._inp.get("1.0","end").strip()
        if not text: return
        self._inp.delete("1.0","end")
        ctx = self.app.ai.build_context(self.app.host_db,
              self.app.engine.get_alerts(20),
              self.app.cap_stats, self.app.engine)
        self._send(text, ctx)

    def _send(self, question, context=""):
        self._write(f"\n🧑 You: {question}\n\n","user")
        self._write("🤖 Analyst:  ", "hdr")
        self._write("thinking…\n","sys")
        self._refresh_ctx()

        def on_done(text, err):
            self.after(0, lambda: self._on_response(text, err))

        self.app.ai.ask(question, context, on_done=on_done)

    def _on_response(self, text, err):
        self._chat.configure(state="normal")
        # Remove "thinking…"
        idx = self._chat.search("thinking…","1.0","end")
        if idx:
            end_idx = f"{idx}+{len('thinking…')+1}c"
            self._chat.delete(idx, end_idx)
        if err:
            self._chat.insert("end", f"❌ Error: {err}\n","err")
        else:
            self._chat.insert("end", text+"\n\n","ai")
        self._chat.see("end")
        self._chat.configure(state="disabled")

    def _reset(self):
        self.app.ai.history.clear()
        self._chat.configure(state="normal")
        self._chat.delete("1.0","end")
        self._chat.configure(state="disabled")
        self._write("Chat reset.\n","sys")

# ═══════════════════════════════════════════════════════════════════
#  TAB 5: LIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════
class DashboardTab(tk.Frame):
    HIST = 90

    def __init__(self, nb, app):
        super().__init__(nb, bg=C["bg2"])
        self.app       = app
        self._pps_h    = collections.deque(maxlen=self.HIST)
        self._bps_h    = collections.deque(maxlen=self.HIST)
        self._alrt_h   = collections.deque(maxlen=self.HIST)
        self._tcp_h    = collections.deque(maxlen=self.HIST)
        self._udp_h    = collections.deque(maxlen=self.HIST)
        self._dns_h    = collections.deque(maxlen=self.HIST)
        self._last_tot = 0; self._last_bytes = 0
        self._last_ts  = time.time()
        self._build(); self._update()

    def _build(self):
        SecHdr(self,
               "📊  Live Dashboard  —  Real-time Network Traffic Analytics  ·  9 Live Charts",
               C["indigo"],
               sub="Packets/sec  ·  Throughput  ·  Protocol breakdown  ·  Entropy analysis  ·  Alert timeline  ·  Top hosts & ports  ·  Flow rates")

        # KPI strip
        kf = tk.Frame(self, bg=C["panel2"], pady=6); kf.pack(fill="x")
        kf2 = tk.Frame(kf, bg=C["panel2"]); kf2.pack(fill="x", padx=8)
        self._kv = {}
        KPI = [
            ("📦 Total Pkts","pkts",  C["cyan"]),
            ("⚡ Pkts/sec",  "pps",   C["green"]),
            ("📶 Throughput","bps",   C["blue"]),
            ("🖥 Hosts",     "hosts", C["teal"]),
            ("🚨 CRITICAL",  "crit",  C["red"]),
            ("⚠ HIGH",       "high",  C["orange"]),
            ("📋 Alerts",    "alerts",C["yellow"]),
            ("🔐 TLS",       "tls",   C["purple"]),
            ("🌐 DNS",       "dns",   C["lime"]),
            ("🔢 Avg Ent",   "ent",   C["pink"]),
            ("📤 Bytes",     "bytes_total",C["indigo"]),
            ("🛡 Rules Hit", "rules", C["gold"]),
        ]
        for label, key, col in KPI:
            f = tk.Frame(kf2, bg=C["card"], padx=10, pady=5,
                         highlightbackground=col, highlightthickness=1)
            f.pack(side="left", padx=2)
            v = tk.StringVar(value="—"); self._kv[key] = v
            tk.Label(f,text=label,bg=C["card"],fg=C["text_dim"],
                     font=("Segoe UI",7,"bold")).pack()
            tk.Label(f,textvariable=v,bg=C["card"],fg=col,
                     font=("Consolas",11,"bold")).pack()

        if not MPLOT:
            Lbl(self,"Install matplotlib for live charts — pip install matplotlib",
                bg=C["bg2"],fg=C["text_dim"],
                font=("Segoe UI",12)).pack(expand=True)
            return

        self._fig = Figure(figsize=(16,7.5), facecolor=C["bg2"])
        self._fig.subplots_adjust(
            hspace=0.52, wspace=0.34,
            left=0.05, right=0.98, top=0.93, bottom=0.08)
        axes = []
        for i in range(1, 10):
            ax = self._fig.add_subplot(3,3,i)
            ax.set_facecolor(C["bg"])
            ax.tick_params(colors=C["text_dim"],labelsize=6)
            for sp in ax.spines.values(): sp.set_edgecolor(C["sep"])
            axes.append(ax)
        (self._ax_pps, self._ax_bps, self._ax_proto,
         self._ax_alrt,self._ax_top, self._ax_risk,
         self._ax_ent, self._ax_port,self._ax_flow) = axes

        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(fill="both",expand=True,padx=6,pady=(0,4))

    def _update(self):
        if not MPLOT:
            if self.winfo_exists(): self.after(2000,self._update); return
        try:   self._refresh()
        except Exception: pass
        if self.winfo_exists(): self.after(2000,self._update)

    def _cs(self, ax, title, col):
        ax.set_title(title,color=col,fontsize=8,pad=4,fontweight="bold")
        ax.tick_params(colors=C["text_dim"],labelsize=6)
        for sp in ax.spines.values(): sp.set_edgecolor(C["sep"])

    def _refresh(self):
        s    = self.app.cap_stats
        pkts = getattr(self.app.tab_pkt,"_pkts",[])
        now  = time.time()
        dt   = max(now - self._last_ts, 0.1); self._last_ts = now

        tot  = s.get("total",0)
        pps  = (tot - self._last_tot)/dt; self._last_tot = tot
        tb   = s.get("bytes",0)
        bkps = (tb - self._last_bytes)/dt/1024; self._last_bytes = tb

        recent= pkts[-400:] if len(pkts)>400 else pkts
        ents  = [p.payload_entropy for p in recent
                 if p.payload_entropy and p.payload_entropy>0]
        avg_e = sum(ents)/len(ents) if ents else 0.0

        alerts= self.app.engine.get_alerts(500)
        crit  = sum(1 for a in alerts if a.severity=="CRITICAL")
        high  = sum(1 for a in alerts if a.severity=="HIGH")
        med   = sum(1 for a in alerts if a.severity=="MEDIUM")

        self._pps_h.append(pps); self._bps_h.append(bkps)
        self._alrt_h.append((crit,high,med))
        self._tcp_h.append(s.get("TCP",0))
        self._udp_h.append(s.get("UDP",0))
        self._dns_h.append(s.get("DNS",0))

        def _fmt(n):
            if n>1_000_000: return f"{n/1_000_000:.2f}M"
            if n>1_000:     return f"{n/1_000:.1f}K"
            return str(int(n))

        self._kv["pkts"].set(_fmt(tot))
        self._kv["pps"].set(f"{pps:.0f}")
        self._kv["bps"].set(f"{bkps:.1f}KB/s")
        self._kv["hosts"].set(str(len(self.app.host_db)))
        self._kv["crit"].set(str(crit))
        self._kv["high"].set(str(high))
        self._kv["alerts"].set(str(len(alerts)))
        self._kv["tls"].set(_fmt(s.get("TLS",0)))
        self._kv["dns"].set(_fmt(s.get("DNS",0)))
        self._kv["ent"].set(f"{avg_e:.3f}")
        self._kv["bytes_total"].set(f"{s.get('bytes',0)//1024}KB")
        self._kv["rules"].set(str(len(self.app.engine.rule_hits)))

        # 1 PPS + anomaly bands
        ax=self._ax_pps; ax.clear(); ax.set_facecolor(C["bg"])
        if len(self._pps_h)>2:
            xs=list(range(len(self._pps_h))); ys=list(self._pps_h)
            mu=sum(ys)/len(ys); sd=(sum((v-mu)**2 for v in ys)/len(ys))**0.5
            ax.fill_between(xs,ys,alpha=0.22,color=C["cyan"])
            ax.plot(xs,ys,color=C["cyan"],lw=1.4)
            if sd>0:
                ax.axhline(mu+2*sd,color=C["yellow"],ls="--",lw=0.8,alpha=0.7,label="μ+2σ")
                ax.axhline(mu+3*sd,color=C["red"],ls="--",lw=0.8,alpha=0.7,label="μ+3σ")
            ax.legend(fontsize=5,loc="upper left",
                      facecolor=C["card"],edgecolor=C["sep"],labelcolor="white")
        self._cs(ax,"Packets / Second",C["cyan"])

        # 2 Throughput
        ax=self._ax_bps; ax.clear(); ax.set_facecolor(C["bg"])
        if len(self._bps_h)>2:
            xs=list(range(len(self._bps_h))); ys=list(self._bps_h)
            ax.fill_between(xs,ys,alpha=0.22,color=C["green"])
            ax.plot(xs,ys,color=C["green"],lw=1.4)
        self._cs(ax,"Throughput  (KB/s)",C["green"])

        # 3 Protocol donut
        ax=self._ax_proto; ax.clear(); ax.set_facecolor(C["bg"])
        protos={k:v for k,v in s.items()
                if k not in("total","bytes","error","iface")
                and isinstance(v,int) and v>0}
        if protos:
            PAL=[C["blue"],C["green"],C["yellow"],C["orange"],C["purple"],
                 C["cyan"],C["teal"],C["pink"],C["lime"],C["red"],C["indigo"]]
            labels=list(protos.keys()); vals=[protos[k] for k in labels]
            total_p=sum(vals)
            disp=[f"{l}\n{v/total_p*100:.0f}%" if v/total_p>=0.03 else ""
                  for l,v in zip(labels,vals)]
            ax.pie(vals,labels=disp,colors=PAL[:len(vals)],startangle=90,
                   wedgeprops=dict(width=0.55,edgecolor=C["bg"],linewidth=0.8),
                   textprops={"color":"white","fontsize":5.5})
            ax.text(0,0,f"{_fmt(total_p)}\npkts",ha="center",va="center",
                    color=C["cyan"],fontsize=8,fontweight="bold")
        self._cs(ax,"Protocol Mix",C["yellow"])

        # 4 Alert timeline stacked
        ax=self._ax_alrt; ax.clear(); ax.set_facecolor(C["bg"])
        if len(self._alrt_h)>2:
            xs=list(range(len(self._alrt_h)))
            cs=[x[0] for x in self._alrt_h]
            hs2=[x[1] for x in self._alrt_h]
            ms=[x[2] for x in self._alrt_h]
            ax.stackplot(xs,cs,hs2,ms,
                         colors=[C["red"],C["orange"],C["yellow"]],
                         alpha=0.72,labels=["CRIT","HIGH","MED"])
            ax.legend(fontsize=5,facecolor=C["card"],
                      edgecolor=C["sep"],labelcolor="white")
        self._cs(ax,"Alert Timeline",C["red"])

        # 5 Top talkers
        ax=self._ax_top; ax.clear(); ax.set_facecolor(C["bg"])
        if pkts:
            src_cnt=collections.Counter(
                p.src_ip for p in pkts[-4000:] if p.src_ip).most_common(7)
            if src_cnt:
                ips,cnts=zip(*src_cnt)
                RCOL2={"Critical":C["red"],"High":C["orange"],
                       "Medium":C["yellow"],"Low":C["green"]}
                bcs=[RCOL2.get(self.app.host_db.get(ip,{}).get("risk",""),C["purple"])
                     for ip in ips]
                bars=ax.barh(list(ips),list(cnts),color=bcs,
                             edgecolor=C["sep"],lw=0.4,height=0.6)
                for b,c in zip(bars,cnts):
                    ax.text(b.get_width()+max(cnts)*0.01,
                            b.get_y()+b.get_height()/2,
                            str(c),va="center",color="white",fontsize=6)
                ax.set_xlim(0,max(cnts)*1.18)
                ax.invert_yaxis()
        self._cs(ax,"Top Talkers",C["purple"])

        # 6 Host risk breakdown
        ax=self._ax_risk; ax.clear(); ax.set_facecolor(C["bg"])
        RORD=["Critical","High","Medium","Low","Unknown"]
        RCOL3={"Critical":C["red"],"High":C["orange"],
               "Medium":C["yellow"],"Low":C["lime"],"Unknown":C["blue"]}
        if self.app.host_db:
            rc=collections.Counter(h.get("risk","Unknown")
                                    for h in self.app.host_db.values())
            rks=[r for r in RORD if rc.get(r,0)>0]
            vs=[rc[r] for r in rks]
            bars=ax.barh(rks,vs,color=[RCOL3[r] for r in rks],
                         edgecolor=C["sep"],lw=0.4,height=0.55)
            for b,v2 in zip(bars,vs):
                ax.text(b.get_width()+0.05,b.get_y()+b.get_height()/2,
                        str(v2),va="center",color="white",fontsize=7)
            ax.set_xlim(0,max(vs)*1.25 if vs else 5)
            ax.invert_yaxis()
        self._cs(ax,"Host Risk",C["green"])

        # 7 Entropy histogram
        ax=self._ax_ent; ax.clear(); ax.set_facecolor(C["bg"])
        all_ents=[p.payload_entropy for p in pkts[-5000:]
                  if p.payload_entropy and p.payload_entropy>0]
        if all_ents:
            n,bins,patches=ax.hist(all_ents,bins=26,color=C["teal"],
                                   edgecolor=C["sep"],alpha=0.75,lw=0.3)
            for patch,b in zip(patches,bins):
                if b>=7.2: patch.set_facecolor(C["red"])
            ax.axvline(7.2,color=C["red"],ls="--",lw=1.2,label="Thr 7.2")
            if all_ents:
                m_e=sum(all_ents)/len(all_ents)
                ax.axvline(m_e,color=C["yellow"],ls=":",lw=1,
                           label=f"μ={m_e:.2f}")
            ax.legend(fontsize=5,facecolor=C["card"],
                      edgecolor=C["sep"],labelcolor="white")
        self._cs(ax,"Payload Entropy",C["teal"])

        # 8 Top destination ports
        ax=self._ax_port; ax.clear(); ax.set_facecolor(C["bg"])
        if pkts:
            dp_cnt=collections.Counter(
                p.dport for p in pkts[-4000:]
                if p.dport and isinstance(p.dport,int)).most_common(10)
            if dp_cnt:
                dps=[f"{p}\n{SERVICE_DB.get(p,'?')[:8]}" for p,_ in dp_cnt]
                dvs=[c for _,c in dp_cnt]
                dcs=[C["red"] if RISK_PORTS.get(p,"Low") in("Critical","High")
                     else C["blue"] for p,_ in dp_cnt]
                ax.bar(dps,dvs,color=dcs,edgecolor=C["sep"],lw=0.3,width=0.7)
        self._cs(ax,"Top Dst Ports",C["blue"])

        # 9 TCP/UDP/DNS flow deltas
        ax=self._ax_flow; ax.clear(); ax.set_facecolor(C["bg"])
        if len(self._tcp_h)>2:
            def _delta(dq):
                lst=list(dq)
                return [max(lst[i]-lst[i-1],0) if i>0 else 0
                        for i in range(len(lst))]
            xs=list(range(len(self._tcp_h)))
            td=_delta(self._tcp_h); ud=_delta(self._udp_h); dd=_delta(self._dns_h)
            ax.plot(xs,td,color=C["blue"],lw=1.2,label="TCP")
            ax.plot(xs,ud,color=C["purple"],lw=1.2,label="UDP")
            ax.plot(xs,dd,color=C["yellow"],lw=1.2,label="DNS")
            ax.fill_between(xs,td,alpha=0.1,color=C["blue"])
            ax.fill_between(xs,ud,alpha=0.1,color=C["purple"])
            ax.legend(fontsize=5,facecolor=C["card"],
                      edgecolor=C["sep"],labelcolor="white")
        self._cs(ax,"Protocol Flow Rates (Δ)",C["indigo"])

        self._fig.canvas.draw_idle()


# ═══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION  —  Professional shell
# ═══════════════════════════════════════════════════════════════════
class ReconShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ ReconShield  v1.0  — Network Security & Reconnaissance   |  Deependra  ")
        try: self.state("zoomed")
        except:
            try: self.attributes("-zoomed",True)
            except: self.geometry("1440x900")
        self.minsize(1280,780)
        self.configure(bg=C["bg"])
        _style_app(self)

        # Shared state
        self.host_db   = {}
        self.pkt_queue = queue.Queue(maxsize=50000)
        self.cap_stats = {}
        self.engine    = ThreatEngine(cb=self._on_alert)
        self.ai        = AIAgent()
        self.status    = tk.StringVar(value="⚡ ReconShield v1.0 ready  —  Go to Network Recon to start scanning, or Packet Analyzer to capture traffic")
        self._alert_flash = 0

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(500, self._tick)

    def _build_ui(self):
        # ── Top banner ────────────────────────────────────────────────
        tb = tk.Frame(self, bg=C["panel"], height=48)
        tb.pack(fill="x"); tb.pack_propagate(False)
        tk.Frame(tb, bg=C["cyan"], width=4).pack(side="left",fill="y")
        tk.Label(tb, text="  ⚡ ReconShield",
                 bg=C["panel"], fg=C["cyan"],
                 font=("Segoe UI Black",16)).pack(side="left",padx=4)
        tk.Label(tb, text=" v1.0",
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI",12)).pack(side="left")
        tk.Label(tb, text="  Network Security & Reconnaissance  ",
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI",10)).pack(side="left",padx=12)

        # Right side: admin badge, status
        rb = tk.Frame(tb, bg=C["panel"]); rb.pack(side="right",padx=10)
        if ROOT:
            tk.Label(rb,text="  ✅ ADMIN  ",bg=C["btn_g"],fg=C["green"],
                     font=("Segoe UI Semibold",9)).pack(side="right",padx=4)
        else:
            tk.Label(rb,text="  ⚠ LIMITED  ",bg=C["btn_r"],fg=C["orange"],
                     font=("Segoe UI Semibold",9)).pack(side="right",padx=4)
        tk.Label(rb,text="Deependra   |  ",
                 bg=C["panel"],fg=C["text_dim"],
                 font=("Segoe UI",8)).pack(side="right")

        # ── Separator ─────────────────────────────────────────────────
        tk.Frame(self, bg=C["cyan"], height=2).pack(fill="x")

        # ── Notebook ──────────────────────────────────────────────────
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_recon = ReconTab(self.nb, self)
        self.tab_pkt   = PacketTab(self.nb, self)
        self.tab_alrt  = AlertsTab(self.nb, self)
        self.tab_ai    = AITab(self.nb, self)

        self.nb.add(self.tab_recon, text="  🛰  Network Recon  ")
        self.nb.add(self.tab_pkt,   text="  📡  Packet Analyzer  ")
        self.nb.add(self.tab_alrt,  text="  🚨  Alerts & Threats  ")
        self.nb.add(self.tab_ai,    text="  🤖  AI Security Analyst  ")

        # ── Status bar ────────────────────────────────────────────────
        sb = tk.Frame(self, bg=C["panel"], height=28)
        sb.pack(fill="x", side="bottom"); sb.pack_propagate(False)
        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x",side="top")
        self._dot = StatusDot(sb, C["green"]); self._dot.pack(side="left",padx=6,pady=4)
        tk.Label(sb, textvariable=self.status,
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI",8)).pack(side="left")
        # Right side: version badge + clock + packet counter
        tk.Label(sb, text="  ReconShield v1.0  ·  Deependra  ·  NFSU  ",
                 bg=C["panel"], fg=C["text_muted"],
                 font=("Segoe UI",7)).pack(side="right", padx=4)
        tk.Frame(sb, bg=C["border"], width=1).pack(side="right", fill="y", pady=4)
        self._clock_var = tk.StringVar()
        tk.Label(sb, textvariable=self._clock_var,
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Consolas",8)).pack(side="right",padx=10)
        tk.Frame(sb, bg=C["border"], width=1).pack(side="right", fill="y", pady=4)
        self._pkt_ctr_var = tk.StringVar(value="Pkts: 0")
        tk.Label(sb, textvariable=self._pkt_ctr_var,
                 bg=C["panel"], fg=C["cyan"],
                 font=("Consolas",8,"bold")).pack(side="right",padx=10)

    def _tick(self):
        self._clock_var.set(time.strftime("  %Y-%m-%d  %H:%M:%S  "))
        tot = self.cap_stats.get("total",0)
        self._pkt_ctr_var.set(f"Pkts: {tot:,}")
        # Alert flash
        crit = sum(1 for a in self.engine.get_alerts(50)
                   if a.severity=="CRITICAL")
        if crit > 0:
            self._alert_flash = (self._alert_flash+1)%2
            col = C["red"] if self._alert_flash else C["panel"]
            self._dot.itemconfig(1, fill=col)
        else:
            self._dot.itemconfig(1, fill=C["green"])
        if self.winfo_exists(): self.after(500, self._tick)

    def _show_welcome(self):
        """Show a professional welcome/quick-start dialog."""
        w = tk.Toplevel(self)
        w.title("Welcome to ReconShield v1.0")
        w.configure(bg=C["bg"])
        w.geometry("680x520")
        w.resizable(False, False)
        try: w.attributes("-topmost", True)
        except: pass
        # Center it
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - 680) // 2
        y = self.winfo_y() + (self.winfo_height() - 520) // 2
        w.geometry(f"680x520+{x}+{y}")

        tk.Frame(w, bg=C["cyan"], height=4).pack(fill="x")

        # Header
        hf = tk.Frame(w, bg=C["panel"], pady=14); hf.pack(fill="x")
        tk.Label(hf, text="⚡ ReconShield  v1.0",
                 bg=C["panel"], fg=C["cyan"],
                 font=("Segoe UI Black", 22)).pack()
        tk.Label(hf, text="Network Security & Reconnaissance ",
                 bg=C["panel"], fg=C["text_dim"],
                 font=("Segoe UI", 11)).pack()
        tk.Label(hf, text="Deependra  ·  NFSU School of Cyber Security & Digital Forensics",
                 bg=C["panel"], fg=C["text_muted"],
                 font=("Segoe UI", 9)).pack(pady=(2, 0))

        tk.Frame(w, bg=C["border"], height=1).pack(fill="x")

        # Quick-start guide
        body = tk.Frame(w, bg=C["bg"], pady=10); body.pack(fill="both", expand=True)

        steps = [
            (C["cyan"],   "1", "Network Recon",
             "Enter a target IP, hostname or CIDR (e.g. 192.168.0.0/24)\n"
             "then click ▶ Start Scan to discover hosts, open ports,\n"
             "service banners, CVE hints and OS fingerprints."),
            (C["green"],  "2", "Packet Analyzer",
             "Select a network interface and click ▶ Start Capture\n"
             "to capture live traffic. Filters by protocol, IP and port.\n"
             "Double-click any packet for full OSI-stack detail + HTTP Inspector."),
            (C["red"],    "3", "Alerts & Threats",
             "15 live detection rules fire automatically during capture:\n"
             "Port scans, SYN floods, DNS tunnels, ARP spoofing, C2, and more.\n"
             "Every alert is mapped to MITRE ATT&CK."),
            (C["purple"], "4", "AI Security Analyst",
             "Enter your Anthropic API key and ask the AI anything.\n"
             "Use Quick Prompt buttons for instant threat reports, IOC\n"
             "extraction, MITRE mapping and incident response plans."),
        ]
        for col, num, title, desc in steps:
            row = tk.Frame(body, bg=C["bg"]); row.pack(fill="x", padx=20, pady=5)
            tk.Frame(row, bg=col, width=4).pack(side="left", fill="y", pady=2)
            inner = tk.Frame(row, bg=C["card"], padx=10, pady=6)
            inner.pack(side="left", fill="x", expand=True, padx=(0, 4))
            tk.Label(inner, text=f"Step {num}  ·  {title}",
                     bg=C["card"], fg=col,
                     font=("Segoe UI Semibold", 10)).pack(anchor="w")
            tk.Label(inner, text=desc,
                     bg=C["card"], fg=C["text_dim"],
                     font=("Segoe UI", 9), justify="left").pack(anchor="w")

        # Admin note
        priv_col = C["green"] if ROOT else C["orange"]
        priv_txt = ("✅  Running as Admin/Root — full capture capabilities available."
                    if ROOT else
                    "⚠  Not running as Admin/Root — some features may be limited.\n"
                    "   Linux: run with  sudo python3 ReconShield_v1.py\n"
                    "   Windows: right-click → Run as Administrator")
        tk.Label(body, text=priv_txt,
                 bg=C["bg"], fg=priv_col,
                 font=("Segoe UI", 9), justify="left").pack(padx=20, anchor="w")

        tk.Frame(w, bg=C["border"], height=1).pack(fill="x")
        bf = tk.Frame(w, bg=C["panel"], pady=8); bf.pack(fill="x")
        GBtn(bf, "  🚀  Get Started  ", w.destroy,
             font=("Segoe UI Semibold", 11), padx=24, pady=6).pack()

    def _on_alert(self, alert):
        self.after(0, lambda: self.status.set(
            f"🚨 [{alert.severity}] {alert.rule}: {alert.title}"))

    def _on_close(self):
        if not messagebox.askyesno(
                "Exit ReconShield",
                "Are you sure you want to exit ReconShield v1.0?\n\n"
                "Active captures and scans will be stopped.",
                icon="warning"):
            return
        try:
            if hasattr(self.tab_pkt, "_stop_ev"):
                self.tab_pkt._stop_ev.set()
        except: pass
        self.destroy()


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not ROOT and _OS != "win32":
        print("[!] Warning: Run as root (sudo) for full promiscuous capture")
    app = ReconShieldApp()
    app.mainloop()

