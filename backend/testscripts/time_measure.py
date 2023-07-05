import time
import random

def average_last_iterations(times, iterations):
    print (times[-iterations:])
    return sum(times[-iterations:]) / iterations

def main():
    i = 0
    times = []
    max_iterations = 5  # Adjust this value to set the maximum size of the 'times' list
    iterations = 0  

    while True:
        start_time = time.time()

        time.sleep(random.random())

        end_time = time.time()
        iteration_time = end_time - start_time
        times.append(iteration_time)
        i += 1
        if iterations< max_iterations:
            iterations +=1

        if len(times) > max_iterations:
            times = times[-max_iterations:]

        avg_last_x_iterations = average_last_iterations(times, iterations)
        print(f"Iteration: {i} | Time: {iteration_time:.4f}s | "
              f"Avg Last {iterations} Iterations: {avg_last_x_iterations:.4f}s")

        time.sleep(random.uniform(0, 1))

if __name__ == '__main__':
    main()
