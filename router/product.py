import time

from fastapi import APIRouter, Depends, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional

"""
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List
"""

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']


async def time_consuming_functionality():
    time.sleep(5)
    return "ok"


@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get('/all')
async def get_all_product():
    await time_consuming_functionality()
    # return products
    data = " ".join(products)
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


@router.get('/withheader')
def get_products(
        response: Response,
        custom_header: Optional[str] = Header(None),  # We can always declare a list
        test_cookie: Optional[str] = Cookie(None)
):
    if custom_header:
        response.headers['custom_response_header'] = ", ".join(custom_header)
    return {
        "data": products,
        "custom_header": custom_header,
        "my_cookie": test_cookie
    }


@router.get('/{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "description": "Returns the html for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available"
            }
        },
        "description": "A clear text error message"
    },
})
def get_single_product(id: int):
    if id > len(products):
        out = 'Product is not available'
        return PlainTextResponse(status_code=404, content=out, media_type='text/plain')
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
            width: 500px
            height: 40px
            border 2px inset green
            background-color: lightblue
            text-align: center
            }}
            </style>
        </head>
        <div class = "product">{product}</div>
        """
        return HTMLResponse(content=out, media_type='text/html')
