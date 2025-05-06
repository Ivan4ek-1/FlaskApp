
document.querySelectorAll("nobr>a>img").forEach((el)=> {
    el.addEventListener("click", (e) => {
        //e.preventDefault()

        let xhr = new XMLHttpRequest();

        xhr.open('POST', '/test/rate');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send( JSON.stringify({"rating": e.target.dataset.number, "id": e.target.dataset.dishId}));
    })
})