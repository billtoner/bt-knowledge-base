# Network Diagnostics

Probing DNS, ports, routes, packets, and bandwidth when the network misbehaves.

- [dig](../../tool-notes/dig.md) — DNS lookups, authoritative queries, `+trace` from the root, resolver comparison
- [host](../../tool-notes/host.md) — friendlier one-shot DNS lookups; A/AAAA/MX/TXT in one line
- [whois](../../tool-notes/whois.md) — domain + IP + AS lookups; Team Cymru bulk-whois recipe
- [ss](../../tool-notes/ss.md) — modern `netstat`; what's listening or connected, by process, with kernel-level filters
- [nmap](../../tool-notes/nmap.md) — port scanning, host discovery, service/version fingerprinting, NSE scripts
- [mtr](../../tool-notes/mtr.md) — continuous traceroute + ping; finds where packets drop on a flaky path
- [traceroute](../../tool-notes/traceroute.md) — single-snapshot path discovery; TCP/UDP/ICMP modes, PMTU
- [tcpdump](../../tool-notes/tcpdump.md) — packet capture with BPF filters; remote-capture-to-local-Wireshark recipes
- [ngrep](../../tool-notes/ngrep.md) — grep on packet payloads; HTTP/DNS content matching with pcap filters
- [iperf3](../../tool-notes/iperf3.md) — active throughput measurement; TCP/UDP, parallel streams, bidirectional
- [iftop](../../tool-notes/iftop.md) — top by network flow (host pairs)
- [nethogs](../../tool-notes/nethogs.md) — top by process bandwidth
- [nc](../../tool-notes/nc.md) — TCP/UDP swiss army knife; port probe, banner grab, ad-hoc listener, throwaway HTTP responder
- [doggo](../../tool-notes/doggo.md) — modern colorized dig; JSON, DoH/DoT, multi-resolver
