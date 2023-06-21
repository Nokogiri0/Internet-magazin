<template>
    <div class="stock-container">
        <div class="stock-info">
            <div class="stock_img">
                <img :src="stock.stock.picture" />
            </div>
            <span>{{ stock.stock.name }}</span>
            {{ total_price }}
        </div>
        <span>Товары в акции:</span>
        <div class="stock-products">
            <div
                class="stock-product"
                v-for="stock_product in stock.stock.products"
            >
                <img :src="stock_product.product.picture" />
                <div class="stock-product-info">
                    <div class="stock-title">
                        {{ stock_product.product.name }}
                    </div>
                    <div class="stock-price">
                        Цена за все: {{ stock_product.price }}
                    </div>
                    <div class="stock-quantity">
                        <span>Количество</span>
                        {{ stock_product.quantity }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
const { stock } = defineProps({ stock: Object });
const total_price = computed(() =>
    stock.stock.products.reduce((sum, product) => sum + product.price, 0)
);
</script>
<style lang="scss" scoped>
.stock-container {
    display: flex;
    padding: 10px;
    flex-direction: column;
    background-color: $secondary-bg;
    border-radius: 20px;

    .stock-info {
        display: flex;
        gap: 10px;

        img {
            object-fit: cover;
            width: 150px;
            height: 150px;
            border-radius: 10px;
            overflow: hidden;
        }
    }

    .stock-products {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 10px;
        padding-top: 10px;

        .stock-product {
            display: grid;
            background-color: $tertiary-bg;
            padding: 5px;
            grid-template-columns: 100px 1fr;
            border-radius: 10px;

            img {
                object-fit: cover;
                width: 100%;
                height: 100%;
                border-radius: 5px;
                overflow: hidden;
            }

            .stock-product-info {
                display: flex;
                flex-direction: column;
                gap: 5px;
                padding-left: 10px;
            }
        }
    }
}
</style>
