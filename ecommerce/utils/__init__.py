from httpx import AsyncClient


#http_client
hc = AsyncClient( 
    http2=True,
    timeout=40
)