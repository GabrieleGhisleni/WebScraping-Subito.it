from messages_and_email import *

if __name__ == "__main__":
    #starting_time(20,45)
    while True:
        print("im into the infinite")
        ora = dt.datetime.now().time().hour
        minuti = dt.datetime.now().time().minute
        #if dt.time(ora, minuti) == dt.time(20, 45) or dt.time(ora, minuti) == dt.time(20, 45):
        sent_working_email()
        try:
            sent_working_email()
        except Exception as e:
            print(e)
            #send_wrong_email()
        today = dt.datetime.today()
        domani = today + dt.timedelta(days=1)
        ora = dt.time(20, 45)
        until = domani.combine(domani, ora)
        diff = until - dt.datetime.today()
        secnd = diff.total_seconds()
        print("i will come back at:",dt.datetime.today() + dt.timedelta(seconds=secnd))
        time.sleep(secnd)