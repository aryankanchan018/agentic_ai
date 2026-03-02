from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)
    subjects = relationship('Subject', back_populates='department')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, unique=True)
    hours_per_week = Column(Integer)
    is_lab = Column(Boolean, default=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', back_populates='subjects')

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True)
    floor = Column(Integer)
    capacity = Column(Integer)
    bench_count = Column(Integer)
    is_lab = Column(Boolean, default=False)
    room_type = Column(String)

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_id = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

class Division(Base):
    __tablename__ = 'divisions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    student_count = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))

class TimeSlot(Base):
    __tablename__ = 'timeslots'
    id = Column(Integer, primary_key=True)
    day = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    slot_number = Column(Integer)

class TimetableEntry(Base):
    __tablename__ = 'timetable_entries'
    id = Column(Integer, primary_key=True)
    division_id = Column(Integer, ForeignKey('divisions.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    timeslot_id = Column(Integer, ForeignKey('timeslots.id'))
