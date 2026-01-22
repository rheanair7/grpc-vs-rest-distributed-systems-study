# REST vs gRPC Performance Benchmarking for Distributed RPC Systems

## Project Overview

This project investigates the performance trade-offs between **REST** and **gRPC**
for remote procedure calls in distributed systems. I designed and implemented
functionally equivalent REST and gRPC services, deployed them across multiple
cloud network configurations, and conducted controlled benchmarks to compare
**latency**, **serialization overhead**, and **network impact**.

The goal of this project is to understand when gRPC provides practical advantages
over REST, and how payload size and geographic distance affect RPC performance
in real-world systems.

---

## Key Questions Explored

- How does gRPC compare to REST for lightweight, latency-sensitive RPCs?
- How do JSON and Protobuf serialization formats affect performance?
- How does network topology influence RPC latency?
- When does network latency outweigh protocol-level optimizations?

---

## Experimental Workloads

To evaluate RPC performance across different compute and data profiles, the
following workloads were implemented:

### 1. Lightweight RPC (Add)
A minimal service that accepts two integers and returns their sum. This workload
isolates framework and network overhead where computation cost is negligible.

### 2. Binary Payload Processing (Raw Image)
Accepts a JPG or PNG image as a raw binary payload and returns image dimensions.
This workload evaluates binary data transfer efficiency without JSON encoding.

### 3. Compute-Heavy JSON Payload (Dot Product)
Accepts two numeric vectors of arbitrary length and computes their dot product.
Vectors are transmitted as JSON arrays to evaluate serialization and compute cost.

### 4. Base64-Encoded JSON Image
Accepts an image encoded as a base64 string inside a JSON payload and returns
image metadata. This workload compares binary payload transfer against
base64-encoded JSON transmission.

---

## API Implementations

### REST API
- Implemented using **Flask**
- JSON payloads for structured data
- Direct binary payload handling for images

### gRPC API
- Implemented using **Protocol Buffers**
- Strongly typed service definitions
- Binary serialization over HTTP/2

Both APIs expose equivalent logical functionality to ensure a fair comparison.

---

## Deployment & Benchmarking Setup

All experiments were conducted on **Google Cloud Platform** using Compute Engine
VMs with the following configuration:

- Machine type: `e2-standard-2`
- Internal IP networking only
- Python-based client and server implementations

### Network Configurations Tested

1. **Localhost**  
   Client and server running on the same machine.

2. **Same Availability Zone**  
   Client and server deployed on separate VMs within `us-west1-a`.

3. **Cross-Region Deployment**  
   Client in `us-west1-a`, server in `europe-west3-a` (Frankfurt).

Each experiment was repeated multiple times and averaged to compute per-operation
latency.

---

## Results

Average latency per operation (milliseconds):

| Method          | Local (ms) | Same-Zone (ms) | Different Region (ms) |
|-----------------|------------|---------------|----------------------|
| REST add        | 2.99       | 3.68          | 303.57               |
| gRPC add        | 0.70       | 0.98          | 148.18               |
| REST rawimg     | 5.82       | 10.07         | 1214.25              |
| gRPC rawimg     | 12.00      | 14.96         | 19267.00             |
| REST dotproduct | 3.73       | 4.36          | 303.50               |
| gRPC dotproduct | 0.81       | 1.17          | 14874.00             |
| REST jsonimg    | 45.39      | 51.00         | 1392.02              |
| gRPC jsonimg    | 25.92      | 31.90         | 21722.00             |
| PING            | 0.048      | 0.466         | 146.75               |

---

## Measurement Notes

- REST timings were recorded directly from client logs reporting average
  milliseconds per operation.
- gRPC timings were calculated by dividing total execution time by the number
  of repetitions.
- PING measurements represent baseline round-trip network latency with no
  application-layer overhead.
- Cross-region tests used internal IP addresses to minimize routing variability.

---

## Observations

### Localhost Performance
When client and server run on the same machine, network latency is negligible.
gRPC consistently outperforms REST for lightweight numeric operations due to
binary serialization and connection reuse. For image-based workloads, REST can
appear slightly faster at this scale because serialization dominates total time.

### Same-Zone Performance
With separate VMs in the same availability zone, latency increases modestly.
Both REST and gRPC remain within a few milliseconds for small payloads.
gRPC maintains an advantage for lightweight calls, while image operations
introduce additional serialization overhead.

### Cross-Region Performance
Across regions, network latency dominates overall performance. REST request
times increase roughly in proportion to baseline latency. gRPC experiences
dramatic slowdowns for large payloads, particularly for image-based workloads,
where round-trip latency and message framing significantly amplify execution time.

### Payload Sensitivity
Numeric RPCs (`add`, `dotProduct`) scale efficiently across all configurations.
Image-based workloads incur substantially higher costs due to payload size and
serialization. REST shows more predictable behavior for JSON payloads, while
gRPC performance is highly sensitive to large message handling.

### Network Baseline
PING latency establishes a lower bound of approximately 0.05 ms (local),
0.47 ms (same-zone), and 146.75 ms (cross-region). The difference between PING
and RPC timings reflects protocol overhead, serialization cost, and Python
execution overhead.

### Conclusion
gRPC provides superior performance for lightweight, high-frequency calls in
low-latency environments, making it well suited for internal microservice
communication. REST offers more stable and predictable performance for larger
payloads and high-latency, cross-region scenarios. Overall, network distance
is the dominant performance factor, with serialization and connection
management acting as secondary influences.

---

## Technologies Used

- Python
- Flask (REST API)
- gRPC & Protocol Buffers
- Google Cloud Platform (Compute Engine)
- Pillow (image processing)
- Base64 encoding
- Linux networking tools (`ping`)

---

## Future Improvements

- Add throughput (requests per second) benchmarks
- Evaluate concurrent client workloads
- Test larger payload sizes and streaming strategies
- Compare additional RPC frameworks

---

## Author

Developed as an independent systems project to study RPC performance in
distributed environments.
