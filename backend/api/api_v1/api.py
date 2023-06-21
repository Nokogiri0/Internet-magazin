from fastapi import APIRouter
from backend.api.api_v1.endpoints import auth, catalog, user, files, products, reviews, stocks, orders, markets, order_messages, slider, cart

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(files.router)
api_v1_router.include_router(catalog.categories_router)
api_v1_router.include_router(products.router)
api_v1_router.include_router(cart.router)
api_v1_router.include_router(reviews.router)
api_v1_router.include_router(stocks.router)
api_v1_router.include_router(orders.router)
api_v1_router.include_router(markets.router)
api_v1_router.include_router(order_messages.router)
api_v1_router.include_router(slider.router)
