// Tech-Interactives Radar System - Frontend

let scene, camera, renderer;
let socket;
let receiverMeshes = {};
let latestData = {};

function init() {
    console.log('%cTech-Interactives Radar System', 'color: #00ff00; font-size: 16px; font-weight: bold;');
    
    initThreeJS();
    connectWebSocket();
    updateClock();
}

function initThreeJS() {
    const container = document.getElementById('canvas');
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    scene.fog = new THREE.FogExp2(0x000000, 0.002);
    
    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(5, 8, 10);
    camera.lookAt(0, 0, 0);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0x00ff00, 0.3);
    scene.add(ambientLight);
    
    const pointLight = new THREE.PointLight(0x0099ff, 1, 100);
    pointLight.position.set(5, 10, 5);
    scene.add(pointLight);
    
    // Floor grid
    const gridHelper = new THREE.GridHelper(20, 20, 0x003300, 0x001a00);
    scene.add(gridHelper);
    
    // Router
    const routerGeo = new THREE.BoxGeometry(0.8, 0.4, 0.8);
    const routerMat = new THREE.MeshStandardMaterial({ color: 0x333333, emissive: 0x0099ff });
    const router = new THREE.Mesh(routerGeo, routerMat);
    router.position.y = 1;
    scene.add(router);
    
    // Receivers
    const positions = [
        { x: -7, z: -7, id: 1 },
        { x: 7, z: -7, id: 2 },
        { x: -7, z: 7, id: 3 },
        { x: 7, z: 7, id: 4 }
    ];
    
    positions.forEach(pos => {
        const geo = new THREE.BoxGeometry(0.4, 0.4, 0.4);
        const mat = new THREE.MeshStandardMaterial({ color: 0x00ff00, emissive: 0x00ff00 });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(pos.x, 0.2, pos.z);
        scene.add(mesh);
        receiverMeshes[pos.id] = mesh;
    });
    
    // Animate
    animate();
    window.addEventListener('resize', onWindowResize);
}

function animate() {
    requestAnimationFrame(animate);
    
    Object.values(receiverMeshes).forEach(mesh => {
        if (mesh) {
            mesh.rotation.x += 0.01;
            mesh.rotation.y += 0.01;
        }
    });
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = document.getElementById('canvas');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function connectWebSocket() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to backend');
        document.getElementById('status').textContent = '● Online';
        document.getElementById('status').style.color = '#00ff00';
        document.getElementById('message').textContent = 'Connected to Tech-Interactives';
    });
    
    socket.on('disconnect', () => {
        document.getElementById('status').textContent = '● Offline';
        document.getElementById('status').style.color = '#ff3333';
    });
    
    socket.on('detection', (data) => {
        latestData = data;
        updateMetrics();
    });
}

function updateMetrics() {
    if (!latestData) return;
    
    document.getElementById('rssi').textContent = latestData.rssi + ' dBm';
    document.getElementById('quality').textContent = Math.round(latestData.rssi * 2 + 200) + '%';
    
    if (latestData.presence) {
        document.getElementById('presence').textContent = latestData.presence.detected ? 'Yes' : 'No';
    }
    
    if (latestData.motion) {
        document.getElementById('motion').textContent = Math.round(latestData.motion.intensity) + '%';
    }
    
    if (latestData.breathing) {
        document.getElementById('breathing').textContent = Math.round(latestData.breathing.breathing_rate) + ' bpm';
    }
}

function updateClock() {
    setInterval(() => {
        const now = new Date();
        document.getElementById('time').textContent = now.toLocaleTimeString();
    }, 1000);
}

function resetView() {
    camera.position.set(5, 8, 10);
    camera.lookAt(0, 0, 0);
}

function calibrate() {
    alert('Calibration mode: Ensure room is empty and click OK');
}

function toggleSettings() {
    alert('Settings panel coming soon');
}

// Start when DOM loaded
document.addEventListener('DOMContentLoaded', init);
