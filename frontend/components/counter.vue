<template>
    <div class="count-selector">
        <div
            :class="['count-button', { active: remove_button_is_active }]"
            @click="emit('decrement')"
        >
            <Icon name="material-symbols:remove-rounded"></Icon>
        </div>
        <div class="count-value">
            {{ counter }}
        </div>
        <div
            :class="['count-button', { active: add_button_is_active }]"
            @click="emit('increment')"
        >
            <Icon name="material-symbols:add-rounded" />
        </div>
    </div>
</template>
<script setup>
const emit = defineEmits(["decrement", "increment"]);
const { counter, remove_button_is_active, add_button_is_active } = defineProps({
    counter: Number,
    remove_button_is_active: Boolean,
    add_button_is_active: Boolean,
});
</script>
<style lang="scss" scoped>
.count-selector {
    @include flex-center;
    gap: 30px;
    border-radius: 50px;
    background-color: $secondary-bg;
    padding: 10px;

    .count-value {
        @include flex-center;
        min-width: 20px;
    }

    .count-button {
        @include flex-center;
        height: 40px;
        width: 40px;
        border-radius: 50%;
        user-select: none;
        color: $quaternary-text;

        svg {
            height: 20px;
            width: 20px;
        }

        &.active {
            color: $primary-text;
            cursor: pointer;

            &:hover {
                background-color: $tertiary-bg;
            }
        }
    }
}
</style>
