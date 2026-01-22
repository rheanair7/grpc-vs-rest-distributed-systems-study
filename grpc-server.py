import grpc
from concurrent import futures
import lab6_pb2, lab6_pb2_grpc
from PIL import Image
import base64, io

class Lab6Servicer(lab6_pb2_grpc.Lab6ServiceServicer):
    def Add(self, request, context):
        return lab6_pb2.AddReply(result=request.a + request.b)

    def DotProduct(self, request, context):
        result = sum([x*y for x, y in zip(request.a, request.b)])
        return lab6_pb2.DotReply(result=result)

    def RawImage(self, request, context):
        image = Image.open(io.BytesIO(request.image))
        width, height = image.size
        return lab6_pb2.ImageReply(width=width, height=height)

    def JsonImage(self, request, context):
        img_data = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(img_data))
        width, height = image.size
        return lab6_pb2.ImageReply(width=width, height=height)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6Servicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("gRPC server running on port 50051...")
server.wait_for_termination()