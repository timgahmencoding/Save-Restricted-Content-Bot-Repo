import multiprocessing
proc = multiprocessing.Process(target=your_proc_function, args=())
proc.start()
# Terminate the process
proc.terminate()  # sends a SIGTERM
