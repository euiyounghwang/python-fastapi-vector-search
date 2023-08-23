


class SearchOmniHandler(object):
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, es_client, logger, config):
        self.es_client = es_client
        self.logger = logger
        self.config = config
        self.OMNI_INDEX_ALIAS = self.config["es"]["index"]["alias"]
        self.search_after = None
        
        
    async def search(self):
        self.logger.info("search..")