/**
 * AI-Powered Shop Scale Application
 * Frontend JavaScript Application
 */

// Configuration
const API_URL = 'http://localhost:5000/api';

// Global state
let cameraStream = null;
let currentResult = null;
let shoppingCart = [];
let allProducts = [];

// DOM Elements
const elements = {
    camera: document.getElementById('camera'),
    canvas: document.getElementById('canvas'),
    startCameraBtn: document.getElementById('start-camera-btn'),
    captureBtn: document.getElementById('capture-btn'),
    retakeBtn: document.getElementById('retake-btn'),
    fileUpload: document.getElementById('file-upload'),
    cameraStatus: document.getElementById('camera-status'),
    previewImage: document.getElementById('preview-image'),
    capturedImage: document.getElementById('captured-image'),
    loading: document.getElementById('loading'),
    results: document.getElementById('results'),
    productName: document.getElementById('product-name'),
    productEnglish: document.getElementById('product-english'),
    confidenceValue: document.getElementById('confidence-value'),
    confidenceProgress: document.getElementById('confidence-progress'),
    alternativesList: document.getElementById('alternatives-list'),
    weightGrams: document.getElementById('weight-grams'),
    weightKg: document.getElementById('weight-kg'),
    weightNote: document.getElementById('weight-note'),
    pricePerKg: document.getElementById('price-per-kg'),
    totalPrice: document.getElementById('total-price'),
    addToCartBtn: document.getElementById('add-to-cart-btn'),
    manualCorrectBtn: document.getElementById('manual-correct-btn'),
    manualDialog: document.getElementById('manual-dialog'),
    productSelect: document.getElementById('product-select'),
    confirmManualBtn: document.getElementById('confirm-manual-btn'),
    cancelManualBtn: document.getElementById('cancel-manual-btn'),
    cartItems: document.getElementById('cart-items'),
    cartCount: document.getElementById('cart-count'),
    cartTotal: document.getElementById('cart-total'),
    checkoutBtn: document.getElementById('checkout-btn'),
    clearCartBtn: document.getElementById('clear-cart-btn'),
    toast: document.getElementById('toast')
};

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadProducts();
    checkBackendStatus();
});

// Initialize event listeners
function initializeEventListeners() {
    elements.startCameraBtn.addEventListener('click', startCamera);
    elements.captureBtn.addEventListener('click', captureImage);
    elements.retakeBtn.addEventListener('click', retakePhoto);
    elements.fileUpload.addEventListener('change', handleFileUpload);
    elements.addToCartBtn.addEventListener('click', addToCart);
    elements.manualCorrectBtn.addEventListener('click', showManualDialog);
    elements.confirmManualBtn.addEventListener('click', confirmManualSelection);
    elements.cancelManualBtn.addEventListener('click', hideManualDialog);
    elements.checkoutBtn.addEventListener('click', checkout);
    elements.clearCartBtn.addEventListener('click', clearCart);
}

// Check if backend is running
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_URL.replace('/api', '')}/`);
        const data = await response.json();
        if (data.status === 'running') {
            showToast('Backend połączony pomyślnie', 'success');
        }
    } catch (error) {
        showToast('Nie można połączyć z backend. Upewnij się, że serwer działa.', 'error');
        console.error('Backend connection error:', error);
    }
}

// Load all products for manual selection
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/products`);
        const data = await response.json();
        allProducts = data.products;

        // Populate product select dropdown
        elements.productSelect.innerHTML = '<option value="">Wybierz produkt...</option>';
        allProducts.forEach(product => {
            const option = document.createElement('option');
            option.value = product.name;
            option.textContent = `${product.name_polish} (${product.name})`;
            elements.productSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('Błąd ładowania produktów', 'error');
    }
}

