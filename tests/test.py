import asyncio
from fastmcp import Client

async def main(): 
  # Connect via stdio to a local script
  async with Client("../server.py", env={"MCP_MODE": "stdio"}) as client: 
    tools = await client.list_tools()
    print(f"Available tools: {tools}")
    
    result = await client.call_tool(
        "getKakaoMapInfo", {"keyword": "restaurant in Gangnam"}
      )
    print(f"Result: {result.content[0].text}")
    result = await client.call_tool(
        "getGoogleMapInfo", {"keyword": "cafe in Barcelona"}
      )
    print(f"Result: {result.content[0].text}")
    result = await client.call_tool(
        "getGoogleRoute", 
        {"origin": "Central Park", "destination": "Times Square", "travelMode": "TRANSIT"}
      )
    print(f"Result: {result.content[0].text}")  
  
if __name__=="__main__":
  asyncio.run(main())