module.exports = {
    apps: [
        {
            name: "internet-magaz-frontend",
            port: "4008",
            exec_mode: "cluster",
            instances: "max",
            script: "./.output/server/index.mjs",
        },
    ],
};
