<template>
    <div class="product-container">
        <div class="line">
            <div class="product-img">
                <img :src="cartProduct.product.picture" />
            </div>
            <div class="info">
                <div class="product-title">{{ cartProduct.product.name }}</div>
                <div class="description">
                    {{ cartProduct.product.description }}
                </div>
            </div>
        </div>
        <div class="line">
            <Counter
                add_button_is_active
                remove_button_is_active
                :counter="cartProduct.quantity"
                @increment="increment"
                @decrement="decrement"
                class="product-counter"
            />

            <div class="total">
                <div class="value">{{ totalProductPrice }} ₽</div>
                <div class="remove" @click="remove">
                    <Icon name="material-symbols:delete" />
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { useCartStore } from "@/stores/cart";
const cartStore = useCartStore();
const { cartProduct } = defineProps({ cartProduct: Object });
const increment = async () => {
    await cartStore.increaseProductQuantity(cartProduct.product.id);
};
const decrement = async () => {
    await cartStore.decreaseProductQuantity(cartProduct.product.id);
};
const remove = async () => {
    await cartStore.removeProductFromCart(cartProduct.product);
};
const totalProductPrice = computed(() => {
    return cartProduct.product.price * cartProduct.quantity;
});
</script>
<style lang="scss" scoped>
.product-container {
    display: flex;
    padding: 10px;
    background-color: $secondary-bg;
    border-radius: 20px;
    gap: 10px;
    flex-direction: column;
    .line {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 10px;

        .total {
            background-color: $primary-bg;
            display: flex;
            align-items: center;
            border-radius: 10px;
            gap: 10px;
            padding: 10px;

            .value {
                font-size: large;
                font-weight: bold;
            }

            .remove {
                @include flex-center;
                margin-left: auto;
                aspect-ratio: 1;
                height: 100%;
                border-radius: 5px;
                background-color: $secondary-bg;
                cursor: pointer;

                &:hover {
                    background-color: $tertiary-bg;
                }

                svg {
                    width: 20px;
                    height: 20px;
                }
            }
        }
    }
    .product-img {
        display: flex;
        width: 100%;
        height: 100%;
        aspect-ratio: 1;
        border-radius: 10px;
        overflow: hidden;

        img {
            object-fit: cover;
        }
    }

    .product-counter {
        background-color: $primary-bg;
        height: min-content;
        border-radius: 10px;
    }
    .info {
        display: flex;
        flex-direction: column;
        overflow: hidden;

        .product-title {
            font-size: large;
            height: min-content;
            font-weight: bold;
        }

        .description {
            max-height: 190px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    }
}
</style>
