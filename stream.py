import socket
import cv2
import numpy
import argparse



def parse_args():
    """This function is Argument Parser """

    parser = argparse.ArgumentParser(description='Stream cam')
    parser.add_argument('--ip', dest='ip', help='stream cam to this ip.', default='0.0.0.0', type=str)
    parser.add_argument('--port', dest='port', help='stream port', default=8000, type=int)
    parser.add_argument('--camid', dest='camid', help='Camera ID', default=0, type=int)
    parser.add_argument('--exposure', dest='exposure', help='Camera exposure', default=1, type=int)
    parser.add_argument('--quality', dest='quality', help='Encode quality', default=80, type=int)
    args = parser.parse_args()
    return args

def stream(ip, port, camid=0, exposure=1, quality=80):
    """This Function does all the required process for video streaming """

    # Stores IP address and port number
    address = (ip, port)

    # Creates a TCP socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(address)

    # Capturing the video through Webcam,
    capture = cv2.VideoCapture(camid)
    # Defining the frame rate and exposure
    capture.set(15, exposure)
    # capture frame by frame
    ret, frame = capture.read()
    # encoding parameter, For JPEG, it can be a quality from 0 to 100 (the higher is the better).
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), quality]

    while ret:
        # Compressing the data in JPEG with the defined frame rate and encoding parameter
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # Converting the resulting data into array
        data = numpy.array(imgencode)
        # Converting this to a string, which will then be sent over the TCP
        stringData = data.tostring()
        # Using string's encode() method, you can convert unicoded strings into any encodings supported by Python.
        # The string ljust() method returns a left-justified string of a given minimum width (16 in this case).
        # This string is then converted to bytes.
        sock.send(bytes(str(len(stringData)).encode().ljust(16)))
        # Send data to the socket.
        sock.send(stringData)
        ret, frame = capture.read()
        if cv2.waitKey(10) == 27:   # wait for ESC key to exit
            break
    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    args = parse_args()
    print("> Cam ID {}".format(args.camid))
    stream(args.ip, args.port, args.camid, args.exposure, args.quality)