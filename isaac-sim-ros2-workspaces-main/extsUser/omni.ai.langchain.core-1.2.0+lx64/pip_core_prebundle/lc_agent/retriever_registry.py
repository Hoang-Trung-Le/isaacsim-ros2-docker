class RetrieverRegistry:
    def __init__(self):
        """
        Instantiate the Registry with an empty list for storing class names
        and a dictionary for storing BaseRetriever objects.
        """
        self.registered_names = []
        self.retrievers = {}

    def register(self, name: str, retriever):
        """
        Register a BaseRetriever under the given name.

        Args:
            name (str): Name under which the BaseRetriever will be registered.
            retriever: The BaseRetriever object to store.
        """
        self.registered_names.append(name)
        self.retrievers[name] = retriever

    def unregister(self, name: str):
        """
        Unregister a BaseRetriever under a given name.

        Args:
            name (str): Name under which the BaseRetriever was registered.
        """
        self.registered_names.remove(name)
        self.retrievers.pop(name)

    def get_retriever(self, name: str):
        """
        Get the BaseRetriever registered under a given name. If name is not provided,
        it defaults to the first registered name.

        Args:
            name (str): Name under which the BaseRetriever was registered.
        """
        if not name and self.registered_names:
            # Default is the first one
            return self.retrievers.get(self.registered_names[0])
        return self.retrievers.get(name)

    def get_registered_names(self):
        """
        Get a list of all names under which BaseRetrievers have been registered.

        Returns:
            List of registered names.
        """
        return self.registered_names[:]


RETRIEVER_REGISTRY = RetrieverRegistry()


def get_retriever_registry():
    """
    Get the global BaseRetriever Registry.

    Returns:
        The global BaseRetriever Registry.
    """
    global RETRIEVER_REGISTRY
    return RETRIEVER_REGISTRY
