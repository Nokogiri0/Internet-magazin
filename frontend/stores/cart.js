import { defineStore } from "pinia";
import { Service, OrdersService } from "@/client";
import { useLocalStorage } from "@vueuse/core";
import { useAuthStore } from "./auth";
export const useCartStore = defineStore({
    id: "card",
    state: () => ({
        _products: useLocalStorage("products", []),
        fetched: false,
        _stocks: useLocalStorage("sales", []),
        _markets: null,
    }),
    getters: {
        products() {
            const { logined } = useAuthStore();
            if (logined) {
                if (!this.fetched) {
                    this.getCart();
                }
            }
            return this._products;
        },
        stocks() {
            const { logined } = useAuthStore();
            if (logined) {
                if (!this.fetched) {
                    this.getCart();
                }
            }
            return this._stocks;
        },
        hasProducts() {
            return this.products.length > 0;
        },
        hasStocks() {
            return this.stocks.length > 0;
        },
        cartIsEmpty() {
            return !this.hasProducts && !this.hasStocks;
        },
        total_products_price() {
            return this.products.reduce(
                (total, product) =>
                    total + product.product.price * product.quantity,
                0
            );
        },
        total_stocks_price() {
            return this._stocks.reduce(
                (total, cart_stock) =>
                    total +
                    cart_stock.stock.products.reduce(
                        (total_product_price, product) =>
                            total_product_price + product.price,
                        0
                    ),
                0
            );
        },
        total_price() {
            return this.total_products_price + this.total_stocks_price;
        },
        products_count() {
            return this._products.length;
        },
        sales_count() {
            return this._stocks.length;
        },
        count() {
            return this.products_count + this.sales_count;
        },
        markets() {
            if (!this._markets) {
                return this.getMarkets();
            }
            return this._markets;
        },
    },
    actions: {
        async addProductToCart(product, quantity) {
            const { logined } = useAuthStore();
            if (!logined) {
                return;
            }

            var old_product_value = this.products.find(
                (cart_product) => cart_product.product?.id === product.id
            );
            const new_cart_product =
                await Service.addProductToCartApiV1CartProductProductIdPost(
                    product.id,
                    quantity
                );
            if (old_product_value) {
                this._products = this._products.map((cart_product) =>
                    cart_product.product.id !== product.id
                        ? cart_product
                        : new_cart_product
                );
            } else {
                this._products.push(new_cart_product);
            }
        },
        async getCart() {
            const { products, stocks, total_price } =
                await Service.getCartInfoApiV1CartGet();
            this._products = products;
            this._stocks = stocks;
            this.fetched = true;
        },
        async decreaseProductQuantity(product_id) {
            const product_index = this._products.findIndex(
                (cart_product) => cart_product.product.id === product_id
            );
            if (product_index !== -1) {
                const result_quantity =
                    this._products[product_index].quantity - 1;
                if (result_quantity > 0) {
                    this._products[product_index].quantity = result_quantity;

                    await Service.changeProductQuantityApiV1CartProductCartProductIdQuantityPut(
                        this._products[product_index].cart_product_id,
                        result_quantity
                    );
                } else {
                    await this.removeProductFromCart(
                        this._products[product_index].product
                    );
                }
            }
        },
        async getMarkets() {
            const markets = await Service.getMarketsApiV1MarketsGet();
            this._markets = markets;
            return markets;
        },
        async increaseProductQuantity(product_id) {
            const product_index = this._products.findIndex(
                (cart_product) => cart_product.product.id === product_id
            );
            if (product_index !== -1) {
                const result_quantity =
                    this._products[product_index].quantity + 1;
                this._products[product_index].quantity = result_quantity;

                await Service.changeProductQuantityApiV1CartProductCartProductIdQuantityPut(
                    this._products[product_index].cart_product_id,
                    result_quantity
                );
            }
        },

        async removeProductFromCart(product) {
            const { logined } = useAuthStore();

            if (logined) {
                const stock_product_id = this._products.find(
                    (cart_product) => cart_product.product.id === product.id
                );

                if (stock_product_id) {
                    await Service.deleteProductFromCartApiV1CartProductProductIdDelete(
                        product.id
                    );
                }
            }
            this._products = this._products.filter(
                (cart_product) => cart_product.product.id !== product.id
            );
        },
        async buy(market_id) {
            const { logined } = useAuthStore();
            if (!logined) {
                return;
            }
            const order = await OrdersService.createOrderApiV1OrdersPost({
                market_id: market_id,
                delivery_address_id: null,
                products: this._products.map((cart_product) => ({
                    product_id: cart_product.product.id,
                    quantity: cart_product.quantity,
                })),
                stocks: this._stocks.map((cart_stock) => cart_stock.stock.id),
            });
            this._products = [];
            this._stocks = [];
            return order;
        },
    },
});
