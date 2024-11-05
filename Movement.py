import Utils
from DriverHos import get_driver_HOS


MOVEMENTS = []

eastern_time_states = [
    "CT",  # Connecticut
    "DE",  # Delaware
    "FL",  # Florida
    "GA",  # Georgia
    "IN",  # Indiana
    "KY",  # Kentucky
    "ME",  # Maine
    "MD",  # Maryland
    "MA",  # Massachusetts
    "MI",  # Michigan
    "NH",  # New Hampshire
    "NJ",  # New Jersey
    "NY",  # New York
    "NC",  # North Carolina
    "OH",  # Ohio
    "PA",  # Pennsylvania
    "RI",  # Rhode Island
    "SC",  # South Carolina
    "TN",  # Tennessee
    "VT",  # Vermont
    "VA",  # Virginia
    "WV"   # West Virginia
    ]

mountain_time_states = [
    "AZ",  # Arizona
    "CO",  # Colorado
    "ID",  # Idaho
    "MT",  # Montana
    "NM",  # New Mexico
    "UT",  # Utah
    "WY"   # Wyoming
    ]

pacific_time_states = [
    "CA",  # California
    "NV",  # Nevada
    "OR",  # Oregon
    "WA"   # Washington
    ]

class Movement:
    def __init__(self, orderNum, tractor, apptEarly, apptLate, destState, miles_out, mph, time_in_current,
                driving_status, drive_time, shiftRemainingMs, cycle_today, cycle_tomorrow) -> None:
        self.orderNum = orderNum
        self.tractor = tractor
        self.state = destState
        self.time_in_current = time_in_current / 60000
        if driving_status == 2:
            self.driving_status = "DRIVING"
        else:
            self.driving_status = "OFFDUTY"
        self.drive_time = drive_time / 60000
        self.shiftRemainingMs = shiftRemainingMs / 60000
        self.cycle_today = cycle_today / 60000
        self.cycle_tomorrow = cycle_tomorrow / 60000
        self.message = ''

        if miles_out == '':
            self.message = "Driver is not tracking"
            return
        self.miles_out = int(miles_out)
        

        if apptLate != "":
            self.delivery = apptLate
        else:
            self.delivery = apptEarly

        match self.state:
            case self.state if self.state in eastern_time_states:
                self.delivery = Utils.time_sub(self.delivery, 60)
            case self.state if self.state in mountain_time_states:
                self.delivery = Utils.time_add(self.delivery, 60)
            case self.state if self.state in pacific_time_states:
                self.delivery = Utils.time_add(self.delivery, 120)

        self.time_to_deliver = Utils.time_diff(Utils.get_now(), self.delivery)

        #Calculate how long it will take to drive
        self.transit = round((int(self.miles_out) / int(mph))*60)

        self.track()
    
        MOVEMENTS.append(self)

    def print_stats(self):
        print("orderNum", self.orderNum, "\n",
            "tractor", self.tractor, "\n",
            "state", self.state, "\n",
            "transit", self.transit, "\n",
            "time_to_deliver", self.time_to_deliver, "\n",
            "delivery", self.delivery, "\n",
            "message", self.message, "\n",
            "time_in_current", self.time_in_current, "\n",
            "drive_time", self.drive_time, "\n",
            "shiftRemainingMs", self.shiftRemainingMs, "\n",
            "cycle_today", self.cycle_today, "\n",
            "cycle_tomorrow", self.cycle_tomorrow)

    def track(self):
        if not self.not_enough_drive():
            self.not_enough_cycle_today()
            self.not_enough_cycle_tomorrow()
        self.delivery_not_possible()
        self.is_passed_delivery()
        if self.message == '': self.follow_up_message()

    def get_eta(self):
        return Utils.time_add(Utils.get_now(), self.transit)

    def is_passed_delivery(self):
        if self.time_to_deliver < 0:
            self.message = "LATE The delivery appt has passed"

    def delivery_not_possible(self):
        if self.transit > self.time_to_deliver:
            self.message = "LATE The transit time is too long."
            if self.driving_status == "DRIVING" and self.drive_time > self.transit: 
                self.message = (self.message + " Driver is rolling " + str(self.miles_out) + 
                                " miles out with an ETA of " + self.get_eta()
                                 + " for a " + self.delivery + " APPT.")
            else: 
                match self.driving_status:
                    case "DRIVING":
                        self.message = (self.message + " Driver is rolling")
                        if self.drive_time > self.transit:
                            self.message = (self.message + " " + str(self.miles_out) + 
                                " miles out with an ETA of " + self.get_eta()
                                 + " for a " + self.delivery + " APPT.")
                        else:
                            self.message = (self.message + ", but does not have enough HOS.")

                    case _:
                        self.message = (self.message + " Driver is not rolling")
                        if self.drive_time > self.transit:
                             (self.message + ", but has a theoretical ETA of " + self.get_eta())
                        else:
                            self.message = (self.message + " and does not have enough HOS for transit.")

    def not_enough_drive(self):
        if self.drive_time < self.transit:
            return(self.break_too_long())
        else:
            self.follow_up_message()
    
    def not_enough_cycle_today(self):
        if (Utils.get_date(self.delivery) == Utils.get_date(Utils.get_now())) and (self.cycle_today < self.transit):
            self.message = "LATE Driver does not have enough time on his 70."
    
    def not_enough_cycle_tomorrow(self):
        if (Utils.get_date(self.delivery) > Utils.get_date(Utils.get_now())) and (self.cycle_tomorrow < self.transit):
            self.message = "LATE Driver will not have enough time on his 70 tomorrow."

    def break_too_long(self):
        TEN_HOURS = 10 * 60  # minutes
        if self.time_to_deliver < (TEN_HOURS + self.transit):
            if self.driving_status != "DRIVING":
                if (self.transit + (TEN_HOURS - self.time_in_current) > self.time_to_deliver):
                    self.message = "LATE Driver's break will not end in time to roll for OTD."
                    return True
                else:
                    self.follow_up_message()
                    return False
            else: 
                self.message = "LATE Driver does not have enough drive time and cannot break"
                return True
        else: 
                self.follow_up_message()
                return False

    def follow_up_message(self):
        if self.driving_status == "DRIVING":
            self.message = ("ONTIME Driver is rolling " + str(self.miles_out) + 
                            " miles out. ETA is " + self.get_eta() + 
                            " for a " + self.delivery + " APPT.")
        else:
            self.message = ("FOLLOWUP Driver needs to roll by " + str(Utils.time_sub(self.delivery, self.transit))) 
    
    def save_all_movements(window):
        global MOVEMENTS

        tracking_txt = []
        late_movements = []
        ontime_movements = []
        if window.parent.parent.settings_tab.settings.get_setting('sort_tracking_val') == 'on':
            for movement in MOVEMENTS:
                if movement.message.split(' ')[0] == 'LATE':
                    late_movements.append(str(movement.orderNum) + ' ' + str(movement.tractor) + ' ' + str(movement.message))
                else:
                    ontime_movements.append(str(movement.orderNum) + ' ' + str(movement.tractor) + ' ' + str(movement.message))
            tracking_txt = late_movements + [" ", " ", " "] + ontime_movements
        else:
            for movement in MOVEMENTS:
                tracking_txt.append(str(movement.orderNum) + ' ' + str(movement.tractor) + ' ' + str(movement.message))

        Utils.save_array_to_txt(tracking_txt, 'Tracking.txt')

    def copy_all_from_McLeod(window, username, password, mph):
        global MOVEMENTS
        
        window.label.configure(text="Copying orders from Order Planning screen.")

        try:
            data = Utils.export_to_excel()
            orders = [[column.strip() for column in line.split('|')] for line in data.split('\n') if '----' not in line]

            if len(orders) < 2:
                raise Exception("Did not meet length requirements.")
        except:
            window.label.configure(text="Error while copying orders. Please try again.")
            window.label.pack()
            return 0

        window.label.configure(text="Logging into Samsara...")

        drivers = get_driver_HOS(username=username, password=password)
        if len(drivers) < 1:
            print("Login failed")
            window.label.configure(text="Login Failed. Check credentials and try again.")
            window.label.pack()
            return 0

        window.label.configure(text="Tracking in progress...")
        try:

            key = {}
            for column in orders[0]:
                key[column] = orders[0].index(column)

            i = 1
            print("Tracking", len(orders), "orders")
            while i < len(orders) - 1:
                if orders[i][key['Actual arrival']] != '' or orders[i][key['Order number']] == '':
                    window.progressbar.set(i/(len(orders)-2))
                    i+=1
                    continue
                if Utils.time_diff(orders[i][key['Next stop arrive early']], window.parent.end_date) < 0: 
                    window.progressbar.set(i/(len(orders)-2))
                    i+=1
                    continue
                try:
                    driverHOS = drivers[orders[i][key['D1 Driver code']]]
                except:
                    i+=1
                    continue
                Movement(
                    orderNum=orders[i][key['Order number']], 
                    tractor=orders[i][key['Tractor']], 
                    apptEarly=orders[i][key['Next stop arrive early']],
                    apptLate=orders[i][key['Next stop arrive late']], 
                    destState=orders[i][key['Dest state']],  
                    miles_out=orders[i][key['Dist to next stop']],
                    mph=mph,
                    time_in_current=driverHOS['time_in_current'],
                    driving_status=driverHOS['driving_status'],
                    drive_time=driverHOS['drive_time'],
                    shiftRemainingMs=driverHOS['shiftRemainingMs'],
                    cycle_today=driverHOS['cycle_today'],
                    cycle_tomorrow=driverHOS['cycle_tomorrow'])

                window.progressbar.set(i/(len(orders)-1))
                i+=1  
        except Exception:
            MOVEMENTS = []
            window.label.configure(text="There was an error tracking. Please try again")
            return 0
        
        window.progressbar.set(1)    

        Movement.save_all_movements(window=window)

        MOVEMENTS = []

        return 1