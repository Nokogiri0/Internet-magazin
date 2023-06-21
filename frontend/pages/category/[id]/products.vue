<template>
    <div class="products-page-container">
        <div>
            <Products :products="products" @updated="UpdateFilter" :name="current_category.name" />
        </div>
        <div class="load-more" @click="loadMore" v-if="ShowLoadMoreButton">
            Загрузить еще
        </div>
        <div class="pagination">
            <el-pagination @current-change="HandlePageChange" layout="prev, pager, next" :total="current_category.pages"
                :page-size="1" />
        </div>
    </div>
</template>
<script setup>
import { filters, default_filter, default_order } from "@/components/products/filters"
import { CategoriesService } from "@/client";


const route = useRoute();
const categoryId = computed(() => route.params.id || 1);
const current_category = await CategoriesService.getCategoryInfoApiV1CategoriesCategoryIdGet(
    categoryId.value
);
const pageQuery = route.query.page;
const page = ref(isNaN(pageQuery) ? 1 : pageQuery);

const filter = ref(default_filter.key)
const order = ref(default_order)



const getProductsFromPage = async (page) => {
    const catalog =
        await CategoriesService.getProductsFromCategoryApiV1CategoriesCategoryIdProductsGet(
            categoryId.value,
            filter.value,
            order.value,
            page
        );
    return catalog
}

const products = ref(await getProductsFromPage(page.value))


const HandlePageChange = async (page) => {
    products.value = await getProductsFromPage(page)
}

const UpdateFilter = data => {
    filter.value = data.key
    order.value = data.order
    console.log(data)
    page.value = 1
    HandlePageChange(page.value)
}

const ShowLoadMoreButton = ref(true)
const loadMore = async () => {
    page.value++
    const new_products = await getProductsFromPage(page.value)
    ShowLoadMoreButton.value = new_products.length > 0
    products.value = [...products.value, ...new_products]
}




</script>
<style lang="scss">
.products-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .load-more {
        display: flex;
        justify-content: center;
        cursor: pointer;
        border: 1px solid $accent-1;
        border-radius: 10px;
        padding: 2px;
        // width: min-content;
        // white-space: nowrap;

        &:hover {
            background-color: $accent-4;
            color: $primary-text;
            ;
        }
    }

    .pagination {
        display: flex;
        justify-content: center;

        .el-pagination {
            --el-pagination-bg-color: transparent;
            --el-pagination-button-disabled-bg-color: transparent;

            .el-pager li.is-active {
                color: $accent-1;
                border-style: dotted;
                border-color: $accent-1;
                border-width: 2px;
                border-radius: 15px;
            }

            button {
                transition: all 0.5s ease;

                &:disabled {
                    display: none;

                }
            }
        }
    }
}
</style>
