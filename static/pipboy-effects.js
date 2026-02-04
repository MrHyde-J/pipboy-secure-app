// Pip-Boy UI Effects and Sound
document.addEventListener('DOMContentLoaded', function() {
    // CRT Scanline Effect
    const scanlines = document.querySelector('.scanlines');
    if (scanlines) {
        let position = 0;
        setInterval(() => {
            position = (position + 1) % 4;
            scanlines.style.backgroundPosition = `0px ${position}px`;
        }, 100);
    }

    // Terminal Typewriter Effect
    const typewriterElements = document.querySelectorAll('.typewriter');
    typewriterElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        
        // Start with a delay
        setTimeout(typeWriter, 1000);
    });

    // Button Click Sound
    const buttons = document.querySelectorAll('.pipboy-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            playSound('beep');
            // Add visual feedback
            this.classList.add('active');
            setTimeout(() => {
                this.classList.remove('active');
            }, 150);
        });
    });

    // Input Field Focus Effects
    const inputs = document.querySelectorAll('.pipboy-input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (this.parentElement) {
                this.parentElement.classList.add('focused');
            }
            playSound('beep');
        });
        
        input.addEventListener('blur', function() {
            if (this.parentElement) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Add typing sound effect
        let typingTimer;
        input.addEventListener('input', function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                playSound('click');
            }, 200);
        });
    });

    // Navigation Hover Effects
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            playSound('hover');
            this.style.transform = 'translateY(-2px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Password Toggle Visibility
    const toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (!input) return;
            
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Change icon
            this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
            playSound('click');
        });
    });

    // Flash Messages Auto-hide
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (message.parentElement) {
                    message.remove();
                }
            }, 300);
        }, 5000);
    });

    // Random Terminal Glitch Effect
    let glitchInterval;
    try {
        glitchInterval = setInterval(() => {
            if (Math.random() < 0.01) { // 1% chance every interval
                document.body.classList.add('glitch');
                setTimeout(() => {
                    document.body.classList.remove('glitch');
                }, 100);
            }
        }, 1000);
    } catch (e) {
        console.log('Glitch effect error:', e);
    }

    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        if (glitchInterval) {
            clearInterval(glitchInterval);
        }
        if (audioContext && audioContext.state !== 'closed') {
            audioContext.close().catch(e => console.log('Audio context close error:', e));
        }
    });
// Add these functions to the existing file

function initPipBoyEffects() {
    // Terminal Boot Sequence
    if (!sessionStorage.getItem('pipboy_booted')) {
        showBootSequence();
        sessionStorage.setItem('pipboy_booted', 'true');
    }
    
    // Geiger Counter Random Clicks
    initGeigerCounter();
    
    // Radio Static Background
    initRadioStatic();
    
    // Screen Power Save Mode
    initPowerSave();
    
    // Authentic Button Press Effects
    enhanceButtons();
    
    // Inventory-like Hover Sounds
    initInventorySounds();
}

function showBootSequence() {
    const bootText = `
╔══════════════════════════════════════════════╗
║        VAULT-TEC INDUSTRIES BOOTLOADER      ║
║              PIP-BOY 3000 MK IV             ║
║              FIRMWARE v2.1.7                ║
║                                              ║
║  INITIALIZING SECURITY SUBSYSTEM...   [OK]  ║
║  LOADING USER INTERFACE...            [OK]  ║
║  CALIBRATING GEIGER COUNTER...        [OK]  ║
║  SYNCING WITH VAULT NETWORK...        [OK]  ║
║                                              ║
║            WELCOME TO THE WASTELAND          ║
╚══════════════════════════════════════════════╝
`;
    
    const bootDiv = document.createElement('div');
    bootDiv.className = 'boot-sequence';
    bootDiv.innerHTML = `<pre class="boot-text">${bootText}</pre>`;
    document.body.appendChild(bootDiv);
    
    // Type out boot sequence
    let i = 0;
    const pre = bootDiv.querySelector('pre');
    const originalText = pre.textContent;
    pre.textContent = '';
    
    function typeBoot() {
        if (i < originalText.length) {
            pre.textContent += originalText.charAt(i);
            i++;
            setTimeout(typeBoot, 30);
            
            // Add typing sound
            if (i % 3 === 0 && window.playSound) {
                window.playSound('click');
            }
        } else {
            // Fade out after delay
            setTimeout(() => {
                bootDiv.style.opacity = '0';
                bootDiv.style.transition = 'opacity 1s';
                setTimeout(() => {
                    bootDiv.remove();
                    // Play startup sound
                    if (window.playSound) {
                        window.playSound('beep');
                    }
                }, 1000);
            }, 2000);
        }
    }
    
    setTimeout(typeBoot, 500);
}

function initGeigerCounter() {
    // Create geiger counter element
    const geigerDiv = document.createElement('div');
    geigerDiv.className = 'geiger-counter';
    geigerDiv.innerHTML = `
        <div class="geiger-dial"></div>
        <div class="geiger-needle"></div>
    `;
    document.body.appendChild(geigerDiv);
    
    // Random geiger clicks
    setInterval(() => {
        if (Math.random() < 0.1) { // 10% chance every interval
            if (window.playSound) {
                window.playSound('click');
            }
            // Visual feedback
            geigerDiv.style.opacity = '0.7';
            setTimeout(() => {
                geigerDiv.style.opacity = '0.3';
            }, 100);
        }
    }, 1000);
}

