var resultTxt = "";
const inputEle = document.querySelector("#input")
const submitBtn = document.querySelector("#submit")
const tweetLoader = document.querySelector("#tweet-loading");
const tweetEle = document.querySelector("#tweet");
const resultEle = document.querySelector("#result");
const resultLoader = document.querySelector("#result-loading");


function type() {
    const currentText = resultEle.textContent;
    if (currentText.length < resultTxt.length) {
        resultEle.textContent += resultTxt[currentText.length];
        setTimeout(type, 80);
    }
}

async function onSubmit() {
    inputEle.select();
    resultEle.innerHTML = '';
    tweetEle.innerHTML = '';

    let inputTxt = String(inputEle.value);
    tweetLoader.classList.add("display");

    let response = await fetch(`http://127.0.0.1:5000/get?link=${inputTxt}`);

    
    let tweet;
    if (response.ok) {
        tweet = await response.text();
        if (tweet === '<NULL>') {
            tweet = 'Something went wrong with your link. Please try again!'
            tweetEle.style.color = '#d00000';
            tweetLoader.classList.remove("display");
            tweetEle.innerHTML = tweet;
            return;
        } else {
            tweetEle.style.color = '#c0c0c0';
            tweetLoader.classList.remove("display");
            tweetEle.innerHTML = tweet;
        }
    } else {
        tweet = 'Can not get tweet. Please try again!';
        tweetEle.style.color = '#d00000';
        tweetLoader.classList.remove("display");
        tweetEle.innerHTML = tweet;
        return
    }
    
    resultLoader.classList.add("display");
    response = await fetch(`http://127.0.0.1:5000/predict?tweet=${tweet}`);

    let result;
    if (response.ok) {
        result = await response.text();
        resultEle.style.color = '#f5f5f5';
        if (result === 'YES') {
            document.body.classList.add("disasters");
            resultTxt = "Your tweet is about REAL disasters.";
        } else if (result === 'NO') {
            document.body.classList.remove("disasters");
            resultTxt = "Your tweet is not about disasters.";
        } else {
            document.body.classList.remove("disasters");
            resultTxt = "Can not get result!";
        }
        resultLoader.classList.remove("display");
        type();
    } else {
        result = 'Can not get result. Please try again!';
        resultEle.style.color = '#fab6c9';
        resultLoader.classList.remove("display");
        resultEle.innerHTML = result;
    }
}

submitBtn.addEventListener('click', onSubmit)

inputEle.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        onSubmit();
    }
});
