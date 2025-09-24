from abc import ABC, abstractmethod 
import multiprocessing as mp


class BaseWorker(ABC):
    def __init__(self):
        self.frame_queue = mp.Queue(maxsize=1)
        self.results_queue = mp.Queue(maxsize=1)
        self.process = None
        self.stop_event = mp.Event()

    @abstractmethod
    def _worker_loop(self, frame_queue, results_queue):
        """ 
        params:
            frame_queue: Multiprocessor queue, frames will put in this queue
            results: Multiprocessor queue, results will put in this queue
        This method processes the frame
        """
        pass

    
    def create_process(self):
        self.process = mp.Process(
            target=self._worker_loop,
            args=(self.frame_queue, self.results_queue)
        )

    def stop(self):
        self.stop_event.set()
        if self.process is not None:
            self.process.join(timeout=2)
            if self.process.is_alive():
                # Si no salió limpio, lo matamos a la fuerza
                self.process.terminate()
                self.process.join()

    def activate_deamon(self):
        # This method activates the daemon
        self.process.daemon = True

    
    def start_process(self):
        # This method starts all the process
        self.process.start()

    
    def put_frames(self, frame):
        """ 
        params:
            frame: image of the window
        This method puts the frame in order to get it processed
        """
        self.frame_queue.put(frame)

    def frame_queue_empty(self):
        # Returns True if frame_queue has no elements
        return self.frame_queue.empty()

    
    def results_queue_empty(self):
        # Returns True if results_queue has no elements
        return self.results_queue.empty()
    

    def get_results(self):
        # This method returns a the first value from the results queue
        return self.results_queue.get()