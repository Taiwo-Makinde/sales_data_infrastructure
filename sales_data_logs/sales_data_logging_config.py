"""
This is the centralised logging for the sales_data_infrastructure project. 

Each entry gets its own logger & its own log file. 
"""

# Importing inbuilt modules in the Standard Python Library 
import json 
import logging 
import logging.config 
from datetime import datetime, timezone 
from pathlib import Path 

# We set the log level here once and for all. We would change the LOG_LEVEL  by just adjusting it here. 
LOG_LEVEL = "DEBUG" 

# We want to determine the exact location where logs that relate to this configuration would be placed.
# Using resolve(), we anchor the logs folder to a predictable file location not the current working directory so that logs always land in the same place, 
# regardless of where the script is run from
SALES_DATA_LOG_DIR = Path(__file__).resolve().parent / "logs"
SALES_DATA_LOG_DIR.mkdir(exists_ok=True) #exists_ok=True is an error handling syntax that ensures that error is not thrown where the file exists


# This project has more than one pipeline delivering data to one data warehouse. We want to create a configuration for a general logging file that works for the three entities.  
# We want:
# a. each pipeline and datawarehouse to get its own log file
# b. the sequence from which the log is from to be visible in the pipeline's log file. # e.g cafe_sales_sequence.extract_cafe_sales 
# We can add a new pipeline or database by adding its name below here 
MODULE_NAMES = ["cafe_sales_pipeline_sequence", "restaurant_sales_pipeline_sequence", "retail_store_pipeline_sequence"] 


# We want to format how logs appear (basically we want it in json format)
class JSONFormatter(logging.Formatter):
    """
    This class is created to format logs records as single-line JSON objects.
    The class inherits Formatter function class under logging class, 
    but creates a new format function that overrides the original format function under logging.Formatter (that is Formatter.format());
    to the effect we subsume all the functions in logging.Formatter excluding format() which we would override
    so that instead of plain text logs which Formatter.format() would originally give, 
    we get a single line json format as we define in our new format function. 
    """
    # We inherit Formatter function class so that we can have the other subclasses functions the Formatter class has.
    # We make all the subclasses functions work for us, excluding of course the original format subclass function which we override with our new format function. 
    
    def format(self, record: logging.LogRecord) -> str: # With this, we create a new format function that overrides the original format function. 
        
        log_record = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname, 
            "logger": record.name, 
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        } 
        
        # We determine that traceback_objects in tuples format be converted to strings 
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        # We want to have all the other extra fields passed via logger.info(..., extra={....})
        standard_keys = logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
        for key, value in record.__dict__.items():
            if key not in standard_keys and key not in log_record: # We do not want these to affect our key-value pairs in standard_keys as well as thosealready set in log_record above
                try:
                    json.dumps(value) # confirm that it is JSON-serialisable 
                    log_record[key] = value # if it is, convert it to json (key & value)
                except (TypeError, ValueError):
                    log_record[key] = str(value) # if it isn't json-serialisable, keep it as string 
                    
        return json.dumps(log_record) # json.dumps produces the final output of log_record as a single JSON-format string. 

def building_logging_config() -> dict:
    """
    This function builds dictConfig dict, generating one handler + one logger per entry in MODULE_NAMES by lopping through each of them. 
    This is so that each pipeline can write its own file.
    """

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    }

    loggers = {}

    for name in MODULE_NAMES:
        handler_key = f"{name}_file"
        handlers[handler_key] = {
            "class": "logging.FileHandler",
            "filename": str(SALES_DATA_LOG_DIR / f"{name}.log"), 
            "formatter": "json",
            "delay": True, # We use "delay": True so that a file would not be created until a log exists for them 
        }

        loggers[name] = {
            "handlers":  ["console", handler_key],
            "level" : LOG_LEVEL,
            "propagate" : False, # We want this to be handled by this logger only and not passed up to the parent logger. We don't want the same logs printed twice. 
        }

    return {
        "version" : 1,
        "disable_existing_loggers": False,
        "Formatters": {
            "json": {"()": "logging_config.JSONFormatter"},
        },
    }


SALES_DATA_LOG_CONFIG = building_logging_config


def setup_logging() -> None:
    """"We would be calling this once, at the start of the program i.e sales_data_pipeline.py"""
    logging.config.dictConfig(SALES_DATA_LOG_CONFIG)
        
        

