// Pip-Boy 3000 Authentic Sound Effects
class PipBoySounds {
    constructor() {
        this.audioContext = null;
        this.sounds = {
            'boot': this.createBootSound.bind(this),
            'beep': this.createBeepSound.bind(this),
            'click': this.createClickSound.bind(this),
            'hover': this.createHoverSound.bind(this),
            'static': this.createStaticSound.bind(this),
            'geiger': this.createGeigerSound.bind(this),
            'tab': this.createTabSound.bind(this),
            'error': this.createErrorSound.bind(this),
            'success': this.createSuccessSound.bind(this)
        };
        
        this.initAudio();
    }
    
    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Web Audio API not supported');
        }
    }
    
    play(soundName, volume = 0.1) {
        if (!this.audioContext || !this.sounds[soundName]) {
            return;
        }
        
        try {
            this.sounds[soundName](volume);
        } catch (e) {
            console.log('Sound error:', e);
        }
    }
    
    createBootSound(volume) {
        const now = this.audioContext.currentTime;
        
        // Power on beep
        const oscillator1 = this.audioContext.createOscillator();
        const gain1 = this.audioContext.createGain();
        oscillator1.connect(gain1);
        gain1.connect(this.audioContext.destination);
        
        oscillator1.frequency.setValueAtTime(200, now);
        oscillator1.frequency.exponentialRampToValueAtTime(800, now + 0.2);
        gain1.gain.setValueAtTime(0, now);
        gain1.gain.linearRampToValueAtTime(volume, now + 0.05);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        
        oscillator1.start(now);
        oscillator1.stop(now + 0.3);
        
        // Static crackle
        setTimeout(() => {
            this.createStaticSound(volume * 0.5);
        }, 150);
    }
    
    createBeepSound(volume) {
        const now = this.audioContext.currentTime;
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800, now);
        oscillator.frequency.setValueAtTime(600, now + 0.05);
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(volume, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        
        oscillator.start(now);
        oscillator.stop(now + 0.1);
    }
    
    createClickSound(volume) {
        const now = this.audioContext.currentTime;
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        // Mechanical click with high frequency
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(1200, now);
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(volume * 0.7, now + 0.001);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.02);
        
        oscillator.start(now);
        oscillator.stop(now + 0.02);
    }
    
    createHoverSound(volume) {
        const now = this.audioContext.currentTime;
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(400, now);
        oscillator.frequency.exponentialRampToValueAtTime(600, now + 0.1);
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(volume * 0.5, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        
        oscillator.start(now);
        oscillator.stop(now + 0.1);
    }
    
    createStaticSound(volume) {
        const now = this.audioContext.currentTime;
        const duration = 0.1;
        
        // Create noise buffer
        const bufferSize = this.audioContext.sampleRate * duration;
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const output = buffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
        
        const source = this.audioContext.createBufferSource();
        const gain = this.audioContext.createGain();
        
        source.buffer = buffer;
        source.connect(gain);
        gain.connect(this.audioContext.destination);
        
        // Filter to make it sound like radio static
        const filter = this.audioContext.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.value = 1000;
        filter.Q.value = 1;
        
        gain.gain.setValueAtTime(volume * 0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
        
        source.start(now);
    }
    
    createGeigerSound(volume) {
        const now = this.audioContext.currentTime;
        
        // Quick click with decay
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(2000, now);
        
        gain.gain.setValueAtTime(volume * 0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
        
        oscillator.start(now);
        oscillator.stop(now + 0.05);
    }
    
    createTabSound(volume) {
        const now = this.audioContext.currentTime;
        
        // Two quick beeps for tab switching
        for (let i = 0; i < 2; i++) {
            const oscillator = this.audioContext.createOscillator();
            const gain = this.audioContext.createGain();
            
            oscillator.connect(gain);
            gain.connect(this.audioContext.destination);
            
            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(600 + (i * 200), now + (i * 0.03));
            
            gain.gain.setValueAtTime(0, now + (i * 0.03));
            gain.gain.linearRampToValueAtTime(volume * 0.6, now + (i * 0.03) + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.001, now + (i * 0.03) + 0.05);
            
            oscillator.start(now + (i * 0.03));
            oscillator.stop(now + (i * 0.03) + 0.05);
        }
    }
    
    createErrorSound(volume) {
        const now = this.audioContext.currentTime;
        
        // Low error buzz
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(300, now);
        oscillator.frequency.setValueAtTime(200, now + 0.1);
        
        gain.gain.setValueAtTime(volume * 0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
        
        oscillator.start(now);
        oscillator.stop(now + 0.2);
    }
    
    createSuccessSound(volume) {
        const now = this.audioContext.currentTime;
        
        // Rising success tone
        const oscillator = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        oscillator.connect(gain);
        gain.connect(this.audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(400, now);
        oscillator.frequency.exponentialRampToValueAtTime(800, now + 0.3);
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(volume * 0.7, now + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        
        oscillator.start(now);
        oscillator.stop(now + 0.3);
    }
}

// Initialize and expose globally
let pipBoyAudio;
document.addEventListener('DOMContentLoaded', () => {
    pipBoyAudio = new PipBoySounds();
    window.pipBoyAudio = pipBoyAudio;
    
    // Override the simple playSound with enhanced sounds
    const originalPlaySound = window.playSound;
    window.playSound = function(type) {
        if (pipBoyAudio && pipBoyAudio.audioContext) {
            pipBoyAudio.play(type);
        } else if (originalPlaySound) {
            originalPlaySound(type);
        }
    };
});