document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Modal functionality
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <div class="modal-body"></div>
        </div>
    `;
    document.body.appendChild(modal);

    const showModal = (title, content) => {
        modal.querySelector('.modal-body').innerHTML = `<h2>${title}</h2><p>${content}</p>`;
        modal.classList.add('show');
        modal.classList.remove('hide');
    };

    const closeModal = () => {
        modal.classList.add('hide');
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 500); // Hide after animation
    };

    modal.querySelector('.close').addEventListener('click', closeModal);

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Button functionality
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const buttonText = button.innerText;
            
            if (buttonText.includes('Ko\'proq ma\'lumot') || buttonText.includes('Подробнее')) {
                const parentElement = button.closest('.featured-item');
                const shortInfo = parentElement.querySelector('.short-info');
                const fullInfo = parentElement.querySelector('.full-info');
                
                // Toggle visibility of additional information
                if (fullInfo.style.display === 'none') {
                    fullInfo.style.display = 'block';
                    shortInfo.style.display = 'none';
                    button.innerText = 'Yashirish'; // Change button text to 'Hide' or similar
                } else {
                    fullInfo.style.display = 'none';
                    shortInfo.style.display = 'block';
                    button.innerText = 'Ko\'proq ma\'lumot'; // Change button text back to 'More info'
                }
            } else if (buttonText.includes('Batafsil o\'qing') || buttonText.includes('Читать далее')) {
                // Show modal with more information
                const parentElement = button.closest('.news-item, .database-item');
                const title = parentElement.querySelector('h3').innerText;
                const content = parentElement.querySelector('p').innerText;
                showModal(title, content);
            }
        });
    });
});
