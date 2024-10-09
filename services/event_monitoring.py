"""
This module provides a function to log significant events to a file.
For the real app, it might be replaces with the real event monitoring system.
"""

import logging

# Configure logging to write to events.log file
# In a real application, this service would use a more robust logging system, e.g. Datadog or Kibana
logging.basicConfig(
    filename="events.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def log_event(message):
    """
    Log significant events to the events.log file.
    """
    logging.info(message)