// Start camera
async function startCamera() {
    try {
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment', // Use back camera on mobile
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });

        elements.camera.srcObject = cameraStream;
        elements.camera.style.display = 'block';
        elements.previewImage.style.display = 'none';

        // Update UI
        elements.startCameraBtn.style.display = 'none';
        elements.captureBtn.style.display = 'block';
        elements.retakeBtn.style.display = 'none';

        showStatus('Kamera włączona. Umieść produkt przed kamerą i naciśnij "Skanuj produkt".', 'success');

    } catch (error) {
        console.error('Camera error:', error);
        showStatus('Błąd dostępu do kamery. Sprawdź uprawnienia.', 'error');
        showToast('Nie można uruchomić kamery', 'error');
    }
}

// Capture image from camera
function captureImage() {
    if (!cameraStream) {
        showToast('Kamera nie jest włączona', 'error');
        return;
    }

    // Set canvas size to match video
    elements.canvas.width = elements.camera.videoWidth;
    elements.canvas.height = elements.camera.videoHeight;

    // Draw video frame to canvas
    const context = elements.canvas.getContext('2d');
    context.drawImage(elements.camera, 0, 0);

    // Convert canvas to blob
    elements.canvas.toBlob(async (blob) => {
        // Display captured image
        const imageUrl = URL.createObjectURL(blob);
        elements.capturedImage.src = imageUrl;
        elements.camera.style.display = 'none';
        elements.previewImage.style.display = 'block';

        // Update UI
        elements.captureBtn.style.display = 'none';
        elements.retakeBtn.style.display = 'block';

        // Stop camera stream to save resources
        stopCamera();

        // Send image to backend for classification
        await classifyImage(blob);

    }, 'image/jpeg', 0.95);
}

// Retake photo
function retakePhoto() {
    elements.results.style.display = 'none';
    currentResult = null;
    startCamera();
}

// Stop camera stream
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
}

// Classify image using backend API
async function classifyImage(imageBlob) {
    try {
        // Show loading state
        elements.loading.style.display = 'flex';
        elements.results.style.display = 'none';
        showStatus('Analizowanie obrazu...', 'info');

        // Convert blob to base64
        const reader = new FileReader();
        reader.readAsDataURL(imageBlob);

        reader.onloadend = async () => {
            const base64Image = reader.result;

            // Send to backend
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: base64Image })
            });

            if (!response.ok) {
                throw new Error('Classification failed');
            }

            const data = await response.json();

            // Hide loading, show results
            elements.loading.style.display = 'none';
            displayResults(data);
        };

    } catch (error) {
        console.error('Classification error:', error);
        elements.loading.style.display = 'none';
        showStatus('Błąd podczas rozpoznawania. Spróbuj ponownie.', 'error');
        showToast('Błąd rozpoznawania obrazu', 'error');
    }
}

// Display classification results
function displayResults(data) {
    currentResult = data;

    // Product information
    const classification = data.classification;
    elements.productName.textContent = data.price.product_name_polish;
    elements.productEnglish.textContent = classification.product;

    // Confidence
    const confidence = classification.confidence;
    elements.confidenceValue.textContent = `${confidence.toFixed(1)}%`;
    elements.confidenceProgress.style.width = `${confidence}%`;

    // Display alternative predictions (Top 5)
    if (classification.alternatives && classification.alternatives.length > 0) {
        const allPredictions = [
            { label: classification.product, confidence: classification.confidence },
            ...classification.alternatives
        ];

        elements.alternativesList.innerHTML = allPredictions.map((pred, index) => `
            <div class="alternative-item top-${index + 1}" onclick="selectAlternative('${pred.label}')">
                <span class="alternative-name">${index + 1}. ${pred.label}</span>
                <span class="alternative-confidence">${pred.confidence.toFixed(1)}%</span>
            </div>
        `).join('');
    }

    // Weight
    const weight = data.weight;
    elements.weightGrams.textContent = weight.weight_grams.toFixed(1);
    elements.weightKg.textContent = weight.weight_kg.toFixed(3);
    elements.weightNote.textContent = weight.note || '';

    // Price
    const price = data.price;
    elements.pricePerKg.textContent = price.price_per_kg.toFixed(2);
    elements.totalPrice.textContent = price.total_price.toFixed(2);

    // Show results
    elements.results.style.display = 'block';
    showStatus('Rozpoznawanie zakończone!', 'success');
}