function initRadioStatic() {
    // Add subtle radio static background
    const staticCanvas = document.createElement('canvas');
    staticCanvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.02;
        z-index: 9998;
        mix-blend-mode: screen;
    `;
    document.body.appendChild(staticCanvas);
    
    const ctx = staticCanvas.getContext('2d');
    
    function resizeCanvas() {
        staticCanvas.width = window.innerWidth;
        staticCanvas.height = window.innerHeight;
    }
    
    function drawStatic() {
        if (!ctx) return;
        
        const imageData = ctx.createImageData(staticCanvas.width, staticCanvas.height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < 0.01) { // Very sparse static
                const brightness = Math.floor(Math.random() * 50);
                data[i] = 0; // R
                data[i + 1] = brightness; // G
                data[i + 2] = 0; // B
                data[i + 3] = 255; // A
            }
        }
        
        ctx.putImageData(imageData, 0, 0);
    }
    
    function animateStatic() {
        drawStatic();
        requestAnimationFrame(animateStatic);
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    animateStatic();
}

function initPowerSave() {
    // Screen dimming after inactivity
    let inactivityTimer;
    const screen = document.querySelector('.pipboy-screen');
    
    function resetTimer() {
        if (screen) {
            screen.style.opacity = '1';
            screen.style.filter = 'none';
        }
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(dimScreen, 30000); // 30 seconds
    }
    
    function dimScreen() {
        if (screen) {
            screen.style.opacity = '0.7';
            screen.style.filter = 'brightness(0.7)';
        }
    }
    
    // Reset on any interaction
    ['mousemove', 'keydown', 'click', 'scroll'].forEach(event => {
        document.addEventListener(event, resetTimer);
    });
    
    resetTimer();
}

function enhanceButtons() {
    // Add authentic button press effects
    const buttons = document.querySelectorAll('.pipboy-btn, .nav-item, .password-toggle');
    
    buttons.forEach(button => {
        // Remove existing click listeners if any
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        newButton.addEventListener('mousedown', function(e) {
            this.style.transform = 'translateY(4px) scale(0.98)';
            this.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.5)';
            
            // Mechanical click sound
            if (window.playSound) {
                setTimeout(() => window.playSound('click'), 50);
            }
        });
        
        newButton.addEventListener('mouseup', function(e) {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
        
        newButton.addEventListener('mouseleave', function(e) {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
}

function initInventorySounds() {
    // Inventory-like sounds for list items
    const listItems = document.querySelectorAll('.inventory-item, .user-item, .result-item');
    
    listItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            if (window.playSound) {
                window.playSound('hover');
            }
        });
        
        item.addEventListener('click', function() {
            if (window.playSound) {
                window.playSound('click');
            }
        });
    });
}

// Add to DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    
    // Initialize enhanced effects
    setTimeout(initPipBoyEffects, 1000);
});
    // Initialize audio context for sounds
    let audioContext;
    
    function playSound(type) {
        try {
            // Don't play sounds if user prefers reduced motion
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                return;
            }
            
            if (!audioContext) {
                try {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                } catch (e) {
                    console.log('Audio context not supported');
                    return;
                }
            }
            
            // Resume audio context if suspended (browser policy)
            if (audioContext.state === 'suspended') {
                audioContext.resume().catch(e => console.log('Audio resume error:', e));
            }
            
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            const now = audioContext.currentTime;
            
            switch(type) {
                case 'beep':
                    oscillator.frequency.setValueAtTime(800, now);
                    gainNode.gain.setValueAtTime(0.05, now); // Reduced volume
                    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
                    oscillator.start(now);
                    oscillator.stop(now + 0.1);
                    break;
                    
                case 'click':
                    oscillator.frequency.setValueAtTime(1200, now);
                    gainNode.gain.setValueAtTime(0.03, now); // Reduced volume
                    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
                    oscillator.start(now);
                    oscillator.stop(now + 0.05);
                    break;
                    
                case 'hover':
                    oscillator.frequency.setValueAtTime(600, now);
                    oscillator.frequency.exponentialRampToValueAtTime(800, now + 0.1);
                    gainNode.gain.setValueAtTime(0.03, now); // Reduced volume
                    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
                    oscillator.start(now);
                    oscillator.stop(now + 0.1);
                    break;
                    
                default:
                    oscillator.frequency.setValueAtTime(1000, now);
                    gainNode.gain.setValueAtTime(0.02, now);
                    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
                    oscillator.start(now);
                    oscillator.stop(now + 0.1);
            }
            
        } catch (e) {
            console.log('Sound play error:', e);
        }
    }

    // Make playSound available globally with safety checks
    window.playSound = function(type) {
        try {
            playSound(type);
        } catch (e) {
            console.log('Global playSound error:', e);
        }
    };
});