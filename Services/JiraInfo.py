from helpers.Utils import Utils
class JiraInfo:
    def __init__(self, connection, ticket_name):
        self.ticket_name = ticket_name
        self.connection = connection

    def get_issue(self):
        return self.connection.issue(self.ticket_name)

    def get_ticket_description(self):
        return self.get_issue().fields.description

