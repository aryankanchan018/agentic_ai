import sys
sys.path.append('..')
from database.database import SessionLocal, init_db
from database.models import TimeSlot
from datetime import time

def seed_timeslots():
    init_db()
    db = SessionLocal()
    
    if db.query(TimeSlot).count() > 0:
        print("Timeslots already exist")
        return
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    slots = [
        (time(9, 0), time(10, 0)),
        (time(10, 0), time(11, 0)),
        (time(11, 0), time(12, 0)),
        (time(12, 0), time(13, 0)),
        (time(13, 0), time(14, 0)),
        (time(14, 0), time(15, 0)),
        (time(15, 0), time(16, 0)),
        (time(16, 0), time(17, 0)),
    ]
    
    slot_number = 1
    for day in days:
        for start, end in slots:
            timeslot = TimeSlot(
                day=day,
                start_time=start,
                end_time=end,
                slot_number=slot_number
            )
            db.add(timeslot)
            slot_number += 1
    
    db.commit()
    print(f"Created {slot_number - 1} timeslots")
    db.close()

if __name__ == "__main__":
    seed_timeslots()
