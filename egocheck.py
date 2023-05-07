from datetime import date
import datetime
import math
import random
import matplotlib.pyplot as progress

class User:
    def __init__(self, username, name, email, height, weight):
        self.username = username
        self.name = name
        self.email = email
        self.height = height
        self.weight = weight
        self.workouts = dict()
        self.recentWorkout = None
        
    def addWorkout(self, topsets):
        self.workouts[date.today()] = Workout(topsets)
        self.recentWorkout = Workout(topsets)
        
    def addRandom(self, days):
        i = days
        #date = datetime.date(random.randint(2022,2023), random.randint(1,12), random.randint(1,28))
        date = datetime.date(2022, (math.ceil(i/28) % 12), 1 + (i % 28))
        #lifts = [(random.randint(100,300), random.randint(1,12)) for _ in range(5)]
        lifts = [(100 + 2*i, 5) for _ in range(5)]
        self.workouts[date] = Workout(lifts)
        
    def displayWorkout(self, date):
        workout = self.workouts[date]
        if workout:
            print(f"Date: {workout.date}")
            print(f"Flat Bench Press: {workout.bench[0]} lbs, {workout.bench[1]} repetitions")
            print(f"Shoulder Press: {workout.ohp[0]} lbs, {workout.ohp[1]} repetitions")
            print(f"Back Squat: {workout.squat[0]} lbs, {workout.squat[1]} repetitions")
            print(f"Conventional Deadlift: {workout.deadlift[0]} lbs, {workout.deadlift[1]} repetitions")
            print(f"Barbell Row: {workout.row[0]} lbs, {workout.row[1]} repetitions")
        else:
            print(f"No workout found for date: {workout.date}")
            
    def calculatePercentile(self, exercise, topset):
        max = int(calculate1RM(topset))
        with open(f"{exercise}standards.txt") as file:
            for line in file:
                values = line.strip().split(',')
                standardBWeight = int(values[0])
                if standardBWeight >= self.weight:
                    for i in range(1, len(values)):
                        if int(values[i]) >= max:
                            if i == 2: return "Beginner (>5%)"
                            elif i == 3: return "Novice (>20%)"
                            elif i == 4: return "Intermediate (>50%)"
                            elif i == 5: return "Advanced (>80%)"
                            elif i == 6: return "Elite (>95%)"
                    return "World-Class"
                            
                            
class Workout:
    def __init__(self, topsets):
        self.date = date.today()
        self.bench = topsets[0]
        self.ohp = topsets[1]
        self.squat = topsets[2]
        self.deadlift = topsets[3]
        self.row = topsets[4]
        
   
def calculate1RM(topset):
    weight = int(topset[0])
    reps = int(topset[1])
    return weight / (1.0278 - (0.0278 * reps))

def graph(user):
    dates = list(user.workouts.keys())
    benchValues = [calculate1RM(workout.bench) for workout in user.workouts.values()]
    ohpValues = [calculate1RM(workout.ohp) for workout in user.workouts.values()]
    squatValues = [calculate1RM(workout.squat) for workout in user.workouts.values()]
    deadliftValues = [calculate1RM(workout.deadlift) for workout in user.workouts.values()]
    rowValues = [calculate1RM(workout.row) for workout in user.workouts.values()]
    
    progress.plot(dates, benchValues, label = 'Flat Bench Press')
    progress.plot(dates, ohpValues, label = 'Shoulder Press')
    progress.plot(dates, squatValues, label = 'Back Squat')
    progress.plot(dates, deadliftValues, label = 'Conventional Deadlift')
    progress.plot(dates, rowValues, label = 'Barbell Row')
    
    progress.xlabel('Date')
    progress.ylabel('One-rep Max (lbs)')
    progress.title('Logged Lifts')
    
    progress.legend()
    
    progress.show()
    
    

    


# demo
Jacob = User("frizellle", "Jacob Frizelle", "test@aol.com", 71, 200)

lift = [(225, 5), (135, 5),  (315, 5), (405, 5), (205, 5)]
Jacob.addWorkout(lift)
Jacob.displayWorkout(date.today())
print(Jacob.calculatePercentile("bench", lift[0]))
for i in range(1, 20):
    Jacob.addRandom(i)
graph(Jacob)



