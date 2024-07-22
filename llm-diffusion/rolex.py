#!env python
import time

def timer():
    start_time = False
    last_call_time = None

    def elapsed_and_lap_time(name=''):
        nonlocal start_time, last_call_time
        if not start_time:  # initial call to start the timer
            start_time = time.time()
            print(f"Timer {name} started.")
        else:
            current_time = time.time()
            elapsed_time = current_time - start_time
            lap_time = current_time - last_call_time if last_call_time else 0
            print(f"{name} took {lap_time:.3f} seconds, total time elapsed: {elapsed_time:.3f}")
            last_call_time = current_time
    
    return elapsed_and_lap_time

rol = timer()
rol("Task 1")
rol("Task 2")
rol("Task 3")
