// Smooth Scroll on Navbar Click
document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});


function showModal(id) {
    document.getElementById(id).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showList(type) {
    const modal = document.getElementById('list-modal');
    const title = document.getElementById('list-title');
    const content = document.getElementById('list-content');

    if (type === 'school') {
        title.textContent = 'Schools Specializing in Autism Education';
        content.innerHTML = `
            <li><strong>Asha Kiran Special Needs School</strong><br>Address: No 10-26, Esther Gardens, Sir M V Nagar, Jayanti Nagar, Horamavu, Bengaluru, Karnataka 560016<br>Contact: 073494 52237</li>
            <li><strong>ASHA Academy for Severe Handicaps and Autism</strong><br>Address:  L 76/A, 3rd Main Rd, 4th Block, HBCS, 3rd Stage, Basaveshwar Nagar, Bengaluru, Karnataka 560079<br>Contact: 080 2322 5279</li>
            <li><strong>Asha Hai</strong><br>Address: D1/1, Block H, Hauz Khas, New Delhi, Delhi 110016<br>Contact:  098106 94640</li>
            <li><strong>Indian Mother and Child Care (Autism, ADHD, MR, Special Boarding School for Boys)</strong><br>Address: R-8/1 Sreenagar West, Srinagar, Panchpota, Pearabagan, Kamalgachhi More, West Bengal 700094<br>Contact:  098308 88888</li>
            <li><strong>Pavani Autism Special Schools</strong><br>Address: 1-6-39/60,Road No20,Dinakar Nagar, West Venkatapuram, Alwal, Secunderabad, Telangana 500015<br>Contact: 099853 81174</li>`;
    } else if (type === 'doctor') {
        title.textContent = 'Doctors and Organizations for Autism';
        content.innerHTML = `
            <li><strong>Dr. Kulbhushan Singh Dagar</strong><br>
                <em>Principal Director, Chief Surgeon & Head - Neonatal & Congenital Heart Surgery, Paediatrics (Ped), Paediatric Cardiac Surgery</em><br>
                Experience: 31+ Years | Gender: Male</li>
    
            <li><strong>Dr. Jasjit Singh Bhasin</strong><br>
                <em>Senior Director - Paediatrics (Ped)</em><br>
                Experience: 17+ Years | Gender: Male</li>
    
            <li><strong>Dr. A.J. Chitkara</strong><br>
                <em>Senior Director - Pediatrics - Paediatrics (Ped)</em><br>
                Experience: 46+ Years | Gender: Male</li>
    
            <li><strong>Dr. Babita Jain</strong><br>
                <em>Senior Director & HOD - Paediatrics (Ped)</em><br>
                Experience: 30+ Years | Gender: Female</li>
    
            <li><strong>Dr. Ramalingam Kalyan</strong><br>
                <em>Senior Director & HOD - M.D. Paediatrics - Paediatrics (Ped)</em><br>
                Experience: 28+ Years | Gender: Male</li>
    
            <li><strong>Dr. Shyam Kukreja</strong><br>
                <em>Senior Director & Head Of The Department - Paediatrics (Ped)</em><br>
                Experience: 45+ Years | Gender: Male</li>
        `;
    }

    modal.style.display = 'block';
}

// File Upload Functionality
document.querySelector(".upload-btn")?.addEventListener("click", () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.onchange = () => {
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("file", file);

        fetch("/upload", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert("File uploaded: " + data.file_path);
            } else {
                alert("Upload failed: " + data.error);
            }
        })
        .catch(err => console.error(err));
    };
    fileInput.click();
});

// Testimonial Slider Functionality
let currentTestimonial = 0;
const testimonialSlider = document.querySelector(".testimonial-slider");

function loadTestimonials() {
    // You can replace this with actual fetch call to your backend
    const testimonials = [
        {
            text: "Autism ERP provided invaluable resources to help my child succeed in school.",
            author: "Parent of an autistic child"
        },
        {
            text: "The tools offered by Autism ERP have made a positive impact on my students.",
            author: "Special Education Teacher"
        },
        {
            text: "The school and doctor lists saved us so much time in finding the right help.",
            author: "Concerned Parent"
        },
        {
            text: "The study materials are perfectly tailored for my child's needs.",
            author: "Grateful Mother"
        }
    ];

    testimonialSlider.innerHTML = '';
    testimonials.forEach(testimonial => {
        const div = document.createElement("div");
        div.classList.add("testimonial");
        div.innerHTML = `<p>"${testimonial.text}"</p><h4>- ${testimonial.author}</h4>`;
        testimonialSlider.appendChild(div);
    });

    // Auto slide testimonials
    setInterval(() => {
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        testimonialSlider.style.transform = `translateX(-${currentTestimonial * 100}%)`;
    }, 5000);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    loadTestimonials();
    
    // Initialize progress bar if exists
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        const width = progressBar.textContent.replace('%', '');
        setTimeout(() => {
            progressBar.style.width = width + '%';
        }, 300);
    }
});