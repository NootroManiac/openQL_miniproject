from detectors.email_detector import EmailDetector
import random
import string
import time
import os
import signal
import multiprocessing
from queue import Empty
import sys

def generate_random_string(length):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def inject_pattern(text, pattern):
    """Inject a pattern at a random position in the text"""
    position = random.randint(0, len(text))
    return text[:position] + pattern + text[position:]

def worker_process(queue, exit_flag):
    """Worker process for fuzzing in parallel"""
    detector = EmailDetector()
    iterations = 0
    threats_found = 0
    
    while not exit_flag.value:
        # Generate random strings for subject and body
        subject_length = random.randint(10, 100)
        body_length = random.randint(50, 1000)
        
        subject = generate_random_string(subject_length)
        body = generate_random_string(body_length)
        
        # Sometimes inject known phishing patterns
        if random.random() < 0.2:  # 20% chance
            patterns = [
                "urgent action required", 
                "verify your account", 
                "account suspended",
                "security alert",
                "password expired",
                "confirm your details"
            ]
            pattern = random.choice(patterns)
            if random.random() < 0.5:
                subject = inject_pattern(subject, pattern)
            else:
                body = inject_pattern(body, pattern)
        
        # Create email data
        email_data = {
            "subject": subject,
            "body": body,
            "sender": "test@example.com"
        }
        
        # Analyze email
        result = detector.analyze(email_data)
        iterations += 1
        
        if result["is_threat"]:
            threats_found += 1
            # Put result in queue to communicate back to main process
            queue.put({
                "subject": subject[:50] + "...",
                "confidence": result["confidence"],
                "patterns": result["details"]["pattern_matches"]
            })
        
        # Update status occasionally
        if iterations % 1000 == 0:
            queue.put({"iterations": iterations, "threats": threats_found})

def main():
    """Main function to run email fuzzing"""
    print("Starting email fuzzing with multiple processes...")
    
    # Create shared data structures
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    exit_flag = manager.Value('b', False)
    
    # Determine number of processes to use (1 per CPU core)
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    print(f"Using {num_processes} CPU cores for fuzzing")
    
    # Start worker processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker_process, args=(result_queue, exit_flag))
        p.start()
        processes.append(p)
    
    # Track global statistics
    total_iterations = 0
    total_threats = 0
    start_time = time.time()
    
    # Handle Ctrl+C to gracefully exit
    def signal_handler(sig, frame):
        print("\nStopping fuzzing (this may take a moment)...")
        exit_flag.value = True
        for p in processes:
            p.join(timeout=2)
        elapsed = time.time() - start_time
        print(f"\nFuzzing summary:")
        print(f"Total iterations: {total_iterations}")
        print(f"Total threats found: {total_threats}")
        print(f"Run time: {elapsed:.2f} seconds")
        print(f"Average rate: {total_iterations/elapsed:.2f} iterations/second")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Main loop to process results
    try:
        while True:
            try:
                result = result_queue.get(timeout=1)
                
                if "iterations" in result:
                    # Update from worker about iterations
                    total_iterations += result["iterations"]
                    total_threats += result["threats"]
                    elapsed = time.time() - start_time
                    print(f"\nCompleted {total_iterations} iterations in {elapsed:.2f} seconds")
                    print(f"Threats found: {total_threats}")
                    print(f"Rate: {total_iterations/elapsed:.2f} iterations/second")
                else:
                    # Threat was found
                    total_threats += 1
                    print(f"\nFound threat! #{total_threats}")
                    print(f"Subject: {result['subject']}")
                    print(f"Confidence: {result['confidence']:.2f}")
                    print(f"Patterns: {result['patterns']}")
            except Empty:
                # No results yet, continue
                pass
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 