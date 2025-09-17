from CarDetector import *
from BaseWorker import BaseWorker


class CarWorker(BaseWorker):
    def _worker_loop(self, frame_queue, results_queue):
        car_detector_model = CarDetector(model_path=Constants.CAR_AI_MODEL_FILE)
        while True:
            frame = frame_queue.get()
            if frame is None:
                break
            data = car_detector_model.detect_car(frame)
            results_queue.put(data)
