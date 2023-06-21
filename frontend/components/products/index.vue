<template>
    <div class="products-container">
        <div class="product-filter">
            <div :class="['filter-item', { active: filter.key == current_filter }, { desc: is_desc }]"
                @click="HandleClick(index)" v-for="(filter, index) in filters">
                <Icon name="material-symbols:arrow-downward"></Icon>
                <span> {{ filter.name }}</span>

            </div>
            <div class="category-name">
                {{ name }}
            </div>
        </div>
        <div class="products-container-items">
            <ProductsItem :product="product" v-for="product in products" />
        </div>
    </div>
</template>
<script setup>
import { filters, default_filter, default_order } from "@/components/products/filters"
const { products, name } = defineProps({
    products: { type: Array, required: true },
    name: { type: String, required: true },
})

const current_filter = ref(default_filter.key)

const is_desc = ref(default_order)

const emit = defineEmits([
    "updated"
])


const HandleClick = (index) => {
    const selected_filter = filters[index].key
    const is_current = current_filter.value === selected_filter
    current_filter.value = selected_filter
    is_desc.value = is_current ? !is_desc.value : false

    emit("updated", { key: selected_filter, order: is_desc.value ? "desc" : "asc" })
}

</script>

<style lang="scss">
.products-container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .product-filter {
        display: flex;
        gap: 10px;


        .filter-item {
            display: flex;
            align-items: center;
            gap: 2px;
            background-color: rgba($color: #000000, $alpha: 0.1);
            border-radius: 10px;
            padding: 5px 10px;
            user-select: none;
            cursor: pointer;


            &.active {
                svg {
                    opacity: 1;
                    width: 15px;
                }

                &.desc {
                    svg {
                        rotate: 180deg;
                    }
                }
            }


            svg {
                opacity: 0;
                width: 0;
                transition: width .2s, opacity .2s, rotate .2s;
            }
        }

        .category-name {
            margin-left: auto;
            color: $accent-1;
            font-weight: bold;
            font-size: larger;
            margin-block: auto;

        }

    }

    .products-container-items {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
    }

}
</style>