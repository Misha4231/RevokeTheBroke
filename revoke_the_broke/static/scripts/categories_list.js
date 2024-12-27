document.querySelectorAll('.category-colorbox').forEach(function(box) {
    var color = box.getAttribute('data-color');
    if (color) {
        box.style.backgroundColor = color;
    }
});

document.querySelectorAll('.expand-list-icon').forEach((icon) => {
    var parentDescription = icon.parentElement.parentElement.querySelector('.category-desctiption-container');
    parentDescription.style.display = 'none'
    icon.addEventListener('click', () => {
        
        
        if (parentDescription.style.display === 'none') {
            parentDescription.style.display = 'block';
            
            var openIconSrc = icon.querySelector('img').dataset.open;
            icon.querySelector('img').setAttribute('src', openIconSrc);
        } else {
            parentDescription.style.display = 'none';
            var closeIconSrc = icon.querySelector('img').dataset.close;
            icon.querySelector('img').setAttribute('src', closeIconSrc);
           
        }
    });
});
