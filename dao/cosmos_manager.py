from azure.cosmos.cosmos_client import CosmosClient


class Cosmos_Manager:

    def __init__(self, context):
        self.client = CosmosClient(context["endpoint"], context["key"])

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
    m = Cosmos_Manager({"endpoint": "https://review-data.documents.azure.com:443/", "key": ""})
    print(m.get({"database": "reviews", "container": "records", "query": "SELECT * FROM c"}))

