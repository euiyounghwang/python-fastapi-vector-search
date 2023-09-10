
import datetime

class ES_Utils(object):
    
    def __init__(self, logger, doc, es_client):
        self.logger = logger
        self.doc = doc
        self.es_client = es_client
    
    def track_performance_metrics(self, Delay_Time):
        self.logger.info("Delay Time : {}".format(Delay_Time))
        log = {
                "entity_type": "Fastapi realtime performance", 
                "elapsed_time": float(Delay_Time), 
                "@timestamp": datetime.datetime.utcnow()
                # "@timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.es_client.index(index="test_service_realtime_metrics_v1", body=log)