<template>
    <div class="error">
        <div class="error__content">
            <div class="error__content__title">
                {{ errorData.statusCode }}
            </div>
            <div class="error__content__message">
                {{ errorData.message }}
            </div>
            <div class="button" @click="handleError">Попробовать снова</div>
        </div>
    </div>
</template>

<script setup>
import { HandleAxiosError } from "@/composables/errors";
const props = defineProps({
    error: Object,
});
const errorData = computed(() => HandleAxiosError(props.error.value));
const emit = defineEmits(["clearError"]);
watch(errorData, (val) => {
    console.log(val);
});
const handleError = () => {
    emit("clearError");
};
</script>
<style lang="scss">
.error {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: $primary-text;

    .error__content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;

        .error__content__title {
            font-size: 50px;
            font-weight: 700;
        }

        .error__content__message {
            font-size: 20px;
            font-weight: 500;
        }

        .button {
            padding: 10px 20px;
            border-radius: 5px;
            background-color: $primary-bg;
            color: $primary-text;
            cursor: pointer;
        }
    }
}</style>
