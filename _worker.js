// Serves the Markdown copy of a page to agents that ask for it
// (Accept: text/markdown). Everything else is the static site as is.
// Cloudflare's own Markdown for Agents needs a Pro plan; this zone is Free.

const CONTENT_SIGNAL = "search=yes, ai-input=yes, ai-train=yes";

function markdownPath(pathname) {
  if (pathname === "/" || pathname === "/index.html") return "/index.md";
  if (/\.[a-z0-9]+$/i.test(pathname) && !pathname.endsWith(".html")) return null;
  return pathname.replace(/\.html$/, "").replace(/\/$/, "") + ".md";
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const accept = request.headers.get("Accept") || "";
    const mdPath = markdownPath(url.pathname);

    if (mdPath && accept.includes("text/markdown") && (request.method === "GET" || request.method === "HEAD")) {
      const md = await env.ASSETS.fetch(new URL(mdPath, url));
      if (md.ok && !(md.headers.get("Content-Type") || "").includes("text/html")) {
        const headers = new Headers(md.headers);
        headers.set("Content-Type", "text/markdown; charset=utf-8");
        headers.set("Content-Signal", CONTENT_SIGNAL);
        headers.set("Vary", "Accept");
        return new Response(request.method === "HEAD" ? null : md.body, { status: 200, headers });
      }
    }

    const response = await env.ASSETS.fetch(request);
    if (!mdPath || !response.ok || !(response.headers.get("Content-Type") || "").includes("text/html")) return response;

    const headers = new Headers(response.headers);
    headers.set("Vary", "Accept");
    headers.set("Content-Signal", CONTENT_SIGNAL);
    headers.set("Link", `<${mdPath}>; rel="alternate"; type="text/markdown", </llms.txt>; rel="describedby"; type="text/plain"`);
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  },
};
