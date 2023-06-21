<template>
    <el-upload class="avatar-uploader" :show-file-list="false" :before-upload="
        (event) =>
            beforeAvatarUpload
                ? beforeAvatarUpload(event)
                : defaultBeforeUpload(event)
    " v-bind="$attrs" :on-success="defaultOnSuccess">
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <Icon name="material-symbols:drive-folder-upload-outline-rounded" class="avatar-uploader-icon" v-else />
    </el-upload>
</template>
<script setup>
import { ElMessage } from "element-plus";
const emit = defineEmits(["file"]);

const runtimeConfig = useRuntimeConfig();

const {
    imageUrl,
    beforeAvatarUpload,
    handleAvatarSuccess,
    onSuccess,
    maxSizeMB,
    aspectRatio,
    borderRadius,
} = defineProps({
    imageUrl: {
        type: String,
        default: "",
    },
    borderRadius: {
        type: String,
        default: "50%",
    },
    aspectRatio: {
        type: Number,
        default: 1,
    },
    beforeAvatarUpload: {
        type: Function,
        default: null,
    },
    onSuccess: {
        type: Function,
    },
    maxSizeMB: {
        type: Number,
        default: null,
    },
});
const defaultOnSuccess = (response, file) => {
    if (onSuccess) {
        onSuccess(response, file);
        return;
    }
    emit("file", file.raw);
};
const defaultBeforeUpload = (rawFile) => {
    if (!rawFile) return false;
    if (rawFile.type.split("/")[0] !== "image") {
        ElMessage.error("Это не картинка!");
        return false;
    } else if (
        rawFile.size / 1024 / 1024 >
        (maxSizeMB || runtimeConfig.public.MAX_IMAGE_FILE_SIZE_MB)
    ) {
        ElMessage.error("Картинка слишком большая!");
        return false;
    }
    return true;
};
</script>

<style lang="scss">
.avatar-uploader {
    width: 100%;
    height: 100%;

    .el-upload {
        position: relative;
        border: 2px dashed transparent;
        border-radius: v-bind(borderRadius);
        cursor: pointer;
        overflow: hidden;
        width: 100%;
        aspect-ratio: v-bind(aspectRatio);

        &::after {
            @include flex-center;
            content: "Изменить";
            flex-direction: column;
            position: absolute;
            inset: 0;
            background-color: rgba(0, 0, 0, 0.5);
            color: #fff;
            opacity: 0;
            transition: opacity 0.3s;
            cursor: pointer;
        }

        &:has(svg) {
            border-color: $accent-2;
        }

        &:hover {
            border-color: $accent-1;

            &::after {
                opacity: 1;
            }
        }

        .avatar-uploader-icon {
            color: #8c939d;
            width: 40px;
            height: 40px;
            text-align: center;
        }

        .avatar {
            width: 100%;
            height: 100%;

            object-fit: cover;
        }
    }
}
</style>