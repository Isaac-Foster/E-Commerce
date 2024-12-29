from fastapi import APIRouter, Request, Response

from ecommerce.schema.users.user import UserSignup, UserSignin


router = APIRouter(prefix='/users', tags=["public"])

@router.post("/signup")
async def register(data: UserSignup, request: Request):
    response = data.register()
    return {"status": response}


@router.post("/signin")
async def signin(data: UserSignin, request: Request, response: Response):
    response = data.verify()

    if response:
        """ 
        #set the cookie and save the session cookie in redis in the future

        response.set_cookie(
        httponly=True
            
        ) """

        return {"session": response}
    return {"session": response}
