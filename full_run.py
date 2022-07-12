import mytime
import goog_calend_temp as gct
import sys
import logging
import time

logging.basicConfig(filename='run.log', level=logging.DEBUG)

if __name__ == "__main__":
    id = input("What is the mytime user ID?  ")
    pw = input("What is the mytime user Password?  ")
    success = False
    i = 0
    while not success and i < 3:
        try:
            i += 1
            schedule = mytime.run_mytime(id, pw, headless=True)
            success = True
        except Exception as e:
            time.sleep(1)
            if i >= 3:
                logging.exception("Schedule not loaded from scraper")
                raise e
            else:
                pass
    print(f"Done collecting the schedule. There are {len(schedule)} events")
    #for s in schedule:
        #print(s)
    try:
        gct.add_events(schedule)
    except Exception as e:
        logging.exception("Google Calendar API Failed to add event to calendar")
        raise e
    print("All events added (it seems)")