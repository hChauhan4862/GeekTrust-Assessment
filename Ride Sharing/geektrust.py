from sys import argv
from src import RideSharing

def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()

    RIDEobj = RideSharing()

    for line in Lines:
        CMD = line.split()
        if CMD[0] == "ADD_DRIVER":
            RIDEobj.addDriver(CMD[1], CMD[2], CMD[3])
        elif CMD[0] == "ADD_RIDER":
            RIDEobj.addRider(CMD[1], CMD[2], CMD[3])
        elif CMD[0] == "MATCH":
            MATCHES = RIDEobj.Match(CMD[1])
            if len(MATCHES) == 0:
                print("NO_DRIVERS_AVAILABLE")
            else:
                print("DRIVERS_MATCHED", " ".join(MATCHES))
        elif CMD[0] == "START_RIDE":
            print(RIDEobj.startRide(CMD[1], CMD[2], CMD[3]))
        elif CMD[0] == "STOP_RIDE":
            print(RIDEobj.stopRide(CMD[1], CMD[2], CMD[3], CMD[4]))
        elif CMD[0] == "BILL":
            print(RIDEobj.Bill(CMD[1]))
        else:
            print("INVALID COMMAND")
    
    
if __name__ == "__main__":
    main()