   const products = [
        {
            id: 1,
            name: 'Болт з шестиграною головкою, оцинкований',
            image: '/static/images/bolt.jpg',
            category: 'bolts'
        },
        {
            id: 2,
            name: 'Гайка DIN934',
            image: '/static/images/6_0004.jpeg',
            category: 'nuts'
        },
        {
            id: 3,
            name: 'Саморіз з напівкруглою головкою',
            image: '/static/images/саморізjpg.jpg',
            category: 'screws'
        },
        {
            id: 4,
            name: 'Шайба',
            image: '/static/images/шайба.jpg',
            category: 'washers'
        },
        {
            id: 5,
            name: 'Шпилька DIN976',
            image: '/static/images/шпилька976.jpg',
            category: 'bolts'
        },
        {
            id: 6,
            name: 'Болт з грибною головкою, оцинкований',
            image: '/static/images/болт_гриб_гол.jpg',
            category: 'nuts'
        },
        {
            id: 7,
            name: 'Шуруп універсальний',
            image: '/static/images/шуруп_універсальнйи.jpg',
            category: 'screws'
        },
        {
            id: 8,
            name: 'Саморіз для ГК',
            image: '/static/images/саморіз_гк.jpg',
            category: 'washers'
        }
    ];

    function renderProducts(productsList) {
        const container = document.querySelector('#productsGrid');
        if (!container) return;

        container.innerHTML = '';

        productsList.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';

            let imageContent;

            if (
                product.image &&
                (
                    product.image.startsWith('/') ||
                    product.image.startsWith('http') ||
                    product.image.startsWith('data:')
                )
            ) {
                imageContent = `
                    <img
                        src="${product.image}"
                        alt="${product.name}"
                        onerror="this.src='/static/img/placeholder.png'; this.onerror=null;"
                    >
                `;
            } else {
                imageContent = product.image;
            }

            card.innerHTML = `
                <div class="product-image">
                    ${imageContent}
                </div>
                <div class="product-info">
                    <h3 class="product-name font-semibold text-xl mb-1">
                        ${product.name}
                    </h3>
                    <div>
                        <a href="product.html?id=${product.id}" class="buy-btn">
                            Купити
                        </a>
                    </div>
                </div>
            `;

            container.appendChild(card);
        });
    }

    function toggleMobileMenu() {
        const nav = document.getElementById('nav');
        if (!nav) return;

        nav.classList.toggle('hidden');
        nav.classList.toggle('mobile-open');
    }

    document.addEventListener('DOMContentLoaded', () => {
        renderProducts(products);
    });