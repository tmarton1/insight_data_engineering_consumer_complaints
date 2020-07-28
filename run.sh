python3
print("start")
from src import consumer_complaints
consumer_complaints.summarize("input/complaints.csv","output/report.csv")
