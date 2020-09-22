# Video Streamer (WebCam) using TCP and Openflow

#Requirements to run the python files:

1) UNIX system / Terminal
2) Python libraries: OpenCV, Numpy, Socket, Argparse
3) Two Laptops/PC's (one as a server and other as a client)

#How to Use :

NOTE: Run the receiver first!

To receive image, type the following command on CLIENT's terminal:

        >> python receive.py --ip 0.0.0.0 --port PORT 
                 
      (Keep PORT = 5000 or any other unused port number)


To Stream, type the following command on SERVER's terminal:

        >> python stream.py --ip IP(e.g. 192.168.1.1) --port PORT --camid 0 --exposure 1 --quality 80
          
        (IP = Receiver's/CLIENT's IP address)
   
        Note: Exposure and Quality affects the image transmission efficiency.
        
