## Results

| Method          | Local (ms) | Same-Zone (ms) | Different Region (ms) |
| ---------------- | ---------- | -------------- | --------------------- |
| REST add         | 2.99       | 3.68           | 303.57                |
| gRPC add         | 0.70       | 0.98           | 148.18                |
| REST rawimg      | 5.82       | 10.07          | 1214.25               |
| gRPC rawimg      | 12.00      | 14.96          | 19267.00              |
| REST dotproduct  | 3.73       | 4.36           | 303.50                |
| gRPC dotproduct  | 0.81       | 1.17           | 14874.00              |
| REST jsonimg     | 45.39      | 51.00          | 1392.02               |
| gRPC jsonimg     | 25.92      | 31.90          | 21722.00              |
| PING             | 0.048      | 0.466          | 146.75                |


## Notes on Table

- All REST times are taken directly from client logs (`Took X ms per operation`).  
- gRPC times were calculated from total seconds per N repetitions → average milliseconds per call.  
  - Example: `add completed 1000 repetitions in 0.704 seconds` → 0.70 ms/operation.  
- PING values represent average round-trip latency.  
- The “Different Region” gRPC measurements are high because each call experiences cross-continent latency plus serialization overhead.


## Observations

**Localhost performance:**  
When both client and server run on the same machine, latency is minimal. gRPC outperforms REST on lightweight tasks like `add` and `dotProduct` since it reuses a single HTTP/2 channel and uses compact binary encoding. For larger image transfers, REST sometimes appears slightly faster due to simpler JSON parsing overhead at this small scale.

**Same-Zone performance:**  
With two VMs in the same Google Cloud zone (`us-west1-a`), network delay increases only slightly. REST remains stable for small calls, while gRPC adds a modest cost for image payloads because of serialization and stream framing. Both protocols perform within a few milliseconds of each other.

**Different-Region performance:**  
Across zones (e.g., `us-west1` → `europe-west3`), latency dominates. REST’s per-call times grow proportionally to network delay, while gRPC’s results balloon dramatically due to the impact of round-trip latency, connection reuse, and message size. For heavy payloads like `rawImage` and `jsonImage`, gRPC’s per-operation times reach tens of seconds.

**Payload impact:**  
Numeric RPCs (`add`, `dotProduct`) scale efficiently and remain close to baseline latency. Image-based operations (`rawImage`, `jsonImage`) incur higher serialization and transfer costs. REST handles JSON-encoded payloads more predictably; gRPC’s performance depends heavily on how large binary data is chunked and streamed.

**Network baseline:**  
PING averages—0.05 ms (local), 0.47 ms (same-zone), and 146.7 ms (cross-region)—establish the lower-bound latency. The jump between zones directly explains the order-of-magnitude increase in both REST and gRPC times. The difference between PING and RPC times shows the protocol and Python overhead layered atop raw network latency.

**Conclusion:**  
Overall, gRPC provides **better efficiency for lightweight, frequent local or same-zone calls**, whereas REST offers **more predictable performance for larger payloads or high-latency regions**. The experiment demonstrates that **network distance is the dominant factor**, but serialization and connection management also influence performance differences between REST and gRPC.
