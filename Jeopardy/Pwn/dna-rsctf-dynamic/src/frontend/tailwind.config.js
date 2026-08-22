/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            fontFamily: {
                mono: ["monospace"], // Atau 'Share Tech Mono' jika font diload
            },
        },
    },
    plugins: [],
};
