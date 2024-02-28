import { defineConfig, loadEnv } from "vite";
import common from "./vite.config.base.js";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
    const env = loadEnv(mode, process.cwd(), "");

    // const plugins = [];
    // common.plugins.push(plugins);

    return {
        ...common,
        base: env.VITE_BASE_URL,
        build: {
            sourcemap: true,
            target: "esnext", //browsers can handle the latest ES features
            minify: "esbuild",
            outDir: "../dist",
            assetsDir: "static",
        },
        esbuild: {
            treeShaking: true,
            minifyWhitespace: true,
            minifyIdentifiers: true,
            minifySyntax: true,
        },
    };
});