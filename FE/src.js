var resultTxt = "";

function type() {
    const currentText = document.querySelector("#auto-type").textContent;

    if (currentText.length < resultTxt.length) {
        document.querySelector("#auto-type").textContent += resultTxt[currentText.length];
        setTimeout(type, 80);
    }
}

async function onSubmit() {
    const currentText = document.querySelector("#auto-type");
    currentText.innerHTML = '';

    let text = String(inputTxt.value);
    let myObject = await fetch(`http://localhost:5000/predict?s=${text}`);
    let response = await myObject.text();

    if (response === 'YES') {
        resultTxt = "Your tweet is about REAL disasters.";
    } else if (response == 'NO') {
        resultTxt = "Your tweet is not about disasters.";
    } else {
        resultTxt = response;
    }
    type();
}

const inputTxt = document.querySelector(".inputTxt")
const submitBtn = document.querySelector(".btnSearch")

submitBtn.addEventListener('click', onSubmit)

inputTxt.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        onSubmit();
        inputTxt.select();
    }
});
