from typing import List, Dict, Any
from ortools.sat.python import cp_model

class OptimizationAgent:
    """Agent responsible for optimizing timetable efficiency"""
    
    def __init__(self):
        self.name = "OptimizationAgent"
    
    def optimize_timetable(self, data: Dict) -> Dict:
        """Use constraint programming to generate optimal timetable"""
        model = cp_model.CpModel()
        
        divisions = data.get('divisions', [])
        subjects = data.get('subjects', [])
        rooms = data.get('rooms', [])
        faculty = data.get('faculty', [])
        timeslots = data.get('timeslots', [])
        
        # Decision variables: assignment[d][s][r][f][t] = 1 if assigned
        assignments = {}
        for d in range(len(divisions)):
            for s in range(len(subjects)):
                for r in range(len(rooms)):
                    for f in range(len(faculty)):
                        for t in range(len(timeslots)):
                            assignments[(d, s, r, f, t)] = model.NewBoolVar(
                                f'assign_d{d}_s{s}_r{r}_f{f}_t{t}'
                            )
        
        # Constraint 1: Each division-subject pair must be scheduled
        for d in range(len(divisions)):
            for s in range(len(subjects)):
                hours_needed = subjects[s].get('hours_per_week', 1)
                model.Add(
                    sum(assignments[(d, s, r, f, t)] 
                        for r in range(len(rooms))
                        for f in range(len(faculty))
                        for t in range(len(timeslots))) == hours_needed
                )
        
        # Constraint 2: No faculty overlap
        for f in range(len(faculty)):
            for t in range(len(timeslots)):
                model.Add(
                    sum(assignments[(d, s, r, f, t)]
                        for d in range(len(divisions))
                        for s in range(len(subjects))
                        for r in range(len(rooms))) <= 1
                )
        
        # Constraint 3: No room overlap
        for r in range(len(rooms)):
            for t in range(len(timeslots)):
                model.Add(
                    sum(assignments[(d, s, r, f, t)]
                        for d in range(len(divisions))
                        for s in range(len(subjects))
                        for f in range(len(faculty))) <= 1
                )
        
        # Constraint 4: No division overlap
        for d in range(len(divisions)):
            for t in range(len(timeslots)):
                model.Add(
                    sum(assignments[(d, s, r, f, t)]
                        for s in range(len(subjects))
                        for r in range(len(rooms))
                        for f in range(len(faculty))) <= 1
                )
        
        # Objective: Minimize gaps in schedule
        gaps = []
        for d in range(len(divisions)):
            for day in range(5):  # Mon-Fri
                day_slots = [t for t in range(len(timeslots)) if timeslots[t]['day'] == day]
                for i in range(len(day_slots) - 1):
                    gap_var = model.NewBoolVar(f'gap_d{d}_day{day}_slot{i}')
                    # Gap exists if slot i is used but slot i+1 is not
                    gaps.append(gap_var)
        
        model.Minimize(sum(gaps))
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0
        status = solver.Solve(model)
        
        result = {
            'status': 'optimal' if status == cp_model.OPTIMAL else 'feasible' if status == cp_model.FEASIBLE else 'infeasible',
            'assignments': []
        }
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for (d, s, r, f, t), var in assignments.items():
                if solver.Value(var) == 1:
                    result['assignments'].append({
                        'division_id': divisions[d]['id'],
                        'subject_id': subjects[s]['id'],
                        'room_id': rooms[r]['id'],
                        'faculty_id': faculty[f]['id'],
                        'timeslot_id': timeslots[t]['id']
                    })
        
        return result
    
    def calculate_utilization(self, timetable: List[Dict]) -> Dict:
        """Calculate resource utilization metrics"""
        total_slots = len(set(e['timeslot_id'] for e in timetable))
        used_slots = len(timetable)
        
        room_usage = {}
        for entry in timetable:
            room_id = entry['room_id']
            room_usage[room_id] = room_usage.get(room_id, 0) + 1
        
        return {
            'slot_utilization': used_slots / total_slots if total_slots > 0 else 0,
            'room_utilization': room_usage,
            'total_classes': used_slots
        }
