<template>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <AppHeader />
            <div class="app-content">
                <slot />
            </div>
        </div>
        <template #error="{ error }">
            <AppError :error="error" @clearError="fixIssue(error)" />
        </template>
    </NuxtErrorBoundary>
</template>
<style lang="scss">
.default-layout {
    max-width: 1500px;
    margin-inline: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;

    .app-content {
        padding: 10px;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
}
</style>
<script setup>
const handleError = (error) => {
    console.error(error);
};
const fixIssue = (error) => {
    error.value = null;
};
</script>
