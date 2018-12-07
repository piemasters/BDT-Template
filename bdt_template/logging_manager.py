import logging


class LoggingManager:

    @staticmethod
    def bdt_logger(status, file_id, message, matched_file='', error=''):
        """ Logs passed values in a set format

        :param status: Logging level (INFO, ERROR)
        :param file_id: Identifier for the affected file
        :param message: Error or success message
        :param matched_file: (Optional) Path to the affected file
        :param error: (Optional) Error message extracted from matched file
        """
        # Format the message
        full_message = str(status).upper() + ': [' + str(file_id) + '] - ' + str(message)

        # If there is a matched file list the name
        if matched_file != '':
            full_message += '. File found: [' + str(matched_file) + ']'

        # If there is an error message add it
        if error != '':
            full_message += ' Error message: ' + error

        # Print the message to the console
        print(full_message)

        # Correctly log the message
        if status.lower() == 'error':
            logging.error(full_message)
        elif status.lower() == 'info':
            logging.info(full_message)
