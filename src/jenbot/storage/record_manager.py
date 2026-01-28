import uuid
import datetime

from jenbot.schemas.registry import get_schema_class
from jenerationutils.jenerationrecord import registry as recorder_registry

class RecordManager():


    def __init__(self, config = None):
        self.config = config

    
    def add_primary_key_field(self, data, SchemaClass):
        pk_name = SchemaClass.get_primary_key_name()
        data[pk_name] = uuid.uuid4().hex[:8]
        return data


    @staticmethod
    def create_timestamp_str():
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


    def build_record(self, data, SchemaClass):
        data = self.add_primary_key_field(data, SchemaClass)
        data["record_created_time"] = self.create_timestamp_str()

        return data


    def create_record(self, data, dataset_name, storage_manager):
        
        SchemaClass = get_schema_class(dataset_name)

        enriched_data = self.build_record(data, SchemaClass)

        GenerationRecordClass = recorder_registry.get_class(
            self.config["data_connections"][dataset_name]["output_data_type"]
        )
        record = GenerationRecordClass(
            schema=SchemaClass,
            generation_metadata = enriched_data
        )
        
        data_row = record.create_data_row()
        
        return data_row
        