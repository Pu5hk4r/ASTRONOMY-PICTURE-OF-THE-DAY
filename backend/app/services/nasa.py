"""
WHY a separate NASA service?

Your route handlers should not contain raw HTTP calls to NASA.
If they do, every route that needs NASA data has to:
  - Know the base URL
  - Append the API key
  - Handle errors
  - Parse the response

That's four responsibilities duplicated everywhere. The Service Layer
pattern puts all NASA communication in one place. Routes just call
nasa_service.get_apod_for_date(date) and get back a clean Python object.

HOW httpx async works:
  httpx.AsyncClient is like requests but non-blocking.
  `async with AsyncClient() as client:` opens a connection pool,
  `await client.get(url)` waits for the response without blocking other requests.
"""

# talks to NASA, returns NasaApodRaw

from datetime import date
from app.core.config import settings

import httpx

from app.core.config import settings
from app.schemas.apod import NasaApodRaw


NASA_BASE_URL = "https://api.nasa.gov/planetary/apod"

class NasaService:
    def __init__(self):
        # WHY a persistent client instead of creating one per request?
        # AsyncClient maintains a connection pool. Reusing it avoids
        # the overhead of TCP handshake + TLS for every single NASA call.
        self.client = httpx.AsyncClient(
            timeout=10.0,           #don't wait  more than 10s for NASA
            base_url=NASA_BASE_URL,
        )

    async def _get(self, params:dict)-> dict:
        """
        Internal method — always injects the API key.
        WHY private (_get)? Callers shouldn't think about auth.
        They just
        """
        params["api_key"] = settings.nasa_api_key
        response = await self.client.get("",params=params)

        # WHY raise_for_status?
        # NASA returns HTTP 429 when you're rate limited, 403 for bad key, etc.
        # raise_for_status() turns non-2xx responses into exceptions
        # so your calling code doesn't have to check response.status_code manually.
        response.raise_for_status()
        return response.json()
    
    async def get_apod_today(self)->NasaApodRaw:
        '''Fetch today's Astronomy Picture  of the Day.'''
        data = await self._get({})
        return NasaApodRaw(**data)

    async def get_apod_for_date(self,target_date:date) -> NasaApodRaw:
        '''Fetch APOD for a specific date. NASA accepts YYYY-MM-DD format.'''
        data = await self._get({"date":target_date.isoformat()})
        return NasaApodRaw(**data)
    
    async def get_apod_range(self, start:date, end:date)->list[NasaApodRaw]:
        """
        Fetch a range of APODs in a single NASA API call.
        NASA supports start_date + end_date params — much more efficient
        than looping and calling get_apod_for_date() for each day.
        """
        data = await self._get({
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        })
        # Range endpoint returns a list
        return [NasaApodRaw(**item) for item in data]

    async def close(self):
        await self.client.aclose()


nasa_service = NasaService()


#test

if __name__ == "__main__":
    import asyncio

    async def test():
        result = await nasa_service.get_apod_today()
        print(result)

    asyncio.run(test())





        
