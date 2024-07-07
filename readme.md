Heart Disease Prediction App

## Project Description
This is a PyQt6 application that allows users to load a CSV file, analyze the data, and make predictions using a machine learning model (Linear Regression). The application provides interactive input widgets and visualizations.

Dataset used:
https://www.scribbr.com/wp-content/uploads//2020/02/heart.data_.zip

This data highlights the correlation between the probability of heart disease vs biking and smoking.

Assumptions about data:
To make meaning of the heart disease numbers and visualize the data well, I had to standardize the heart disease numbers by deducting approx. 15 from each entry. I also assumed that this is the increased probability of heart disease, rather than the absolute probability, since other factors that affect heart health are unknown.

## Prerequisites
- pyqt6
- pandas
- scikit-learn
- matplotlib
- requests

## Installation
1.  Clone the repository:
    git clone [Repository URL]
2.  Navigate to the project directory:
    cd [project-directory]
3.  Create a virtual environment:
    python -m venv venv
4.  Activate the virtual environment:
    source venv/bin/activate
5.  Install the required packages:
    pip install -r requirements.txt

## Basic Usage
- run main.py
- Load CSV data
- Change feature variables using interactive input widgets 
- Visualize data and predictions