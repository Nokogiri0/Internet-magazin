<template>
    <div class="spec-item-container">
        <div class="spec-item-name">
            {{ name }}
        </div>
        <div class="spec-item-value">
            {{ value }}
        </div>
    </div>
</template>
<script setup>
defineProps({ name: String, value: String });
</script>
<style lang="scss" scoped>
.spec-item-container {
    display: flex;
    gap: 10px;
    padding: 5px 15px;
    border-radius: 5px;
    justify-content: space-between;


    &:nth-child(4n-2),
    &:nth-child(4n-3) {
        background-color: $secondary-bg;

    }

    &:nth-child(4n),
    &:nth-child(4n-1) {
        background-color: $accent-5;
    }



    .spec-item-name {}

    .spec-item-value {}

}
</style>