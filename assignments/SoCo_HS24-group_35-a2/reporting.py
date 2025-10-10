import sys
from prettytable import PrettyTable
from datetime import datetime

def parse_log_file(filename):
    function_log = {} #storing function_name, num_calls, total_time
    start_times = {} #dictionary to compute time difference based on function_id

    with open(filename, 'r') as file:
        lines = file.readlines() 
        for line in lines:
            # Split the line by commas to get the individual values
            content = line.strip().split(',')
            # Defensive Coding: We should always have 4 elements for our table
            assert len(content) == 4, ValueError(f"Unexpected line format: {line}")

            function_id = content[0]
            timestamp = content[1]
            function_name = content[2]
            event = content[3]


            # Make datetime object (again) out of timestamp
            if timestamp != "timestamp":
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

            if event == "start":
                # Store the start time for the function
                start_times[function_id] = timestamp
            elif event == "stop" and function_id in start_times:
                # Calculate the time difference in milliseconds: start-end time
                start_time = start_times[function_id]
                duration_ms = (timestamp - start_time).total_seconds() * 1000 
                del start_times[function_id]

                if function_name not in function_log:
                    function_log[function_name] = {'num_calls': 0, 'total_time': 0.0}
                #dictionary inside dictionary :') sorry.
                function_log[function_name]['num_calls'] += 1
                function_log[function_name]['total_time'] += duration_ms #sums up all the time spent running this particular function

    return function_log




def pretty_table(function_log):

    table = PrettyTable()
    table.field_names = ["Function Name", "Num. of calls", "Total Time (ms)", "Average Time (ms)"]

    for function_name, data in function_log.items():
        num_calls = data['num_calls']
        total_time = data['total_time']
        average_time = 0
        if num_calls > 0:
            average_time = total_time / num_calls
        table.add_row([function_name, num_calls, total_time, average_time])
    print(table)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 reporting.py trace_file.log")
        sys.exit(1)

    filename = sys.argv[1]
    function_log = parse_log_file(filename)
    pretty_table(function_log)

if __name__ == "__main__":
    main()
