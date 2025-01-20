const searchField = document.querySelector('#searchField');

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0) {
        fetch('/search-expenses',{
            body: JSON.stringify({ searchText: searchValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.length === 0)
        });
    }
})