class RecommendationApp {
    constructor() {
        this.products = [];
        this.selectedProduct = null;
        this.init();
    }
    
    async init() {
        await this.loadProducts();
        this.setupEventListeners();
    }
    
    async loadProducts() {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.products = data.products;
                this.renderProducts();
            } else {
                this.showError('Failed to load products');
            }
        } catch (error) {
            this.showError('Error loading products: ' + error.message);
        }
    }
    
    renderProducts() {
        const productsGrid = document.getElementById('products-grid');
        productsGrid.innerHTML = '';
        
        this.products.forEach(product => {
            const productCard = this.createProductCard(product);
            productsGrid.appendChild(productCard);
        });
    }
    
    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.dataset.productId = product.id;
        card.dataset.category = product.category;
        
        const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
        
        card.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-category">${product.category}</div>
            <div class="product-price">$${product.price}</div>
            <div class="product-description">${product.description}</div>
            <div class="product-rating">
                <span class="rating-stars">${stars}</span>
                <span>(${product.rating})</span>
            </div>
        `;
        
        card.addEventListener('click', () => this.handleProductClick(product));
        
        return card;
    }
    
    async handleProductClick(product) {
        // Visual feedback
        document.querySelectorAll('.product-card').forEach(card => {
            card.classList.remove('clicked');
        });
        document.querySelector(`[data-product-id="${product.id}"]`).classList.add('clicked');
        
        this.selectedProduct = product;
        
        // Track click event
        await this.trackClick(product.id, product.category);
        
        // Get and display recommendations
        await this.loadRecommendations(product.id);
    }
    
    async trackClick(productId, category) {
        try {
            const response = await fetch('/api/track-click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: productId,
                    category: category
                })
            });
            
            const data = await response.json();
            if (data.status !== 'success') {
                console.warn('Failed to track click:', data.message);
            }
        } catch (error) {
            console.error('Error tracking click:', error);
        }
    }
    
    async loadRecommendations(productId) {
        const recommendationsSection = document.getElementById('recommendations-section');
        const recommendationsGrid = document.getElementById('recommendations-grid');
        
        // Show loading state
        recommendationsSection.style.display = 'block';
        recommendationsGrid.innerHTML = '<div class="loading">Loading recommendations...</div>';
        
        try {
            const response = await fetch(`/api/recommendations?product_id=${productId}&limit=6`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.renderRecommendations(data.recommendations);
            } else {
                this.showError('Failed to load recommendations');
            }
        } catch (error) {
            this.showError('Error loading recommendations: ' + error.message);
        }
    }
    
    renderRecommendations(recommendations) {
        const recommendationsGrid = document.getElementById('recommendations-grid');
        recommendationsGrid.innerHTML = '';
        
        if (recommendations.length === 0) {
            recommendationsGrid.innerHTML = '<div class="error">No recommendations found</div>';
            return;
        }
        
        recommendations.forEach(rec => {
            const recCard = this.createRecommendationCard(rec);
            recommendationsGrid.appendChild(recCard);
        });
    }
    
    createRecommendationCard(recommendation) {
        const product = recommendation.product;
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        
        const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
        
        card.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-category">${product.category}</div>
            <div class="product-price">$${product.price}</div>
            <div class="product-description">${product.description}</div>
            <div class="product-rating">
                <span class="rating-stars">${stars}</span>
                <span>(${product.rating})</span>
            </div>
            <div class="recommendation-reason">${recommendation.reason}</div>
        `;
        
        card.addEventListener('click', () => this.handleProductClick(product));
        
        return card;
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(errorDiv, container.firstChild);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    setupEventListeners() {
        // Add any additional event listeners here
        window.addEventListener('beforeunload', () => {
            // Cleanup if needed
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RecommendationApp();
});