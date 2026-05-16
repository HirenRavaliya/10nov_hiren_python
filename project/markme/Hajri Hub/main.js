// Initialize Lucide Icons
lucide.createIcons();

// Initialize AOS (Animate on Scroll)
AOS.init({
    duration: 1000,
    once: true,
    offset: 100,
    easing: 'ease-out-cubic'
});

// --- 'THE TECH GRID' - THREE.JS 3D ENGINE ---
const canvas = document.getElementById('bg-canvas');
const colorGreen = 0x82bc4a;

// Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ 
    canvas: canvas, 
    antialias: true, 
    alpha: true 
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// Tech Group
const techGroup = new THREE.Group();
scene.add(techGroup);

// 1. Digital Floor (Grid)
const gridHelper = new THREE.GridHelper(100, 50, colorGreen, 0x112211);
gridHelper.position.y = -5;
techGroup.add(gridHelper);

// 2. Rising Data Cubes
const cubes = [];
const cubeCount = 40;
for(let i = 0; i < cubeCount; i++) {
    const size = Math.random() * 0.5 + 0.1;
    const geometry = new THREE.BoxGeometry(size, size, size);
    const material = new THREE.MeshStandardMaterial({ 
        color: colorGreen,
        transparent: true,
        opacity: 0.6,
        emissive: colorGreen,
        emissiveIntensity: 2
    });
    const cube = new THREE.Mesh(geometry, material);
    
    cube.position.set(
        (Math.random() - 0.5) * 40,
        (Math.random() - 0.5) * 20 - 5,
        (Math.random() - 0.5) * 40
    );
    
    const cubeObj = {
        mesh: cube,
        speed: Math.random() * 0.05 + 0.01,
        rotSpeed: Math.random() * 0.02
    };
    cubes.push(cubeObj);
    techGroup.add(cube);
}

// 3. Ambient Connections (Lines)
const lineMaterial = new THREE.LineBasicMaterial({ color: colorGreen, transparent: true, opacity: 0.1 });
for(let i = 0; i < 20; i++) {
    const points = [];
    points.push(new THREE.Vector3((Math.random()-0.5)*50, -5, (Math.random()-0.5)*50));
    points.push(new THREE.Vector3((Math.random()-0.5)*50, 15, (Math.random()-0.5)*50));
    const lineGeom = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(lineGeom, lineMaterial);
    techGroup.add(line);
}

// Lighting
const mainLight = new THREE.PointLight(colorGreen, 15);
mainLight.position.set(0, 10, 0);
scene.add(mainLight);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
scene.add(ambientLight);

camera.position.set(0, 5, 15);
camera.lookAt(0, 0, 0);

// Mouse Interaction
let mouseX = 0;
let mouseY = 0;

window.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - window.innerWidth / 2) / 500;
    mouseY = (event.clientY - window.innerHeight / 2) / 500;
});

// Animation Loop
const clock = new THREE.Clock();

function animate() {
    const elapsedTime = clock.getElapsedTime();
    
    // Rotate Tech Group
    techGroup.rotation.y = elapsedTime * 0.05;
    
    // Cube Animation
    cubes.forEach(c => {
        c.mesh.position.y += c.speed;
        c.mesh.rotation.x += c.rotSpeed;
        c.mesh.rotation.z += c.rotSpeed;
        
        if(c.mesh.position.y > 15) {
            c.mesh.position.y = -10;
        }
    });
    
    // Smooth Camera Follow
    camera.position.x += (mouseX * 5 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 5 + 5 - camera.position.y) * 0.05;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

// Resize Handling
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();

// --- UI LOGIC ---

const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('bg-dark/95', 'backdrop-blur-xl', 'py-2', 'shadow-2xl', 'border-b', 'border-primaryGreen/20');
        navbar.classList.remove('py-4');
    } else {
        navbar.classList.remove('bg-dark/95', 'backdrop-blur-xl', 'py-2', 'shadow-2xl', 'border-b', 'border-primaryGreen/20');
        navbar.classList.add('py-4');
    }
});

const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const closeMenuBtn = document.getElementById('close-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

function toggleMenu() {
    mobileMenu.classList.toggle('active');
    document.body.classList.toggle('overflow-hidden');
}

mobileMenuBtn.addEventListener('click', toggleMenu);
closeMenuBtn.addEventListener('click', toggleMenu);

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            if (mobileMenu.classList.contains('active')) toggleMenu();
        }
    });
});
