<template>
    <NuxtLink
        :to="{ name: 'products-id', params: { id: product.id } }"
        class="product-container shadow"
    >
        <div class="product-img">
            <img :src="product.picture" alt="product" />
        </div>
        <div class="product-headline">{{ product.name }}</div>
        <div class="product-info">
            <div class="product-price">
                <span>{{ product.price }}</span>
                <Icon name="mingcute:currency-rubel-2-line" />
            </div>
        </div>
    </NuxtLink>
</template>
<script setup>
const { product } = defineProps({
    product: { type: Object, required: true },
});
</script>
<style lang="scss" scoped>
.product-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 3px;
    padding: 5px;
    border-radius: 15px;
    background-color: rgba($color: #000000, $alpha: 0.05);

    &:hover {
        background-color: rgba($color: #000000, $alpha: 0.1);
    }

    // border: 0.05px solid grey;
    .product-headline {
        // font-weight:;
    }

    .product-info {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;

        .product-price {
            color: $accent-1;
            font-weight: bold;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            height: min-content;

            span {
                margin-top: 1%;
            }

            svg {
                height: 100%;
            }
        }

        .product-avilable {
        }
    }

    .product-img {
        display: flex;
        overflow: hidden;
        border-radius: 10px;
        width: 100%;
        aspect-ratio: 1;

        img {
            object-fit: cover;
            height: 100%;
            width: 100%;
        }
    }
}
</style>
