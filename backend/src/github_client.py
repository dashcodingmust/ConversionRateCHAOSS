import httpx

class GitHubClient:
    def __init__(self, headers):
        self.headers = headers

    async def get(self, url, params=None):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            return response.json()  