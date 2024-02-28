import path from "path";
import vue from "@vitejs/plugin-vue";

const root = path.resolve(__dirname, "..");

export default {
    resolve: {
        extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
        alias: {
            "@": path.resolve(root, "./src"),
        },
    },
    optimizeDeps: {
        include: [],
    },
    plugins: [vue()],
};