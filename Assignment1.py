from datetime import datetime
import pandas as pd
import openpyxl
from numpy.ma.extras import average

file_path = 'Data For Matches.xlsx'
df = pd.read_excel(file_path)
df['Date'] = pd.to_datetime(df['Date'])
draw_matches = df[df['Win team'] == '-']

averageHomeGoal = df.groupby('Home')['Home Goals'].mean()
averageAwayGoal = df.groupby('Away')['Away Goals'].mean()

points = {}

for i, row in df.iterrows():
    homeTeam = row['Home']
    awayTeam = row['Away']
    winTeam = row['Win team']

    if homeTeam not in points:
        points[homeTeam] = 0
    if awayTeam not in points:
        points[awayTeam] = 0;

    if winTeam == homeTeam:
        points[homeTeam] += 3
    elif winTeam == awayTeam:
        points[awayTeam] += 3
    elif winTeam == '-':
        points[homeTeam] += 1
        points[awayTeam] += 1

# for team, point in points.items():
#     print(f"{team}: {point}")

import numpy as np
import math


def poissonProbability(k, lamb):
    return (math.pow(lamb, k) * math.exp(-lamb)) / math.factorial(k)


def predictMatchOutcome(homeTeam, awayTeam):
    lamdaHome = averageHomeGoal.get(homeTeam)
    lamdaAway = averageAwayGoal.get(awayTeam)

    homeGoals = np.random.poisson(lamdaHome)
    awayGoals = np.random.poisson(lamdaAway)

    if homeGoals > awayGoals:
        result = f"{homeTeam} wins"
    elif homeGoals < awayGoals:
        result = f"{awayTeam} wins"
    else:
        result = f"It's a draw"

    return homeGoals, awayGoals, result


# home_team = 'Arsenal'
# away_team = 'Chelsea'
# predicted_home_goals, predicted_away_goals, result = predictMatchOutcome(home_team, away_team)
# print(f"Predicted Score: {home_team} {predicted_home_goals} - {predicted_away_goals} {away_team}")
# print("Match Result:", result)

def MonteCarloSimulation(homeTeam, awayTeam, numOfSimulations):
    homeWins = 0;
    awayWins = 0;
    draws = 0;

    for _ in range(numOfSimulations):
        homeGoals, awayGoals, result = predictMatchOutcome(homeTeam, awayTeam)
        if result == f"{homeTeam} wins":
            homeWins += 1
        elif result == f"{awayTeam} wins":
            awayWins += 1
        else:
            draws += 1

    print(f"Out of {numOfSimulations} simulations: ")
    print(f"{homeTeam} wins: {homeWins / numOfSimulations :.2%}")
    print(f"{awayTeam} wins: {awayWins / numOfSimulations :.2%}")
    print(f"Draws: {draws / numOfSimulations :.2%}")


# MonteCarloSimulation('Arsenal', 'Chelsea', 10000)

import matplotlib.pyplot as plt


def simulateGoals(lamb):
    simulated_goals = np.random.poisson(lamb, 10000)
    plt.hist(simulated_goals, bins=10, color='skyblue', edgecolor='black')
    plt.title(f"Distribution of Simulated Goals (λ = {lamb})")
    plt.xlabel("Number of Goals")
    plt.ylabel("Frequency")
    plt.show()


# simulateGoals(averageHomeGoal['Arsenal'])

decay_rate = 0.05


def calculateWeightedLambda(team, teamType, currentDate, decayRate):
    if teamType == 'home':
        teamMatches = df[df['Home'] == team]
        goals = teamMatches['Home Goals']
    elif teamType == 'away':
        teamMatches = df[df['Away'] == team]
        goals = teamMatches['Away Goals']

    if teamMatches.empty:
        raise ValueError(f"No match data available for {team} as {teamType}")

    timeDifferences = (currentDate - teamMatches['Date']).dt.days
    weights = np.exp(-decayRate * timeDifferences / 7)
    weight_sum = np.sum(weights)
    if weight_sum == 0:
        raise ValueError(f"Weight sum for {team} as {teamType} is zero. Check the decay rate or time differences.")
    weightedLambda = np.average(goals, weights=weights)
    return weightedLambda


def predictMatchOutcome(homeTeam, awayTeam):
    currentDate = datetime.now()
    lambdaHome = calculateWeightedLambda(homeTeam, 'home', currentDate, decay_rate)
    lambdaAway = calculateWeightedLambda(awayTeam, 'away', currentDate, decay_rate)
    homeGoals = np.random.poisson(lambdaHome)
    awayGoals = np.random.poisson(lambdaAway)

    if homeGoals > awayGoals:
        return homeTeam, 3
    elif homeGoals < awayGoals:
        return awayTeam, 3
    else:
        return 'Draw', 1


def monteCarloSimulationPoints(teams, remianingMatches, numOfSimulations):
    finalPoints = {team: points[team] for team in teams}
    simulationPoints = finalPoints.copy()

    for _ in range(numOfSimulations):
        for homeTeam, awayTeam in remianingMatches:
            winner, pointsScored = predictMatchOutcome(homeTeam, awayTeam)
            if winner == homeTeam:
                simulationPoints[homeTeam] += 3
            elif winner == awayTeam:
                simulationPoints[awayTeam] += 3
            else:
                simulationPoints[homeTeam] += 1
                simulationPoints[awayTeam] += 1

    averagePoints = {team: finalPoints[team]+ (simulationPoints[team] -finalPoints[team]) / numOfSimulations for team in teams}
    return averagePoints


remaining_matches = [
    ('Arsenal', 'Chelsea'),
    ('Man City', 'Chelsea'),
    ('Chelsea', 'Liverpool')
]
teams = list(points.keys())
average_final_points = monteCarloSimulationPoints(teams, remaining_matches, numOfSimulations=1000)

# Display predicted final points
print("Predicted Final Points for Each Team:")
for team, pts in average_final_points.items():
    print(f"{team}: {pts:.2f} points")