const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const http = require("http");

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url ?? "/", `http://${req.headers.host}`);
    const target = url.searchParams.get("param");
    if (!target) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      return res.end("Missing ?param= in query string");
    }
    const response = await fetch(target);
    const body = await response.text();
    const window = new JSDOM("").window;
    const DOMPurify = createDOMPurify(window);
    const clean = DOMPurify.sanitize(body);
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/html");
    res.end(clean);
  } catch (err) {
    console.error(err);
    res.writeHead(500, { "Content-Type": "text/plain" });
    res.end("Server error");
  }
});

const PORT = process.env.PORT || 1337;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
