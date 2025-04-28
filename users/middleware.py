
import time
import logging



logger =logging.getLogger(__name__)


class LoggingApiHitTime:
    def __init__(self,get_response):
        self.get_response = get_response         

    def __call__(self, request):
        start_time =time.time()

        response =self.get_response(request)

        duration = time.time() - start_time
        print(duration,"hii")
        logger.info(f"[{request.method}] {request.get_full_path()} took {duration:.4f} seconds")

        # logger.info(f"[{request.method}] took {duration} seconds")

        return response
        
    