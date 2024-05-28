 
 
    const menuItems = document.querySelectorAll('.sub-menu li');

    // Add click event listeners to each menu item
    menuItems.forEach((menuItem) => {
        menuItem.addEventListener('click', (event) => {
            // Remove 'active' class from all menu items
            menuItems.forEach((item) => {
                item.classList.remove('active');
            });

            // Add 'active' class to the clicked menu item
            event.currentTarget.classList.add('active');
        });
    });
 
