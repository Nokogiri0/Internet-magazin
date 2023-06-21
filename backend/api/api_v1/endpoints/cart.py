from fastapi import HTTPException, Depends, APIRouter, status
from backend.crud.crud_cart import CRUDCart
from backend.crud.crud_products import CRUDProduct
from backend.crud.crud_stocks import CRUDStocks
from backend.helpers.auth import Authenticate
from backend.schemas.cart import CartInfo, ProductQuantity, StockQuantity

router = APIRouter(tags=['Корзина'], prefix='/cart')


@router.get('', response_model=CartInfo)
def get_cart_info(auth: Authenticate = Depends(Authenticate())):
    crud_cart = CRUDCart(auth.db)
    cart_products = crud_cart.get_cart_products(auth.current_user_id)
    cart_stocks = crud_cart.get_cart_stocks(auth.current_user_id)
    total_price_products = sum(
        [product.product.price * product.quantity for product in cart_products])
    total_price_stocks = sum(
        [sum([stock_product.product.price for stock_product in cart_stock.stock.products]) for cart_stock in cart_stocks])
    total_price = total_price_products + total_price_stocks
    return CartInfo(
        products=cart_products,
        stocks=cart_stocks,
        total_price=total_price
    )


@router.post('/product/{product_id}', response_model=ProductQuantity, status_code=status.HTTP_201_CREATED)
def add_product_to_cart(product_id: int, quantity: int, auth: Authenticate = Depends(Authenticate())):
    crud_product = CRUDProduct(auth.db)
    product = crud_product.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_cart = CRUDCart(auth.db)
    return crud_cart.add_product_to_cart(product_id, quantity, auth.current_user_id)


@router.post('/stock/{stock_id}', response_model=StockQuantity, status_code=status.HTTP_201_CREATED)
def add_stock_to_cart(stock_id: int, quantity: int, auth: Authenticate = Depends(Authenticate())):
    crud_stock = CRUDStocks(auth.db)
    stock = crud_stock.get_stock_by_id(stock_id=stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_cart = CRUDCart(auth.db)
    return crud_cart.add_stock_to_cart(stock_id, quantity, auth.current_user_id)


@router.put('/product/{cart_product_id}/quantity', response_model=ProductQuantity)
def change_product_quantity(cart_product_id: int, quantity: int, auth: Authenticate = Depends(Authenticate())):
    crud_cart = CRUDCart(auth.db)
    cart_product = crud_cart.get_cart_product_by_id(cart_product_id)
    if not cart_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден в корзине")
    return crud_cart.change_product_quantity(cart_product=cart_product, quantity=quantity)


@router.put('/stock/{cart_stock_id}/quantity', response_model=StockQuantity)
def change_stock_quantity(cart_stock_id: int, quantity: int, auth: Authenticate = Depends(Authenticate())):
    crud_cart = CRUDCart(auth.db)
    cart_stock = crud_cart.get_cart_stock_by_id(cart_stock_id)
    if not cart_stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден в корзине")
    return crud_cart.change_stock_quantity(cart_stock=cart_stock, quantity=quantity)


@router.delete('/clear', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(auth: Authenticate = Depends(Authenticate())):
    crud_cart = CRUDCart(auth.db)
    crud_cart.clear_cart(auth.current_user_id)


@router.delete('/product/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product_from_cart(product_id: int, auth: Authenticate = Depends(Authenticate())):
    crud_product = CRUDProduct(auth.db)
    product = crud_product.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_cart = CRUDCart(auth.db)
    crud_cart.delete_product_from_cart(auth.current_user_id, product_id)


@router.delete('/stock/{stock_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_from_cart(stock_id: int, auth: Authenticate = Depends(Authenticate())):
    crud_stock = CRUDStocks(auth.db)
    stock = crud_stock.get_stock_by_id(stock_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_cart = CRUDCart(auth.db)
    crud_cart.delete_stock_from_cart(auth.current_user_id, stock_id)
