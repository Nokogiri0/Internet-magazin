<template>
    <div class="product-page-container">
        <div class="path">
            <router-link to="/#parent-categories">
                <span>Категории</span>
            </router-link>
            <Icon name="material-symbols:chevron-right-rounded" />
            <template v-for="(category, index) in product.path">
                <router-link
                    :to="{ name: 'category-id', params: { id: category.id } }"
                >
                    <span>{{ category.name }}</span>
                </router-link>
                <Icon
                    name="material-symbols:chevron-right-rounded"
                    v-if="index !== product.path.length - 1"
                />
            </template>
        </div>
        <div class="product-container">
            <div class="product-picture">
                <img :src="product.picture" />
            </div>
            <div class="product-info">
                <div class="product-name">
                    {{ product.name }}
                </div>
                <div class="product-description">
                    {{ product.description }}
                </div>
                <div class="splitter"></div>
                <div class="product-price">
                    <span>{{ product.price }}</span>
                    <Icon name="mingcute:currency-rubel-2-line" />
                </div>
                <div class="chose-button-container">
                    <Counter
                        :add_button_is_active="add_button_is_active"
                        :remove_button_is_active="remove_button_is_active"
                        :counter="counter"
                        @increment="increment"
                        @decrement="decrement"
                    />
                    <div class="cart-button" @click="addToCart">В корзину</div>
                </div>
                <div class="stores-and-delivery-container">
                    <div class="card">
                        <Icon name="fluent:building-shop-24-filled" />
                        <span
                            >Доступно в {{ product.available.length }} магазинах
                        </span>
                        <div class="items">
                            <div
                                class="market"
                                v-for="market in showed_available"
                            >
                                <div class="address">{{ market.address }}</div>
                                <div class="quantity">
                                    <b>{{ market.quantity }}</b> шт.
                                </div>
                            </div>
                            <div
                                class="market-show-more-button"
                                v-if="
                                    showed_available.length < available.length
                                "
                                @click="showMoreMarketsModalOpened = true"
                            >
                                Посмотреть все
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <Icon name="mdi:truck" />
                        <span
                            >Бесплатная доставка при заказе от 2 000
                            рублей.</span
                        >
                    </div>
                </div>
                <ModalDialog
                    :active="showMoreMarketsModalOpened"
                    @close="showMoreMarketsModalOpened = false"
                >
                    <template #content>
                        <div class="modal">
                            <div class="market" v-for="market in available">
                                <div class="address">{{ market.address }}</div>
                                <div class="quantity">
                                    <b>{{ market.quantity }}</b> шт.
                                </div>
                            </div>
                        </div>
                    </template>
                </ModalDialog>
                <ProductsSpecs :specs="product.characteristics"></ProductsSpecs>
            </div>
            <ProductsSpecs :specs="product.characteristics"></ProductsSpecs>
            <div class="reviews">
                <div class="headline">Отзывы</div>
                <div class="reviews-cotainer">
                    <ReviewCard
                        :review="review"
                        v-for="review in product.reviews"
                        @delete="deleteReview(review.id)"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const cartStore = useCartStore();
const { $toast } = useNuxtApp();
const route = useRoute();
const productId = computed(() => route.params.id || 1);
const product = ref(
    await Service.getProductApiV1ProductsProductIdGet(productId.value)
);
useHead({
    title: product.value.name,
});
const showMoreMarketsModalOpened = ref(false);
const totalQuantity = product.value.available.reduce(
    (partialSum, market) => partialSum + market.quantity,
    0
);
const deleteReview = (reviewId) => {
    product.value.reviews = product.value.reviews.filter(
        (review) => review.id !== reviewId
    );
};
const available = product.value.available.sort(
    (a, b) => a.quantity - b.quantity
);
const showed_available = available.slice(0, 3);
const counter = ref(1);
const add_button_is_active = computed(() => counter.value < totalQuantity);
const remove_button_is_active = computed(() => counter.value > 1);
const increment = () => {
    if (!add_button_is_active.value) return;
    counter.value++;
};
const decrement = () => {
    if (!remove_button_is_active.value) return;
    counter.value--;
};
const addToCart = async () => {
    if (!logined.value) {
        $toast.error(
            "Для добавления товара в корзину необходимо авторизоваться"
        );
        return;
    }
    await cartStore.addProductToCart(product.value, counter.value);
    counter.value = 1;
};
</script>
<style lang="scss" scoped>
.product-page-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    border-radius: 20px;
    padding: 10px;
    gap: 10px;

    .product-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 4rem;

        @include lg(true) {
            gap: 20px;
            grid-template-columns: 1fr;
        }

        .product-picture {
            @include flex-center;
            aspect-ratio: 1;

            img {
                border-radius: 10px;
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        }
        .reviews {
            display: flex;
            flex-direction: column;
            gap: 10px;

            .headline {
                font-size: larger;
                font-weight: bold;
            }

            .reviews-cotainer {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
        }

        .product-info {
            display: flex;
            flex-direction: column;
            gap: 10px;

            .splitter {
                background-color: rgba($quinary-bg, 0.5);
                width: 100%;
                height: 1.5px;
            }

            .product-name {
                font-size: 3rem;
                font-weight: bold;
            }

            .product-price {
                font-weight: bold;
                color: $accent-1;
                @include flex-center;
                font-size: 1.5rem;
            }

            .chose-button-container {
                display: flex;
                gap: 10px;
                // justify-content: space-between;

                .cart-button {
                    @include flex-center;
                    background-color: $accent-4;
                    color: $primary-text;
                    border-radius: 40px;
                    padding-inline: 20px;
                    flex-grow: 1;
                    user-select: none;
                    border: 1px dashed;
                    cursor: pointer;
                    white-space: nowrap;

                    &:hover {
                        color: $primary-text;
                        background-color: $accent-1;
                    }
                }
            }

            .stores-and-delivery-container {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: auto;

                @include lg(true) {
                    flex-direction: column-reverse;
                }

                .card {
                    @include flex-center;
                    border: 1px solid $quaternary-bg;
                    border-radius: 10px;
                    padding: 10px;
                    flex-grow: 1;
                    gap: 10px;
                    flex-direction: column;

                    .items {
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        flex-wrap: wrap;
                        width: 100%;

                        .market-show-more-button {
                            display: flex;
                            justify-content: center;
                            cursor: pointer;
                            user-select: none;
                        }
                    }
                }
            }

            .product-description {
                font-size: 1.1em;
                display: -webkit-box;
                -webkit-box-orient: vertical;
                -webkit-line-clamp: 3;
                overflow: hidden;
            }
        }
    }
}

.market {
    border: 1px dashed $quinary-bg;
    border-radius: 5px;
    display: flex;
    gap: 15px;
    padding: 5px;
    justify-content: space-between;
    flex-grow: 1;
}
</style>
