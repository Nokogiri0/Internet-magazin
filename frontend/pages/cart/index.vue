<template>
    <div class="cart-title">Корзина:</div>
    <div class="cart-container">
        <div class="cart-item-container shadow-lg">
            <div class="empty" v-if="cartIsEmpty">Корзина пуста</div>
            <div class="items" v-if="hasProducts">
                <div class="items-title">Товары</div>
                <div class="items-container" v-if="cartStore.products">
                    <CartProduct
                        :cart-product="cart_product"
                        v-for="cart_product in cartStore.products"
                    />
                </div>
            </div>
            <div class="items" v-if="hasStocks">
                <div class="items-title">Акции</div>
                <div class="items-container">
                    <CartStock
                        :stock="stock"
                        v-for="stock in cartStore.stocks"
                    ></CartStock>
                </div>
            </div>
        </div>

        <div class="options-bar shadow-lg">
            <div class="options-title">Условия заказа</div>
            <div class="result-products" v-if="hasProducts">
                <div class="product" v-for="cart_product in cartStore.products">
                    <div class="product-name">
                        {{ cart_product.product.name }}
                    </div>
                    <div class="product-price">
                        <div class="product-count">
                            {{ cart_product.quantity }}шт. x
                        </div>
                        <div class="product-price-value">
                            {{ cart_product.product.price }} руб.
                        </div>
                    </div>
                </div>
            </div>
            <div class="result-products" v-if="hasStocks">
                <span>Акции</span>
                <div class="product" v-for="cart_stock in cartStore.stocks">
                    <div class="product-name">
                        {{ cart_stock.stock.name }}
                    </div>
                    <div class="product-price">
                        <div class="product-count">
                            {{ cart_stock.quantity }}шт. x
                        </div>
                        <div class="product-price-value">
                            {{ cart_stock.stock.price }} руб.
                        </div>
                    </div>
                </div>
            </div>
            <div class="total-container">
                <div class="title">Итого:</div>
                <div class="total-value">{{ cartStore.total_price }} руб.</div>
            </div>
            <div
                class="buy-button"
                v-if="!cartIsEmpty"
                @click="selectMarketModal = true"
            >
                Перейти к оформлению
            </div>
            <ModalDialog
                :active="selectMarketModal"
                @close="selectMarketModal = false"
                head-text="Выберите магазин"
            >
                <template #content>
                    <div class="markets">
                        <div
                            class="market"
                            v-for="market in cartStore.markets"
                            @click="buy(market.id)"
                        >
                            {{ market.address }}
                        </div>
                    </div>
                </template>
            </ModalDialog>
        </div>
    </div>
</template>
<script setup>
import { useCartStore } from "~~/stores/cart";
import { storeToRefs } from "pinia";
const cartStore = useCartStore();
const { cartIsEmpty, hasProducts, hasStocks } = storeToRefs(cartStore);
const selectMarketModal = ref(false);

const buy = async (market_id) => {
    selectMarketModal.value = false;
    const order = await cartStore.buy(market_id);
    return navigateTo({
        name: "orders-id",
        params: { id: order.id },
    });
};
</script>
<style lang="scss" scoped>
.markets {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .market {
        background-color: $accent-5;
        border-radius: 10px;
        padding: 10px;
        cursor: pointer;

        &:hover {
            background-color: $accent-4;
        }
    }
}
.cart-title {
    font-size: x-large;
    font-weight: bolder;
}

.cart-container {
    display: grid;
    grid-template-columns: 1fr min-content;
    min-height: 270px;
    gap: 10px;
    .empty {
        @include flex-center;
        height: 100%;
    }
    .cart-item-container {
        border: 2px solid $border-color;
        border-radius: 10px;
        padding: 10px;

        .items-title {
            border-bottom: 1px solid $quinary-bg;
            padding: 10px;
            font-size: large;
        }
        .items {
            display: flex;
            flex-direction: column;

            .items-container {
                padding-top: 10px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
        }
    }

    .options-bar {
        display: flex;
        flex-direction: column;
        border: 2px solid $border-color;
        border-radius: 10px;
        padding: 10px;
        min-width: 300px;
        height: min-content;
        min-height: 270px;

        .options-title {
            border-bottom: 1px solid $quinary-bg;
            padding: 10px;
            font-size: large;
        }

        .result-products {
            display: flex;
            flex-direction: column;
            padding-bottom: 10px;

            .product {
                display: flex;
                justify-content: space-between;
                align-items: center;

                .product-name {
                    font-size: smaller;
                }

                .product-price {
                    @include flex-center;
                    gap: 5px;

                    .product-count {
                        font-size: smaller;
                    }

                    .product-price-value {
                        font-size: smaller;
                    }
                }
            }
        }

        .total-container {
            margin-top: auto;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: smaller;
            font-weight: bold;
        }

        .buy-button {
            @include flex-center;
            padding: 10px;
            background-color: $accent-5;
            border-radius: 10px;
            border: 1px dashed black;
            cursor: pointer;
            user-select: none;

            &:hover {
                background-color: $accent-4;
            }
        }
    }
}
</style>