// Add item to shopping cart
function addToCart() {
    if (!currentResult) {
        showToast('Brak produktu do dodania', 'error');
        return;
    }

    const item = {
        id: Date.now(),
        name: currentResult.price.product_name_polish,
        nameEnglish: currentResult.classification.product,
        weight: currentResult.weight.weight_grams,
        weightKg: currentResult.weight.weight_kg,
        pricePerKg: currentResult.price.price_per_kg,
        totalPrice: currentResult.price.total_price,
        confidence: currentResult.classification.confidence
    };

    shoppingCart.push(item);
    updateCartDisplay();
    showToast(`Dodano ${item.name} do koszyka`, 'success');

    // Record transaction
    recordTransaction(item);
}

// Update shopping cart display
function updateCartDisplay() {
    if (shoppingCart.length === 0) {
        elements.cartItems.innerHTML = '<p class="empty-cart">Koszyk jest pusty</p>';
        elements.cartCount.textContent = '0';
        elements.cartTotal.textContent = '0.00 PLN';
        elements.checkoutBtn.disabled = true;
        elements.clearCartBtn.style.display = 'none';
        return;
    }

    // Calculate total
    const total = shoppingCart.reduce((sum, item) => sum + item.totalPrice, 0);

    // Update count and total
    elements.cartCount.textContent = shoppingCart.length;
    elements.cartTotal.textContent = `${total.toFixed(2)} PLN`;
    elements.checkoutBtn.disabled = false;
    elements.clearCartBtn.style.display = 'block';

    // Render cart items
    elements.cartItems.innerHTML = shoppingCart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-details">
                    ${item.weightKg.toFixed(3)} kg × ${item.pricePerKg.toFixed(2)} PLN/kg
                </div>
            </div>
            <div class="cart-item-price">${item.totalPrice.toFixed(2)} PLN</div>
            <button class="cart-item-remove" onclick="removeFromCart(${index})">×</button>
        </div>
    `).join('');
}

// Remove item from cart
function removeFromCart(index) {
    const item = shoppingCart[index];
    shoppingCart.splice(index, 1);
    updateCartDisplay();
    showToast(`Usunięto ${item.name}`, 'info');
}

// Clear entire cart
function clearCart() {
    if (confirm('Czy na pewno chcesz wyczyścić cały koszyk?')) {
        shoppingCart = [];
        updateCartDisplay();
        showToast('Koszyk został wyczyszczony', 'info');
    }
}

// Checkout
function checkout() {
    if (shoppingCart.length === 0) {
        showToast('Koszyk jest pusty', 'error');
        return;
    }

    const total = shoppingCart.reduce((sum, item) => sum + item.totalPrice, 0);
    const itemCount = shoppingCart.length;

    alert(`🎉 Dziękujemy za zakupy!\n\nProdukty: ${itemCount}\nRazem: ${total.toFixed(2)} PLN\n\n(To jest demo - rzeczywista płatność nie została przetworzona)`);

    // Clear cart after checkout
    shoppingCart = [];
    updateCartDisplay();
}

// Show manual correction dialog
function showManualDialog() {
    elements.manualDialog.style.display = 'flex';
}

// Hide manual correction dialog
function hideManualDialog() {
    elements.manualDialog.style.display = 'none';
}

// Confirm manual product selection
async function confirmManualSelection() {
    const selectedProduct = elements.productSelect.value;

    if (!selectedProduct) {
        showToast('Wybierz produkt z listy', 'error');
        return;
    }

    try {
        // Get weight estimate for selected product
        const estimatorResponse = await fetch(`${API_URL}/product/${selectedProduct}`);
        const productData = await estimatorResponse.json();

        // Estimate weight using current result or default
        const weightGrams = currentResult?.weight?.weight_grams || 150;

        // Calculate price
        const priceResponse = await fetch(`${API_URL}/calculate_price`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_name: selectedProduct,
                weight_grams: weightGrams
            })
        });

        const priceData = await priceResponse.json();

        // Update current result
        currentResult = {
            classification: {
                product: selectedProduct,
                confidence: 100 // Manual selection = 100% confidence
            },
            weight: {
                weight_grams: weightGrams,
                weight_kg: weightGrams / 1000,
                note: 'Ręcznie poprawione'
            },
            price: priceData
        };

        // Display updated results
        displayResults(currentResult);
        hideManualDialog();
        showToast('Produkt zaktualizowany', 'success');

    } catch (error) {
        console.error('Manual selection error:', error);
        showToast('Błąd aktualizacji produktu', 'error');
    }
}

// Record transaction to database
async function recordTransaction(item) {
    try {
        await fetch(`${API_URL}/transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_name: item.nameEnglish,
                weight_g: item.weight,
                price_per_kg: item.pricePerKg,
                total_price: item.totalPrice,
                confidence: item.confidence
            })
        });
    } catch (error) {
        console.error('Transaction recording error:', error);
    }
}

