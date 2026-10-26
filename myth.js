// Homepage artwork: Kitsune (the guardian), the dragon (the struggle), Pegasus (freedom).
// Three still paintings behind the words. Nothing slides; small natural things keep them alive:
// rain, fireflies, lantern light and fox-fires at the shrine, mist and plum petals on the scroll,
// sunlight and wandering golden motes in Pegasus' sky. The dragon's coils and Pegasus' legs move in short
// see-through loops placed exactly over the painted creatures.
// Between chapters one painting fades out and the next fades in.
(function () {
    'use strict';

    const section = document.querySelector('.myth');
    if (!section) return;
    const stage = section.querySelector('.myth-stage');
    const chapters = [...section.querySelectorAll('.chapter')];
    const scenes = [...stage.querySelectorAll('.myth-scene')];   // kitsune, dragon, pegasus
    const rigs = scenes.map(s => s.querySelector('.myth-rig'));
    const parts = scenes.map(s => [...s.querySelectorAll('.myth-part')]);
    const canvases = scenes.map(s => s.querySelector('.myth-fx'));
    const videos = scenes.map(s => [...s.querySelectorAll('video')]);
    // Safari only plays see-through video as HEVC; everyone else gets VP9 WebM
    const ext = /Apple/.test(navigator.vendor) ? '.mov' : '.webm';
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const small = window.matchMedia('(max-width: 820px)').matches;
    const TONES = ['dark', 'light', 'dark'];
    const ART = [1920, 1088];          // every painting and its layers share this size

    // story time T: sections 0 intro, 1 kitsune, 2 gap, 3 dragon, 4 gap, 5 pegasus, 6 final.
    // Each painting is shown over its own stretch; in the gaps one fades out, then the next fades in.
    const SPANS = [[0, 2.5], [2.5, 4.5], [4.5, 7]];
    const FADE = 0.2;

    const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
    const rnd = (a, b) => a + Math.random() * (b - a);
    const many = (n, make) => Array.from({ length: n }, make);

    // T: the section in the middle of the screen, plus how far through it we are.
    function storyTime() {
        const mid = window.innerHeight / 2;
        for (let i = chapters.length - 1; i >= 0; i--) {
            const r = chapters[i].getBoundingClientRect();
            if (r.top <= mid) return i + clamp((mid - r.top) / r.height, 0, 1);
        }
        return 0;
    }

    // Size each rig to cover the screen at the painting's own proportions, framed on its subject.
    let W = 0, H = 0, rigW = 0;
    function layout() {
        W = stage.clientWidth;
        H = stage.clientHeight;
        const s = Math.max(W / ART[0], H / ART[1]), h = ART[1] * s;
        rigW = ART[0] * s;
        rigs.forEach(r => {
            const focus = +(W < H && r.dataset.focusTall || r.dataset.focus || 0.5);
            const x = clamp(W / 2 - focus * rigW, W - rigW, 0);
            Object.assign(r.style, { width: rigW + 'px', height: h + 'px', transform: `translate(${x}px, ${(H - h) / 2}px)` });
        });
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvases.forEach(c => {
            c.width = W * dpr;
            c.height = H * dpr;
            c.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
        });
    }

    /* ---------- the small living things, one canvas per painting ---------- */
    const rain = many(small ? 50 : 100, () => ({ x: rnd(0, 1.2), y: rnd(0, 1), l: rnd(0.04, 0.11), v: rnd(0.9, 1.5), a: rnd(0.07, 0.17) }));
    const spawnPetal = (p, anywhere) => Object.assign(p, {
        x: anywhere ? rnd(0, 1.1) : rnd(0.85, 1.1), y: anywhere ? rnd(0.1, 1) : rnd(0.45, 0.95),
        vx: rnd(0.035, 0.07), vy: rnd(0.008, 0.025), r: rnd(3.6, 6.2), s: rnd(0, 6), w: rnd(1, 2.4),
        c: Math.random() < 0.3 ? '222,120,128' : '190,52,58',
    });
    const petals = many(small ? 14 : 30, () => spawnPetal({}, true));
    // things that wander instead of sliding: each follows its own slow looping curve
    const wanderers = n => many(n, () => ({ x: rnd(0, 1), y: rnd(0, 1), r: rnd(1.6, 3.6), s: rnd(0, 6), f: rnd(0.15, 0.35), a: rnd(0.02, 0.05), v: rnd(-0.012, 0.004) }));
    const fireflies = wanderers(small ? 10 : 18);
    const motes = wanderers(small ? 22 : 40);
    function wander(g, list, dt, t, color, minX) {
        for (const m of list) {
            m.y += m.v * dt;
            if (m.y < -0.05) { m.y = 1.05; m.x = rnd(minX, 1); }
            if (m.y > 1.05) { m.y = -0.05; m.x = rnd(minX, 1); }
            const x = (m.x + Math.sin(t * m.f + m.s) * m.a + Math.sin(t * m.f * 2.3 + m.s * 2) * m.a * 0.5) * W;
            const y = (m.y + Math.cos(t * m.f * 1.4 + m.s) * m.a) * H;
            const glow = 0.35 + 0.65 * Math.max(0, Math.sin(t * m.f * 6 + m.s));      // fireflies pulse
            const gr = g.createRadialGradient(x, y, 0, x, y, m.r * 4);
            gr.addColorStop(0, `rgba(${color},${0.9 * glow})`);
            gr.addColorStop(0.35, `rgba(${color},${0.3 * glow})`);
            gr.addColorStop(1, `rgba(${color},0)`);
            g.fillStyle = gr;
            g.fillRect(x - m.r * 4, y - m.r * 4, m.r * 8, m.r * 8);
        }
    }

    const draw = {
        rain(g, dt, t) {
            wander(g, fireflies, dt, t, '226,240,160', 0.35);
            g.lineWidth = 1;
            for (const d of rain) {
                d.y += d.v * dt;
                if (d.y > 1 + d.l) { d.y = -d.l; d.x = rnd(0, 1.2); }
                const x = d.x * W, y = d.y * H, l = d.l * H;
                g.strokeStyle = `rgba(226,232,240,${d.a})`;
                g.beginPath();
                g.moveTo(x, y);
                g.lineTo(x - l * 0.07, y - l);
                g.stroke();
            }
        },
        petals(g, dt, t) {
            for (const p of petals) {
                p.x -= p.vx * dt * (1 + 0.4 * Math.sin(t * 0.7));            // gusts
                p.y += p.vy * dt + Math.sin(t * p.w + p.s) * 0.0006;
                if (p.x < -0.05 || p.y > 1.05) spawnPetal(p, false);
                g.save();
                g.translate(p.x * W, p.y * H);
                g.rotate(t * p.w + p.s);
                g.scale(1, 0.45 + 0.4 * Math.abs(Math.sin(t * p.w * 1.3 + p.s)));   // tumbling
                g.fillStyle = `rgba(${p.c},0.85)`;
                g.beginPath();
                g.ellipse(0, 0, p.r, p.r * 0.7, 0, 0, Math.PI * 2);
                g.fill();
                g.restore();
            }
        },
        sky(g, dt, t) {
            wander(g, motes, dt, t, '255,232,180', 0);
        },
    };

    let last = 0;
    function frame(now) {
        const T = storyTime(), t = now / 1000;
        const dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
        last = now;
        scenes.forEach((scene, i) => {
            const [a, b] = SPANS[i];
            const fadeIn = i === 0 ? 1 : clamp((T - a) / FADE, 0, 1);
            const fadeOut = i === scenes.length - 1 ? 1 : clamp((b - T) / FADE, 0, 1);
            const shown = Math.min(fadeIn, fadeOut);
            scene.style.opacity = shown;
            videos[i].forEach(v => {
                if (!v.src && T > a - 1) v.src = v.dataset.src + ext;   // load a chapter ahead
                if (still) return;
                if (shown > 0 && v.paused && v.src) v.play().catch(() => {});
                if (shown === 0 && !v.paused) v.pause();
            });
            if (still || shown === 0) return;
            parts[i].forEach(el => {
                const drop = +el.dataset.drop || 0;
                if (drop && !el.style.transform) el.style.transform = `translateY(${drop * H}px)`;
            });
            const c = canvases[i], g = c.getContext('2d');
            g.clearRect(0, 0, W, H);
            draw[c.dataset.fx](g, dt, t);
        });
        const at = SPANS.findIndex(([, b]) => T < b);
        stage.dataset.tone = TONES[at < 0 ? TONES.length - 1 : at];

        if (running) requestAnimationFrame(frame);
    }

    let running = false;
    layout();
    window.addEventListener('resize', () => {
        layout();
        parts.flat().forEach(el => { el.style.transform = ''; });
        frame(performance.now());
    });
    if (still) {
        window.addEventListener('scroll', () => requestAnimationFrame(frame), { passive: true });
        frame(0);
    } else {
        // animate only while the artwork is on screen
        new IntersectionObserver(([entry]) => {
            const was = running;
            running = entry.isIntersecting;
            if (running && !was) {
                last = 0;
                requestAnimationFrame(frame);
            }
        }).observe(section);
        frame(performance.now());
    }
})();
