from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.post("/showSummary", {"email": "test@userid.co.uk"})

    @task
    def view_competitions(self):
        # '/showSummary' is the index.html page.
        self.client.post("/showSummary", {"email": "test@userid.co.uk"})

