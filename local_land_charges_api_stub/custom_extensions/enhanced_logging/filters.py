from flask import ctx
from flask import g
from flask import request
import logging


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """Provide some extra variables to be placed into the log message """

        # If we have an app context (because we're servicing an http request) then get the trace id we have
        # set in g (see app.py)
        if ctx.has_app_context():
            log_record.trace_id = g.trace_id
            log_record.msg = "Endpoint: {}, Method: {}, Caller: {}.{}[{}], {}".format(
                request.endpoint, request.method, log_record.module, log_record.funcName, log_record.lineno,
                log_record.msg)
        else:
            log_record.trace_id = 'N/A'
        return True
