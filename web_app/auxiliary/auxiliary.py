import string
import logging

class StreamToLogger(object):
      """
      Fake file-like stream object that redirects writes to a logger instance.
      """
      def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

      def write(self, buf):
            for line in buf.rstrip().splitlines():
                  self.logger.log(self.log_level, line.rstrip())

      def flush(self):
          pass


def write_to_log_error(buf):

    log = logging.getLogger('ROOT_LOGGER')

    for line in buf.rstrip().splitlines():
        log.error(line)


def write_to_log_info(buf):

    log = logging.getLogger('ROOT_LOGGER')

    for line in buf.rstrip().splitlines():
        log.info(line)