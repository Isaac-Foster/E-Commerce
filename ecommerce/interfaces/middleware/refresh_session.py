

""" @app.middleware("http")
async def refresh_session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if session_id and redis_client.exists(session_id):
        redis_client.expire(session_id, SESSION_TTL)  # Reinicia o TTL
    response = await call_next(request)
    return response """


""" SESSION_TTL = 3600  # 1 hora

def get_user_role(session_id: str) -> str:
    #Recupera o role do usuário a partir do Redis ou banco de dados.
    # Exemplo fictício; em produção, buscar no Redis ou DB
    return redis_client.get(session_id) or "guest"  # Default para não logados

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    role = get_user_role(session_id) if session_id else "guest"

    # Busca permissões do papel do usuário
    permissions = PERMISSIONS_DB.get(role, [])
    path = request.url.path
    method = request.method

    # Verifica se a rota é permitida
    for permission in permissions:
        if permission["route"] == path and permission["method"] == method:
            if session_id:
                redis_client.expire(session_id, SESSION_TTL)  # Atualiza TTL
            response = await call_next(request)
            return response

    # Bloqueia se não houver permissão
    raise HTTPException(status_code=403, detail="Forbidden") """


""" @app.middleware("http")
async def internal_api_middleware(request: Request, call_next):
    path = request.url.path

    # Verifica se a rota é uma API interna
    if path.startswith("/api/"):
        internal_key = request.headers.get("X-Internal-Key")
        if internal_key != INTERNAL_API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")

    response = await call_next(request)
    return response """



"""from fastapi import FastAPI, Request, Response, HTTPException
from datetime import datetime, timedelta
import uuid
import redis

app = FastAPI()

# Simulando o Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

SESSION_TIMEOUT = 3600  # Tempo de expiração do cookie em segundos (1 hora)
COOKIE_NAME = "session_token"

@app.middleware("http")
async def session_renewal(request: Request, call_next):
    # Tentando obter o cookie de sessão
    session_token = request.cookies.get(COOKIE_NAME)
    
    if session_token:
        # Verificando se o token de sessão existe no Redis
        username = redis_client.get(session_token)
        
        if username:
            # Usuário autenticado, renovando a expiração no Redis
            redis_client.expire(session_token, SESSION_TIMEOUT)  # Renovando o tempo de expiração no Redis
            
            # Renovando o cookie no cliente
            response = await call_next(request)
            response.set_cookie(
                key=COOKIE_NAME,
                value=session_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=SESSION_TIMEOUT,  # Renovando a expiração para 1 hora
                expires=(datetime.utcnow() + timedelta(seconds=SESSION_TIMEOUT)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            )
            return response
        else:
            raise HTTPException(status_code=401, detail="Sessão expirada ou inválida.")
    else:
        # Se o cookie não estiver presente, simplesmente passa para a próxima rota (usuário não autenticado)
        response = await call_next(request)
        return response
"""