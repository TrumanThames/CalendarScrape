import mytime
import goog_calend_temp as gct
import sys

if __name__ == "__main__":
    id = input("What is the mytime user ID?  ")
    pw = input("What is the mytime user Password?  ")
    schedule = mytime.run_mytime(id, pw, headless=False)
    print("Done collecting the schedule")
    #for s in schedule:
        #print(s)
    gct.add_events(schedule)
    print("All events added (it seems)")