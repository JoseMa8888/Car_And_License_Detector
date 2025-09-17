from LicensePlateDetector import *
from BaseWorker import BaseWorker


class LicenseWorker(BaseWorker):
    def _worker_loop(self, frame_queue, results_queue):
        license_text_detector = LicensePlateDetector()
        while True:
            license_frame = frame_queue.get()
            if license_frame is None:
                break
            license_text, licence_image = license_text_detector.get_license_plate(license_frame)
            if license_text is not None:
                results_queue.put(license_text.replace(" ", ""))