const form = document.getElementById("form");
const inputFile = document.getElementById("file");

const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData();

    for (const file of inputFile.files) {
        formData.append("files", file);
    }

    fetch("http://localhost:8000/files/", {
        method: "post",
        body: formData,
    }).catch((error) => ("Something went wrong!", error));
};

form.addEventListener("submit", handleSubmit);