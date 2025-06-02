function getNetflixTitles() {
    // Select all Netflix title cards
    let titleDivsNetflix = document.querySelectorAll('.title-card');
    let titles = [];
    titleDivsNetflix.forEach(titleDiv => {
        if (
            titleDiv.children[0] &&
            titleDiv.children[0].children[0] &&
            titleDiv.children[0].children[0].ariaLabel
        ) {
            let title = titleDiv.children[0].children[0].ariaLabel;
            titles.push(title);
        }
    });
    return titles;
}

function getNetflixTitlesWithImages() {
    // Select all Netflix title cards
    let titleDivsNetflix = document.querySelectorAll('.title-card');
    let results = [];
    titleDivsNetflix.forEach(titleDiv => {
        let title = null;
        let imageUrl = null;
        if (
            titleDiv.children[0] &&
            titleDiv.children[0].children[0]
        ) {
            let child = titleDiv.children[0].children[0];
            if (child.ariaLabel) {
                title = child.ariaLabel;
            }
            // Try to find an <img> tag inside the card
            let img = child.querySelector('img');
            if (img && img.src) {
                imageUrl = img.src;
            }
        }
        if (title) {
            results.push({ title, imageUrl });
        }
    });
    return results;
}