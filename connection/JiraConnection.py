from jira import JIRA

class JiraConnection:
    def __init__(self, jira_url, email, api_token):
        self.jira_url = jira_url
        self.email = email
        self.api_token = api_token

    def connect(self):
        # Utilisation de 'server' au lieu de 'jira_url'
        return JIRA(
            
            basic_auth=(self.email, self.api_token),
            options={"server": "https://bourmechfarah3.atlassian.net/"},
            max_retries=5,


        )
