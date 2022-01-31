const form = document.querySelector("#form");

const downloadFile = (url, fileName) => {
  const a = document.createElement("a");
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
  a.click();
  a.remove(); //afterwards we remove the element again
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const formData = new FormData(e.target);
    const data = new URLSearchParams(formData);
    const count = data.get("count");
    const book = data.get("book");
    const chap_start = data.get("chap_start").trim();
    const chap_end = data.get("chap_end").trim();
    console.log(chap_start || chap_end);
    if (chap_start && !chap_end) {
      throw new Error("Either both or no chapters need to be completed");
    }
    if (!chap_start && chap_end) {
      throw new Error("Either both or no chapters need to be completed");
    }
    const resp = await fetch("/flashcards", {
      method: "POST",
      headers: new Headers({ "Content-Type": "application/json" }),
      body: JSON.stringify({ count, book, chap_start, chap_end }),
    });
    const blob = await resp.blob();
    const fileName = resp.headers
      .get("content-disposition")
      .split("filename=")[1]
      .split(";")[0];
    const url = window.URL.createObjectURL(new File([blob], fileName));
    downloadFile(url, fileName);
  } catch (error) {
    const mssg = error.message || "Looks like there was an error!";
    alert(mssg);
  }
});
