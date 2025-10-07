# SIR-Disease-Spread-Simulation-in-Python
A Python simulation of disease spread using the SIR (Susceptible-Infected-Recovered) model. Models how infections spread through a population with configurable parameters: population size, contact range, infection rate, and recovery rate. Tracks daily statistics and identifies peak infections.

Open final_four.py and find this line at the bottom:
pythoncounts = simulate_disease(100, 2, .2, .05)
Change the four numbers:

100 = Population size
2 = Contact range (how far disease spreads)
.2 = Infection chance (20% per contact)
.05 = Recovery chance (5% per day)
