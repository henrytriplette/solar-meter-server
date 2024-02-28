import { defineConfig, loadEnv } from "vite";

import common from "./vite.config.base.js";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
    const env = loadEnv(mode, process.cwd(), "");

    //   const plugins = [basicSsl()];
    //   common.plugins.push(plugins);

    return {
        ...common,
        base: env.VITE_BASE_URL,
        server: {},
        build: {
            sourcemap: true,
            target: "esnext", //browsers can handle the latest ES features
        },
    };
});