document.querySelectorAll('.category-colorbox').forEach(function(box) {
    var color = box.getAttribute('data-color');
    if (color) {
        box.style.backgroundColor = color;
    }
});

document.querySelectorAll('.expand-list-icon').forEach((icon) => {
    icon.addEventListener('onclick', () => {
        icon.parentElement.parentElement.querySelector('.category-desctiption-container').style.display = 'none'
    })

})