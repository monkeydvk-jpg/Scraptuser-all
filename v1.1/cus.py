import threading
import tkinter as tk

def start_process():
    global stop_event, process_thread
    stop_event = threading.Event()
    process_thread = threading.Thread(target=run_process, args=(stop_event,))
    process_thread.start()
    status_label.config(text="Process running...")

def stop_process():
    if 'stop_event' in globals():
        stop_event.set()
        status_label.config(text="Process stopped")

def run_process(stop_event):
    # Your long-running process
    for i in range(100):
        if stop_event.is_set():
            break
        # Do work here
        print(f"Processing step {i}")
        # Check periodically if we should stop
        time.sleep(0.5)
    
    # Update UI when done
    if not stop_event.is_set():
        root.after(0, lambda: status_label.config(text="Process completed"))

root = tk.Tk()
start_button = tk.Button(root, text="Start", command=start_process)
stop_button = tk.Button(root, text="Stop", command=stop_process)
status_label = tk.Label(root, text="Ready")

start_button.pack()
stop_button.pack()
status_label.pack()

root.mainloop()
