

class RecordManager():


    def __init__(self, config = None):
        self.config = config

    
    def save_record(self, data, dataset_name, storage_manager):
        storage_manager.data_connections[dataset_name].append_data(data)