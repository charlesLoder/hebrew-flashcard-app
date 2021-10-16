const form = document.querySelector("#form");

const downloadFile = (url) => {
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
    const resp = await fetch("/flashcards", {
      method: "POST",
      headers: new Headers({ "Content-Type": "application/json" }),
      body: JSON.stringify({ count, book }),
    });
    const fileName =
      resp.headers
        .get("content-disposition")
        .split("filename=")[1]
        .split(";")[0] || "defaul-name.csv";
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(new File([blob], fileName));
    downloadFile(url);
  } catch (error) {
    const mssg = error.message || "Looks like there was an error!";
    alert(mssg);
  }
});
