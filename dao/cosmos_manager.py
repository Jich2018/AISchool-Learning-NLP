from azure.cosmos.cosmos_client import CosmosClient
from flask import current_app as app


class Cosmos_Manager:

    def __init__(self, cosmosEndpoint = None, cosmosKey = None):
        if cosmosEndpoint is None:
            cosmosEndpoint = app.config["NLP_COSMOS_ENDPOINT"]
        
        if cosmosKey is None:
            cosmosKey = app.config["NLP_COSMOS_KEY"]

        self.client = CosmosClient(cosmosEndpoint, cosmosKey)

    def add(self, data):
        database_name = data["database"]
        container_name = data["container"]
        content = data["value"]

        database = self.client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        container.create_item(content)

    def get(self, data): #TODO: need to refactor
        database_name = data["database"]
        container_name = data["container"]
        query = data["query"]

        database = self.client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        return list(container.query_items(query=query, enable_cross_partition_query=True))


if __name__ == "__main__":
    m = Cosmos_Manager()
    print(m.get({"database": "movie-reco", "container": "reviews", "query": "SELECT * FROM c"}))

