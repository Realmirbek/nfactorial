// Блокируем все отправки форм по умолчанию
document.addEventListener("submit", (e) => {
  e.preventDefault();
}, true);

// Ждём, пока DOM готов, чтобы найти нужную форму
window.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  const clone = form.cloneNode(true);
  form.replaceWith(clone);

  clone.addEventListener("submit", async (e) => {
    const formData = new FormData(e.target);
    const phone = formData.get("number").replace(/\D/g, "");
    const formattedPhone = phone.startsWith("8") ? "+7" + phone.slice(1) : "+" + phone;

    const data = new URLSearchParams();
    data.append("name", formData.get("name"));
    data.append("phone", formattedPhone);

    await fetch("/send-contact", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: data
    });

    window.location.href = "/?success=true";
  });
});


