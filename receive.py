import socket

import cv2

import numpy

import argparse



def parse_args():

    parser = argparse.ArgumentParser(description='Stream cam') #The parser is like a container where we can have different arguments in it.

    parser.add_argument('--ip', dest='ip', help='stream cam to this ip.', default='0.0.0.0', type=str) #we add arguments to the container that we had in previous line

    parser.add_argument('--port', dest='port', help='stream port', default=8000, type=int) #same as above. Consider that both ip and port are optional arguments.

    args = parser.parse_args() #we parse the arguments above(imagine that we put all those arguments in the container). It gives us the arguments object

    return args

def recvdata(sock, count): #function to recieve n bites(of the size count) or return None if EOF(End of the File) is hit
#count is the max capacity of the buffer.

    buf = b''  #Byte object

    while count:

        newbuf = sock.recv(count)  #socket.recv(bufsize[, flags]), bufsize is the max amount of data to be received at once
        # For best match with hardware and network realities, the value of bufsize should be a relatively small power of 2, for example, 4096.

        if not newbuf: return None #if it didn't receive data return None

        buf += newbuf #concatening the previously available data and the newly received data

        count -= len(newbuf)   #calculate the max amount of data to be received in the next repetiotion of while loop
    return buf



def receive(conn):

    while 1: # it will continue streaming unless we press Esc key.

        length = recvdata(conn, 16)  #probably it's the header and it tells about the size of the data which is going to be received.

        if length is None:

            break

        stringData = recvdata(conn, int(length))  #now receive the actual data by calling the recvdata function once more with count=length.
        data = numpy.fromstring(stringData, dtype='uint8') #gives us a 1-D array from the text datain the string
        #numpy.fromstring(string, dtype=float, count=-1, sep='') -> dtype is the data type of the array.
        decimg = cv2.imdecode(data, 1)
        #The function reads an image from the specified buffer in the memory. If the buffer is too short or contains invalid data, the empty matrix/image is returned.
        #In the case of color images, the decoded images will have the channels stored in **B G R** order.
        #cv2.imdecode(buf, flags) -> flags > 0 means : Return a 3-channel color image.
        cv2.imshow('CAM',decimg)
        #Displays an image in a window. The window will automatically fit the size of the image. First argument is a string and is the name that we give to the window.
        #Second arguement is the image that we want to show.
        #Important: imshow() function should be followed by a waitkey function which determines how long the image must be shown.
        if cv2.waitKey(10) == 27:
            #The function waitKey waits for a key event infinitely (when \f$\texttt{delay}\leq 0\f$ ) or for delay in milliseconds, when it is positive.
            #waitkey(0) means showing the image infinately until any keypress. imshow(25) means that the image will be shown for 25 miliseconds.
            #cv2.waitKey(10) == 27 means that wait for Esc ket to be pressed.
            s.close() #Close a socket file descriptor.
            cv2.destroyAllWindows() #simply destroys all the windows we created
            break
    cv2.destroyAllWindows()



def ShowCam(ip, port):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.socket([family[, type[, proto]]])
    #Create a new socket using the given address family, socket type and protocol number. The address family should be AF_INET (the default), AF_INET6 or AF_UNIX.
    #The socket type should be SOCK_STREAM (the default), SOCK_DGRAM or perhaps one of the other SOCK_ constants. The protocol number is usually zero and may be omitted in that case.
    #In our code: creates a TCP/IP socket --- AF_INET refers to the address familly ipv4 ---- SOCK_STREAM means connection oriented TCP protocol
    s.bind(address)  #bind the socket to tuple. In this case tuple consists of IP and Port number.
    #Binding of a socket is done to address and port in order to receive data on this socket (most cases) or to use this address/port as the source of the data when sending data
    s.listen(True) #Be prepared for all incoming connections.
    #socket.listen(backlog)
    #Listen for connections made to the socket. The backlog argument specifies the maximum number of queued connections and should be at least 0;
    #the maximum value is system-dependent (usually 5), the minimum value is forced to 0.
    conn, addr = s.accept() #Store the socket object to conn and addr
    #Accept a connection. The socket must be bound to an address and listening for connections.
    #The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection,
    #and address is the address bound to the socket on the other end of the connection

    while 1:
        receive(conn)
        cv2.destroyAllWindows()
        conn, addr = s.accept()



if __name__ == '__main__':    #if the file is beaing run directly do the following. If it is imported by another file do not run it.

    args = parse_args()



    print("> Listening on: {}:{}".format(args.ip, args.port))  #Print the ip and port number we have in args.ip and args.port



    ShowCam(args.ip, args.port)