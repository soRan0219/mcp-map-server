import os, httpx
from dotenv import load_dotenv
from typing import Union
from fastmcp import FastMCP

mcp = FastMCP(name="mcp-map")

load_dotenv("mcp_map_server/env/data.env")
KAKAO_APP_KEY = os.getenv('kakao_app_key')
KAKAO_URL = os.getenv('kakao_url')
kakao_headers = {
  "Authorization": "KakaoAK "+KAKAO_APP_KEY,
  "Accept": "application/json;charset=UTF-8",
  "Content-Type": "application/json;charset=UTF-8"
}

GOOGLE_API_KEY = str(os.getenv('google_api_key'))
GOOGLE_MAP_URL = str(os.getenv('google_map_url'))
GOOGLE_ROUTE_URL = str(os.getenv('google_route_url'))
google_headers = {
  "X-Goog-Api-Key": GOOGLE_API_KEY, 
  "Content-Type": "application/json;charset=UTF-8"
}

@mcp.tool(
  name="getKakaoMapInfo", 
  description="Kakao Map API-powered tool for finding places in Korea by keyword (e.g. cafe, hospital, or street name)"
)
async def getKakaoMapInfo(keyword: str) -> dict: 
  """ 
  Search for location information using Kakao Map API
  
  Args:
    keyword(str): The keyword to search for in Kakao Map (e.g. 'restaurant in Gangnam')
  """
  async with httpx.AsyncClient() as client: 
    response = await client.get(KAKAO_URL, params={"query":keyword}, headers=kakao_headers)
    info = response.json()
    return info

@mcp.tool(
  name="getGoogleMapInfo",
  description="Google Map API-powered tool for finding places outside Korea by keyword (e.g. cafe, hospital, or street name)"
)
async def getGoogleMapInfo(keyword: str) -> dict: 
  """
  Search for location information using Google Map API
  
  Args:
    keyword(str): The keyword to search for in Google Map (e.g. 'pizza restaurant in New York')
  """
  async with httpx.AsyncClient() as client: 
    google_map_headers = google_headers
    google_map_headers["X-Goog-FieldMask"] = "places.displayName,places.formattedAddress,places.types"
    response = await client.post(GOOGLE_MAP_URL, params={"textQuery":keyword}, headers=google_map_headers)
    info = response.json()
    return info

@mcp.tool(
  name="getGoogleRoute",
  description="Google Map API-powered tool for finding the optimal route from a given location to a destination"
)
async def getGoogleRoute(
  origin: str, destination: str, travelMode: str, 
  routingPreference: Union[str, None]=None
  ) -> dict:
  """ 
  Search for the best route from a specific location to another
  
  Args: 
    origin(str): address of origin location
    destination(str): address of destination
    travelMode(str): travel mode (DRIVE, TRANSIT, TWO_WHEELER, BICYCLE, WALK)
    routingPreference(str | None): routing preference (TRAFFIC_UNAWARE, TRAFFIC_AWARE, TRAFFIC_AWARE_OPTIMAL)
  """
  async with httpx.AsyncClient() as client: 
    google_route_headers = google_headers
    google_route_headers["X-Goog-FieldMask"] = "routes.duration,routes.distanceMeters,routes.description,routes.travelAdvisory,routes.legs"
    route_data = {
      "origin":{
        "address": origin
      },
      "destination":{
        "address": destination
      },
      "travelMode": travelMode
    }
    if routingPreference!=None: 
      route_data["routingPreference"] = routingPreference
    
    response = await client.post(GOOGLE_ROUTE_URL, json=route_data, headers=google_route_headers)
    route = response.json()
    return route

if __name__=="__main__": 
  mcp.run()