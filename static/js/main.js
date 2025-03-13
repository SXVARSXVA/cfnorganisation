// Show selected section and hide others
function showSection(sectionClass) {
    const sections = document.querySelectorAll('.container');
    sections.forEach(section => {
        section.style.display = 'none';
        section.style.opacity = '0';
        section.classList.remove('active');
    });

    const selectedSection = document.querySelector('.' + sectionClass);
    if (selectedSection) {
        selectedSection.style.display = 'block';
        selectedSection.classList.add('active');
        // Trigger reflow to ensure transition works
        selectedSection.offsetHeight;
        selectedSection.style.opacity = '1';
    }
}

// Toggle event details
function toggleEvent(eventId) {
    const eventSection = document.getElementById(eventId);
    if (eventSection) {
        if (eventSection.style.display === 'block') {
            eventSection.style.opacity = '0';
            setTimeout(() => {
                eventSection.style.display = 'none';
            }, 300);
        } else {
            eventSection.style.display = 'block';
            // Trigger reflow
            eventSection.offsetHeight;
            eventSection.style.opacity = '1';
        }
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Show about section by default
    showSection('about-container');
    
    // Add loading="lazy" to images for better performance
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }
    });
    
    // Add smooth scrolling to internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
