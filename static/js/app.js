(() => {
  "use strict";
  const body = document.body;
  const themeToggle = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");
  const urlInput = document.getElementById("url");
  const pasteButton = document.getElementById("pasteButton");
  const form = document.getElementById("downloadForm");
  const button = document.getElementById("downloadButton");
  const buttonText = document.getElementById("downloadButtonText");
  const buttonIcon = document.getElementById("downloadIcon");
  const status = document.getElementById("status");
  const sun =
    '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>';
  const moon =
    '<path d="M20.5 14.7A8.5 8.5 0 0 1 9.3 3.5 8.5 8.5 0 1 0 20.5 14.7Z"/>';
  const down = '<path d="M12 3.5v15m0 0 6-6m-6 6-6-6"/>';
  const spinner = '<path d="M12 3a9 9 0 1 0 9 9"/>';
  function setStatus(message, kind = "") {
    status.textContent = message;
    status.dataset.kind = kind;
  }
  function setTheme(light) {
    body.dataset.theme = light ? "light" : "dark";
    themeIcon.innerHTML = light ? moon : sun;
    themeToggle.setAttribute(
      "aria-label",
      light ? "Ativar tema escuro" : "Ativar tema claro",
    );
    try {
      localStorage.setItem("black-glass-theme", light ? "light" : "dark");
    } catch (_) {}
  }
  let savedTheme = "dark";
  try {
    savedTheme = localStorage.getItem("black-glass-theme") || "dark";
  } catch (_) {}
  setTheme(savedTheme === "light");
  themeToggle.addEventListener("click", () =>
    setTheme(body.dataset.theme !== "light"),
  );
  function normalizeVideoUrl(raw) {
    try {
      const parsed = new URL(raw.trim());
      const hostname = parsed.hostname.toLowerCase().replace(/^www\./, "");
      if (
        !["http:", "https:"].includes(parsed.protocol) ||
        ![
          "youtube.com",
          "m.youtube.com",
          "music.youtube.com",
          "youtu.be",
        ].includes(hostname) ||
        parsed.username ||
        parsed.password ||
        (parsed.port && !["80", "443"].includes(parsed.port))
      )
        return null;
      let videoId = null;
      if (hostname === "youtu.be") {
        videoId = parsed.pathname.replace(/^\/+|\/+$/g, "");
      } else if (parsed.pathname.replace(/\/+$/, "") === "/watch") {
        videoId = parsed.searchParams.get("v");
      } else {
        const match = parsed.pathname.match(
          /^\/(?:shorts|live|embed)\/([A-Za-z0-9_-]{11})\/?$/,
        );
        if (match) videoId = match[1];
      }
      return /^[A-Za-z0-9_-]{11}$/.test(videoId || "")
        ? `https://www.youtube.com/watch?v=${videoId}`
        : null;
    } catch (_) {
      return null;
    }
  }
  function isYoutubeUrl(raw) {
    return normalizeVideoUrl(raw) !== null;
  }
  pasteButton.addEventListener("click", async () => {
    if (!navigator.clipboard?.readText) {
      setStatus("Cole o link no campo usando Ctrl+V.", "error");
      urlInput.focus();
      return;
    }
    try {
      const clipboardText = (await navigator.clipboard.readText()).trim();
      if (!clipboardText) {
        setStatus("A área de transferência está vazia.", "error");
        return;
      }
      const singleVideoUrl = normalizeVideoUrl(clipboardText);
      urlInput.value = singleVideoUrl || clipboardText;
      urlInput.focus();
      setStatus(
        singleVideoUrl
          ? "Link do vídeo pronto. Escolha o formato."
          : "Confira se é um link de vídeo do YouTube.",
        singleVideoUrl ? "" : "error",
      );
    } catch (_) {
      setStatus(
        "Não foi possível acessar a área de transferência. Use Ctrl+V.",
        "error",
      );
      urlInput.focus();
    }
  });
  urlInput.addEventListener("input", () => {
    if (status.dataset.kind === "error") setStatus("");
  });
  urlInput.addEventListener("paste", () => {
    setTimeout(() => {
      const singleVideoUrl = normalizeVideoUrl(urlInput.value);
      if (singleVideoUrl) urlInput.value = singleVideoUrl;
    }, 0);
  });
  urlInput.addEventListener("change", () => {
    const singleVideoUrl = normalizeVideoUrl(urlInput.value);
    if (singleVideoUrl) urlInput.value = singleVideoUrl;
  });
  function getDownloadName(header, format) {
    const fallback = `youtube-download.${format}`;
    if (!header) return fallback;
    const utf = header.match(/filename\*\s*=\s*UTF-8''([^;]+)/i);
    if (utf) {
      try {
        return decodeURIComponent(utf[1].trim().replace(/^"|"$/g, ""));
      } catch (_) {}
    }
    const plain = header.match(/filename\s*=\s*(?:"([^"]+)"|([^;]+))/i);
    return (plain && (plain[1] || plain[2]).trim()) || fallback;
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (button.disabled) return;
    const value = urlInput.value.trim();
    if (!value) {
      setStatus("Cole o link de um vídeo para continuar.", "error");
      urlInput.focus();
      return;
    }
    const singleVideoUrl = normalizeVideoUrl(value);
    if (!singleVideoUrl) {
      setStatus(
        "Informe o link de um vídeo do YouTube (não apenas uma playlist).",
        "error",
      );
      urlInput.focus();
      return;
    }
    urlInput.value = singleVideoUrl;
    if (location.protocol === "file:") {
      setStatus("Prévia do visual: execute o app.py para baixar arquivos.");
      return;
    }
    button.disabled = true;
    button.classList.add("is-loading");
    button.setAttribute("aria-busy", "true");
    buttonText.textContent = "Preparando download...";
    buttonIcon.innerHTML = spinner;
    setStatus(
      "Buscando a melhor qualidade disponível e preparando a capa. Arquivos grandes podem demorar.",
    );
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
      });
      if (!response.ok) {
        const details = (await response.text()).trim();
        throw new Error(
          details || `Erro ${response.status} ao baixar o arquivo.`,
        );
      }
      buttonText.textContent = "Salvando arquivo...";
      setStatus("Download pronto. Salvando no seu dispositivo...");
      const blob = await response.blob();
      const format = new FormData(form).get("format") || "mp4";
      const downloadName = getDownloadName(
        response.headers.get("Content-Disposition"),
        format,
      );
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = downloadName;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
      setStatus("Arquivo enviado para download com sucesso.", "success");
    } catch (error) {
      setStatus(
        error.message || "Não foi possível concluir o download.",
        "error",
      );
    } finally {
      button.disabled = false;
      button.classList.remove("is-loading");
      button.removeAttribute("aria-busy");
      buttonText.textContent = "Baixar arquivo";
      buttonIcon.innerHTML = down;
    }
  });
  if (
    matchMedia("(pointer: fine)").matches &&
    !matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    document.querySelectorAll(".reactive-glass").forEach((element) => {
      let frame = 0;
      element.addEventListener("pointermove", (event) => {
        if (frame) return;
        const x = event.clientX,
          y = event.clientY;
        frame = requestAnimationFrame(() => {
          const rect = element.getBoundingClientRect();
          element.style.setProperty(
            "--px",
            `${((x - rect.left) / rect.width) * 100}%`,
          );
          element.style.setProperty(
            "--py",
            `${((y - rect.top) / rect.height) * 100}%`,
          );
          frame = 0;
        });
      });
      element.addEventListener("pointerleave", () => {
        element.style.setProperty("--px", "50%");
        element.style.setProperty("--py", "0%");
      });
    });
  }
})();
