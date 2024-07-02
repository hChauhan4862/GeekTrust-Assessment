class RideSharing:
    def __init__(self):
        self.drivers = {}
        self.riders = {}
        self.rides = {}
    
    def addDriver(self, id, x, y):
        x, y = int(x), int(y)
        self.drivers[id] = {
            "X": x,
            "Y": y,
            "driving": False
        }

    def addRider(self, id, x, y):
        x, y = int(x), int(y)
        self.riders[id] = {
            "X": x,
            "Y": y,
            "MATCHES": [],
        }
    
    def Match(self, RIDER_ID):
        if RIDER_ID not in self.riders:
            return []
        
        rider = self.riders[RIDER_ID]
        matches = []
        
        for driver_id, driver in self.drivers.items():
            if not driver["driving"]:
                distance = ((driver["X"] - rider["X"]) ** 2 + (driver["Y"] - rider["Y"]) ** 2) ** 0.5
                if distance <= 5:
                    matches.append((driver_id, distance))
        
        matches.sort(key=lambda item: item[1])
        matched_drivers = [driver_id for driver_id, _ in matches[:5]]
        self.riders[RIDER_ID]["MATCHES"] = matched_drivers
        return matched_drivers
    
    def startRide(self, RIDE_ID, N, RIDER_ID):
        N = int(N)

        if RIDE_ID in self.rides:
            return "INVALID_RIDE"
        
        if RIDER_ID not in self.riders:
            return "INVALID_RIDE"
        
        rider = self.riders[RIDER_ID]
        
        if not rider["MATCHES"] or len(rider["MATCHES"]) < N:
            return "INVALID_RIDE"

        driver_id = rider["MATCHES"][N - 1]
        driver = self.drivers[driver_id]

        if driver["driving"]:
            return "INVALID_RIDE"

        self.drivers[driver_id]["driving"] = True
        self.rides[RIDE_ID] = {
            "start_X": rider["X"],
            "start_Y": rider["Y"],
            "end_X": -1,
            "end_Y": -1,
            "Minutes": 0,
            "Fare": 0,
            "Driver": driver_id,
            "Rider": RIDER_ID,
            "isFinished": False
        }

        return "RIDE_STARTED " + RIDE_ID

    def stopRide(self, RIDE_ID, X, Y, Minutes):
        X, Y, Minutes = int(X), int(Y), int(Minutes)

        if RIDE_ID not in self.rides:
            return "INVALID_RIDE"
        
        ride = self.rides[RIDE_ID]
        
        if ride["isFinished"]:
            return "INVALID_RIDE"

        ride["end_X"] = X
        ride["end_Y"] = Y
        ride["Minutes"] = Minutes

        distance = (round((X - ride["start_X"]) ** 2, 2) + round((Y - ride["start_Y"]) ** 2, 2)) ** 0.5
        
        FARE = round(50 + round(distance, 2) * 6.5 + Minutes * 2, 2)
        FARE += FARE / 5
        ride["Fare"] = "%.2f" % round(FARE, 2)

        self.drivers[ride["Driver"]]["driving"] = False
        self.drivers[ride["Driver"]]["X"] = X
        self.drivers[ride["Driver"]]["Y"] = Y
        self.riders[ride["Rider"]]["X"] = X
        self.riders[ride["Rider"]]["Y"] = Y
        ride["isFinished"] = True

        return "RIDE_STOPPED " + RIDE_ID

    def Bill(self, RIDE_ID):
        if RIDE_ID not in self.rides:
            return "INVALID_RIDE"
        
        ride = self.rides[RIDE_ID]

        if not ride["isFinished"]:
            return "RIDE_NOT_COMPLETED"

        return "BILL " + RIDE_ID + " " + ride["Driver"] + " " + str(ride["Fare"])