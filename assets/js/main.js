(() => {
  "use strict";

  const isAnalyticsAvailable = () => typeof window.gtag === "function";

  const sendEvent = (name, parameters = {}) => {
    if (!isAnalyticsAvailable()) {
      return;
    }

    window.gtag("event", name, {
      page_path: window.location.pathname,
      page_title: document.title,
      ...parameters,
    });
  };

  const getContentContext = () => {
    const parts = window.location.pathname.split("/").filter(Boolean);

    if (parts.length >= 2 && ["projects", "blog", "notes"].includes(parts[0])) {
      return {
        content_type: parts[0],
        content_slug: parts[1],
      };
    }

    return {};
  };

  const classifyOutboundLink = (url) => {
    const hostname = url.hostname.toLowerCase();

    if (hostname === "github.com" || hostname.endsWith(".github.com")) {
      return "github_click";
    }

    if (hostname === "medium.com" || hostname.endsWith(".medium.com")) {
      return "medium_click";
    }

    if (hostname === "linkedin.com" || hostname.endsWith(".linkedin.com")) {
      return "linkedin_click";
    }

    return "outbound_link_click";
  };

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");

    if (!link) {
      return;
    }

    let url;

    try {
      url = new URL(link.href, window.location.href);
    } catch (_) {
      return;
    }

    const context = getContentContext();
    const protocol = url.protocol.toLowerCase();

    if (protocol === "mailto:") {
      sendEvent("contact_click", {
        contact_method: "email",
        ...context,
      });
      return;
    }

    if (protocol === "tel:") {
      sendEvent("contact_click", {
        contact_method: "phone",
        ...context,
      });
      return;
    }

    const currentHost = window.location.hostname.toLowerCase();
    const targetHost = url.hostname.toLowerCase();

    if (targetHost && targetHost !== currentHost) {
      sendEvent(classifyOutboundLink(url), {
        link_url: url.href,
        link_domain: targetHost,
        link_text: (link.textContent || "").trim().slice(0, 100),
        ...context,
      });
      return;
    }

    const path = url.pathname.toLowerCase();
    if (/\.(pdf|doc|docx|zip)$/i.test(path)) {
      sendEvent("file_download", {
        file_name: path.split("/").pop(),
        link_url: url.href,
        ...context,
      });
    }
  });
})();
