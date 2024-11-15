import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to find the waiting time for all processes
def findWaitingTime(processes, n, wt, gantt_chart):
    rt = [0] * n
    for i in range(n):
        rt[i] = processes[i][1]

    complete = 0
    t = 0
    minm = 999999999
    short = 0
    check = False

    # Process until all processes get completed
    while complete != n:
        # Find process with minimum remaining time among the processes that arrive till the current time
        for j in range(n):
            if processes[j][2] <= t and rt[j] < minm and rt[j] > 0:
                minm = rt[j]
                short = j
                check = True

        if not check:
            t += 1
            continue

        # Process execution
        rt[short] -= 1
        gantt_chart.append((t, short + 1))  # Add the process execution to Gantt chart

        # Update minimum
        minm = rt[short]
        if minm == 0:
            minm = 999999999

        # If a process gets completely executed
        if rt[short] == 0:
            complete += 1
            check = False
            fint = t + 1
            wt[short] = fint - processes[short][1] - processes[short][2]
            if wt[short] < 0:
                wt[short] = 0

        # Increment time
        t += 1

# Function to calculate turn around time 
def findTurnAroundTime(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

# Function to calculate average waiting and turn-around times.
def findavgTime(processes, n):
    wt = [0] * n
    tat = [0] * n
    gantt_chart = []

    # Find waiting time for all processes
    findWaitingTime(processes, n, wt, gantt_chart)

    # Find turn around time for all processes
    findTurnAroundTime(processes, n, wt, tat)

 # Process Details Table
    st.write("### Process Details")
    # Create a list of headers for the table
    headers = ["Process ID", "Burst Time", "Arrival Time", "Waiting Time", "Turn-Around Time"]

    # Add the header to the table data
    table_data = [headers]
    
    total_wt = 0
    total_tat = 0

    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        # Append process details as strings in the correct format
        table_data.append([
            f"P{processes[i][0]}",   # Process ID
            f"{processes[i][1]} ms", # Burst Time
            f"{processes[i][2]} ms", # Arrival Time
            f"{wt[i]} ms",           # Waiting Time
            f"{tat[i]} ms"           # Turn-Around Time
        ])

    # Display the table using st.table
    st.table(table_data)
    # Display average times
    avg_wt = total_wt / n
    avg_tat = total_tat / n
    st.write(f"**Average Waiting Time:** {avg_wt:.5f}")
    st.write(f"**Average Turn Around Time:** {avg_tat:.5f}")

    # Visualize Gantt Chart
    st.write("### Gantt Chart")
    visualize_gantt_chart(gantt_chart)

# Function to visualize Gantt chart using Matplotlib
def visualize_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(8, 2))  # Adjust figure size for smaller height

    # Set colors for each process
    colors = plt.cm.tab20.colors
    start_time = 0
    bar_height = 0.3  # Set a smaller bar height for compact Gantt chart

    for t, process in gantt_chart:
        ax.barh(1, 1, height=bar_height, left=start_time, color=colors[process % len(colors)], edgecolor='black')
        ax.text(start_time + 0.5, 1, f"P{process}", va='center', ha='center', color='black', fontsize=8)  # Adjust font size
        start_time += 1

    ax.set_xlabel('Time')
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_title('Gantt Chart for SRTF Scheduling', fontsize=10)

    # Adjusting the plot for better readability
    ax.set_ylim(0.8, 1.2)  # Set the y-limits to control the height

    # Display chart
    st.pyplot(fig)


# Streamlit app
st.set_page_config(page_title="SRTF Scheduling Algorithm", layout="wide")
st.write("""
## Shortest Remaining Time First (SRTF)""")
# Introduction Section
st.write("""
## Introduction
Shortest Remaining Time First (SRTF) is a preemptive CPU scheduling algorithm. It is a variation of the Shortest Job Next (SJN) scheduling algorithm but differs by allowing a process to be interrupted if a newly arriving process has a shorter burst time than the currently running process. SRTF focuses on minimizing the overall time processes spend waiting in the queue, which reduces the average waiting time in the system.
""")

# Divider for Steps with orange color
st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

# Step-by-Step guide for SRTF
st.write("""
## Step 1: Understand SRTF Scheduling
SRTF is a preemptive version of the Shortest Job First (SJF) algorithm.
It selects the process with the shortest remaining burst time at every time unit.
If a new process arrives with a burst time shorter than the remaining time of the current process, the CPU is preempted and assigned to the new process.
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

st.write("""
## Step 2: Gather the Input
Collect the necessary details for each process:

- Process ID (Unique identifier for each process)
- Arrival Time (Time at which the process arrives in the system)
- Burst Time (Total time required by the process for execution)
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

st.write("""
## Step 3: Initialize Variables
Create the following variables:

- Remaining Time for each process (initially set to its burst time)
- Current Time (start at 0)
- Completed Processes count (initially set to 0)
- Total Waiting Time and Total Turnaround Time (to calculate averages later)
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

st.write("""
## Step 4: Process Execution Loop
While there are incomplete processes:

1. **Select the Process**: From the list of available processes (those that have arrived by the current time), choose the one with the shortest remaining time.
    - If multiple processes have the same remaining time, choose the one that arrived first.
2. **Execute the Process**:
    - Execute the selected process for 1 time unit.
    - Decrease its remaining time by 1.
    - If the remaining time of the process becomes 0, mark it as completed and:
        - Calculate Completion Time: Record the time at which the process finished.
        - Calculate Turnaround Time: Completion Time - Arrival Time
        - Calculate Waiting Time: Turnaround Time - Burst Time
        - Increment the Completed Processes count.
3. **Increment the Current Time**: Increase the current time by 1 unit.
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

st.write("""
## Step 5: Repeat Until All Processes Are Completed
Continue the loop in Step 4 until all processes are completed.
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

st.write("""
## Step 6: Calculate Averages
- **Average Waiting Time** = Total Waiting Time / Number of Processes
- **Average Turnaround Time** = Total Turnaround Time / Number of Processes
""")

st.markdown('<hr style="border-top: 3px solid orange;" />', unsafe_allow_html=True)

# Input process details
n = st.slider("Number of Processes", 1, 10, 4)

proc = []
for i in range(n):
    burst_time = st.number_input(f"Enter burst time for Process {i+1}", min_value=1, max_value=50, value=6)
    arrival_time = st.number_input(f"Enter arrival time for Process {i+1}", min_value=0, max_value=50, value=0)
    proc.append([i+1, burst_time, arrival_time])

# Display entered processes in a table before calculating
if st.checkbox("Show Process List"):
    st.write("### Entered Processes")
    st.write("Process ID    Burst Time    Arrival Time")
    process_table = [[p[0], p[1], p[2]] for p in proc]
    st.table(process_table)

# Calculate and display process details and Gantt chart
if st.button("Calculate Scheduling"):
    findavgTime(proc, n)

# Footer Section
st.write("""
## Further Reading
- [Operating Systems: Three Easy Pieces](https://www.ostep.org/)
- [Scheduling Algorithms in Operating Systems](https://www.geeksforgeeks.org/cpu-scheduling/)
""")
