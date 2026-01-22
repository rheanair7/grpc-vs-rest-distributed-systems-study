import sys
import grpc
import lab6_pb2, lab6_pb2_grpc
import random, base64, time

def run(server_addr, command, reps):
    channel = grpc.insecure_channel(f"{server_addr}:50051")
    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    start = time.time()

    for _ in range(reps):
        if command == "add":
            resp = stub.Add(lab6_pb2.AddRequest(a=5, b=7))
        elif command == "dotProduct":
            a = [random.random() for _ in range(100)]
            b = [random.random() for _ in range(100)]
            resp = stub.DotProduct(lab6_pb2.DotRequest(a=a, b=b))
        elif command == "rawImage":
            with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
                data = f.read()
            resp = stub.RawImage(lab6_pb2.ImageRequest(image=data))
        elif command == "jsonImage":
            with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
            resp = stub.JsonImage(lab6_pb2.JsonImageRequest(image=b64_data))
        else:
            print("Invalid command")
            return

    elapsed = time.time() - start
    print(f"{command} completed {reps} repetitions in {elapsed:.3f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 grpc-client.py <SERVER_ADDR> <COMMAND> <REPS>")
        sys.exit(1)

    server_addr = sys.argv[1]
    command = sys.argv[2]
    reps = int(sys.argv[3])
    run(server_addr, command, reps)