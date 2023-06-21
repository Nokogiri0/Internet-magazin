<template>
    <div class="specs-container">
        <div class="title">Характеристики: </div>
        <div class="specs-items-container">
            <ProductsSpecsItem v-bind="spec" v-for="spec in specs_array"></ProductsSpecsItem>
        </div>

    </div>
</template>
<script setup>
const { specs } = defineProps({ specs: Object });
const specs_array = computed(() => Object.keys(specs).map((name) => ({ name: name, value: specs[name] })));

</script>
<style lang="scss" scoped>
.specs-container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    @include lg {
        grid-column: 1/3;
    }

    .title {
        font-weight: bolder;
        font-size: larger;
    }

    .specs-items-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        border: 1px solid $tertiary-bg;
        gap: 15px;
        padding: 25px;
        border-radius: 15px;

        @include lg {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
        }
    }
}
</style>