// Show status message
function showStatus(message, type = 'info') {
    elements.cameraStatus.textContent = message;
    elements.cameraStatus.className = `status-message ${type}`;
    elements.cameraStatus.style.background = type === 'success' ? '#d4edda' :
        type === 'error' ? '#f8d7da' : '#d1ecf1';
    elements.cameraStatus.style.color = type === 'success' ? '#155724' :
        type === 'error' ? '#721c24' : '#0c5460';
}

// Show toast notification
function showToast(message, type = 'success') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type} show`;

    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showToast('Proszę wybrać plik obrazu', 'error');
        return;
    }

    // Display uploaded image
    const imageUrl = URL.createObjectURL(file);
    elements.capturedImage.src = imageUrl;
    elements.camera.style.display = 'none';
    elements.previewImage.style.display = 'block';

    // Update UI
    elements.startCameraBtn.style.display = 'none';
    elements.captureBtn.style.display = 'none';
    elements.retakeBtn.style.display = 'block';

    // Stop camera if running
    stopCamera();

    // Classify the uploaded image
    await classifyImage(file);
}

// Select alternative prediction
async function selectAlternative(productName) {
    try {
        showStatus('Aktualizowanie wyboru...', 'info');

        // Get weight estimate for selected product
        const weightGrams = currentResult?.weight?.weight_grams || 150;

        // Calculate price
        const priceResponse = await fetch(`${API_URL}/calculate_price`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_name: productName,
                weight_grams: weightGrams
            })
        });

        const priceData = await priceResponse.json();

        // Estimate weight
        const estimatorResponse = await fetch(`${API_URL}/product/${productName}`);
        const productData = await estimatorResponse.json();

        // Update current result
        currentResult = {
            classification: {
                product: productName,
                confidence: 100,
                alternatives: currentResult.classification.alternatives
            },
            weight: {
                weight_grams: weightGrams,
                weight_kg: weightGrams / 1000,
                note: 'Wybrano ręcznie z listy'
            },
            price: priceData
        };

        // Update display
        elements.productName.textContent = priceData.product_name_polish;
        elements.productEnglish.textContent = productName;
        elements.confidenceValue.textContent = '100.0%';
        elements.confidenceProgress.style.width = '100%';
        elements.pricePerKg.textContent = priceData.price_per_kg.toFixed(2);
        elements.totalPrice.textContent = priceData.total_price.toFixed(2);

        showStatus('Produkt zaktualizowany!', 'success');
        showToast(`Wybrano: ${priceData.product_name_polish}`, 'success');

    } catch (error) {
        console.error('Error selecting alternative:', error);
        showToast('Błąd aktualizacji produktu', 'error');
    }
}

// Make functions globally accessible
window.removeFromCart = removeFromCart;
window.selectAlternative = selectAlternative;
